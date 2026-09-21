import os
import json
import numpy as np
import pandas as pd
# pyrefly: ignore [missing-import]
import torch
# pyrefly: ignore [missing-import]
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, recall_score, precision_score, f1_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seeds for reproducibility
SEED = 42
np.random.seed(SEED)
torch.manual_seed(SEED)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "Week_1_Data_Cleaning", "HR_Analytics_Cleaned.csv")
OUTPUT_JSON = os.path.join(BASE_DIR, "deep_learning_summary.json")

def load_and_preprocess_data():
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded dataset with shape: {df.shape}")
    
    # Target column
    if 'Attrition_Numeric' in df.columns:
        y = df['Attrition_Numeric'].values
    else:
        y = (df['Attrition'].astype(str).str.strip().str.lower() == 'yes').astype(int).values
        
    # Exclude target & redundant non-feature columns
    exclude_cols = ['Attrition', 'Attrition_Numeric', 'MonthlyIncome_Uncapped']
    feature_df = df.drop(columns=[c for c in exclude_cols if c in df.columns])
    
    # One-hot encode categorical features
    feature_df_encoded = pd.get_dummies(feature_df, drop_first=True)
    
    X = feature_df_encoded.values.astype(np.float32)
    feature_names = feature_df_encoded.columns.tolist()
    
    print(f"Engineered X shape: {X.shape}, total features: {len(feature_names)}")
    return df, X, y, feature_names

# Define PyTorch Multi-Layer Perceptron (Sequential ANN)
class HRAttritionANN(nn.Module):
    def __init__(self, input_dim):
        super(HRAttritionANN, self).__init__()
        # Layer 1: Dense 64, ReLU, Dropout 0.3
        self.fc1 = nn.Linear(input_dim, 64)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.3)
        
        # Layer 2: Dense 32, ReLU, Dropout 0.2
        self.fc2 = nn.Linear(64, 32)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.2)
        
        # Output Layer: Dense 1, Sigmoid
        self.fc3 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        out = self.dropout1(self.relu1(self.fc1(x)))
        out = self.dropout2(self.relu2(self.fc2(out)))
        out = self.sigmoid(self.fc3(out))
        return out

def train_and_evaluate():
    df, X, y, feature_names = load_and_preprocess_data()
    
    # 80/20 train/test split
    X_train_full, X_test, y_train_full, y_test = train_test_split(
        X, y, test_size=0.20, random_state=SEED, stratify=y
    )
    
    # 80/20 train/validation split within train_full (effectively 64% train, 16% val, 20% test)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_full, y_train_full, test_size=0.20, random_state=SEED, stratify=y_train_full
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Convert to PyTorch Tensors
    X_tr_t = torch.tensor(X_train_scaled, dtype=torch.float32)
    y_tr_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    
    X_val_t = torch.tensor(X_val_scaled, dtype=torch.float32)
    y_val_t = torch.tensor(y_val, dtype=torch.float32).unsqueeze(1)
    
    X_te_t = torch.tensor(X_test_scaled, dtype=torch.float32)
    y_te_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)
    
    # Data Loaders
    batch_size = 32
    train_dataset = TensorDataset(X_tr_t, y_tr_t)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    # Dynamic Class Weighting for BCE Loss
    neg_count = np.sum(y_train == 0)
    pos_count = np.sum(y_train == 1)
    pos_weight = torch.tensor([neg_count / float(pos_count)], dtype=torch.float32)
    print(f"Train class balance: Stayed={neg_count}, Departed={pos_count}. Pos weight = {pos_weight.item():.4f}")
    
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    
    # Model instantiation
    input_dim = X_train_scaled.shape[1]
    model = HRAttritionANN(input_dim)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Early Stopping params
    patience = 15
    best_val_loss = float('inf')
    best_model_state = None
    best_epoch = 0
    
    history = {
        'epoch': [],
        'train_loss': [],
        'val_loss': [],
        'val_auc': []
    }
    
    max_epochs = 100
    
    for epoch in range(1, max_epochs + 1):
        model.train()
        running_loss = 0.0
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            # Forward pass before sigmoid for BCEWithLogitsLoss
            # Compute raw logits: fc3(dropout2(relu2(fc2(...))))
            out1 = model.dropout1(model.relu1(model.fc1(batch_X)))
            out2 = model.dropout2(model.relu2(model.fc2(out1)))
            logits = model.fc3(out2)
            
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * batch_X.size(0)
            
        epoch_train_loss = running_loss / len(train_dataset)
        
        # Validation phase
        model.eval()
        with torch.no_grad():
            out1_val = model.relu1(model.fc1(X_val_t))
            out2_val = model.relu2(model.fc2(out1_val))
            val_logits = model.fc3(out2_val)
            val_probs = torch.sigmoid(val_logits).numpy()
            val_loss = nn.BCEWithLogitsLoss(pos_weight=pos_weight)(val_logits, y_val_t).item()
            val_auc = roc_auc_score(y_val, val_probs)
            
        history['epoch'].append(epoch)
        history['train_loss'].append(float(epoch_train_loss))
        history['val_loss'].append(float(val_loss))
        history['val_auc'].append(float(val_auc))
        
        # Early Stopping Check
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_model_state = model.state_dict().copy()
            best_epoch = epoch
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping triggered at epoch {epoch}. Restoring best epoch {best_epoch} weights (Val Loss: {best_val_loss:.4f})")
                break
                
    # Restore best weights
    model.load_state_dict(best_model_state)
    model.eval()
    
    # Test set evaluation
    with torch.no_grad():
        out1_te = model.relu1(model.fc1(X_te_t))
        out2_te = model.relu2(model.fc2(out1_te))
        te_logits = model.fc3(out2_te)
        test_probs = torch.sigmoid(te_logits).numpy().flatten()
        test_preds = (test_probs >= 0.5).astype(int)
        
    test_auc = float(roc_auc_score(y_test, test_probs))
    test_recall = float(recall_score(y_test, test_preds))
    test_precision = float(precision_score(y_test, test_preds))
    test_f1 = float(f1_score(y_test, test_preds))
    cm = confusion_matrix(y_test, test_preds).tolist()
    
    print("\n--- Test Set Evaluation ---")
    print(f"ROC-AUC Score: {test_auc:.4f}")
    print(f"Attrited Recall (Sensitivity): {test_recall:.4f}")
    print(f"Attrited Precision: {test_precision:.4f}")
    print(f"Attrited F1-Score: {test_f1:.4f}")
    print("Confusion Matrix (TN, FP, FN, TP):", cm)
    
    # Save visualizations
    fig_dir = os.path.join(BASE_DIR, "figures")
    os.makedirs(fig_dir, exist_ok=True)
    
    # Plot 1: Loss & Validation AUC Trajectory
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history['epoch'], history['train_loss'], label='Train Loss', color='#6366f1')
    plt.plot(history['epoch'], history['val_loss'], label='Val Loss', color='#ec4899', linestyle='--')
    plt.axvline(best_epoch, color='#10b981', linestyle=':', label=f'Best Epoch ({best_epoch})')
    plt.title('Training & Validation Loss Trajectory')
    plt.xlabel('Epoch')
    plt.ylabel('BCE Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history['epoch'], history['val_auc'], label='Val ROC-AUC', color='#8b5cf6')
    plt.axvline(best_epoch, color='#10b981', linestyle=':', label=f'Best Epoch ({best_epoch})')
    plt.title('Validation ROC-AUC Trajectory')
    plt.xlabel('Epoch')
    plt.ylabel('ROC-AUC Score')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "loss_trajectory.png"), dpi=300)
    plt.close()
    
    # Plot 2: Confusion Matrix Heatmap
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Stayed (0)', 'Departed (1)'], yticklabels=['Stayed (0)', 'Departed (1)'])
    plt.title(f'ANN Confusion Matrix (AUC: {test_auc:.2f})')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "confusion_matrix.png"), dpi=300)
    plt.close()
    
    # Export deep_learning_summary.json
    summary_data = {
        "dataset_samples": len(df),
        "train_samples": len(X_train),
        "val_samples": len(X_val),
        "test_samples": len(X_test),
        "input_features_count": input_dim,
        "architecture": {
            "input_dim": input_dim,
            "hidden_layer_1": {"nodes": 64, "activation": "ReLU", "dropout": 0.3},
            "hidden_layer_2": {"nodes": 32, "activation": "ReLU", "dropout": 0.2},
            "output_layer": {"nodes": 1, "activation": "Sigmoid"},
            "optimizer": "Adam",
            "learning_rate": 0.001,
            "loss_function": "Binary Cross-Entropy with Dynamic Class Weighting"
        },
        "training_trajectory": {
            "total_epochs_run": len(history['epoch']),
            "best_epoch": best_epoch,
            "best_val_loss": round(best_val_loss, 4),
            "history": history
        },
        "test_metrics": {
            "roc_auc": round(test_auc, 4),
            "recall": round(test_recall, 4),
            "precision": round(test_precision, 4),
            "f1_score": round(test_f1, 4),
            "confusion_matrix": cm,
            "tn": cm[0][0],
            "fp": cm[0][1],
            "fn": cm[1][0],
            "tp": cm[1][1]
        }
    }
    
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(summary_data, f, indent=2)
    print(f"Summary saved to {OUTPUT_JSON}")
    
    return summary_data

if __name__ == "__main__":
    train_and_evaluate()
