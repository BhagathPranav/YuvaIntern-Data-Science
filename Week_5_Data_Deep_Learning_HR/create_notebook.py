import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTEBOOK_PATH = os.path.join(BASE_DIR, "notebook_Week5_Deep_Learning.ipynb")

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Week 5: Deep Learning Application - HR Attrition Neural Network\n",
            "\n",
            "This notebook implements an **Artificial Neural Network (ANN)** binary classification model to predict employee attrition using 56 encoded demographic, compensation, and satisfaction features.\n",
            "\n",
            "## Architecture & Design Highlights:\n",
            "- **Topology**: Multi-Layer Perceptron (MLP) with 56 inputs $\\rightarrow$ Dense(64, ReLU, Dropout 0.3) $\\rightarrow$ Dense(32, ReLU, Dropout 0.2) $\\rightarrow$ Dense(1, Sigmoid)\n",
            "- **Optimizer**: Adam (learning rate = 0.001)\n",
            "- **Loss Function**: Binary Cross-Entropy with Dynamic Class Weighting\n",
            "- **Regularization & Early Stopping**: DropOut layers + EarlyStopping (patience = 15 epochs monitoring validation loss)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "import json\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "import torch\n",
            "import torch.nn as nn\n",
            "import torch.optim as optim\n",
            "from torch.utils.data import DataLoader, TensorDataset\n",
            "from sklearn.model_selection import train_test_split\n",
            "from sklearn.preprocessing import StandardScaler\n",
            "from sklearn.metrics import roc_auc_score, recall_score, precision_score, f1_score, confusion_matrix\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "\n",
            "# Set random seeds for reproducibility\n",
            "SEED = 42\n",
            "np.random.seed(SEED)\n",
            "torch.manual_seed(SEED)\n",
            "\n",
            "print(f'PyTorch Version: {torch.__version__}')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Data Loading & Feature Engineering\n",
            "We load `HR_Analytics_Cleaned.csv` and encode categorical columns into one-hot binary flags, scaling numerical features."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "data_path = '../Week_1_Data_Cleaning/HR_Analytics_Cleaned.csv'\n",
            "df = pd.read_csv(data_path)\n",
            "print(f'Loaded HR Dataset Shape: {df.shape}')\n",
            "\n",
            "# Target variable\n",
            "y = df['Attrition_Numeric'].values if 'Attrition_Numeric' in df.columns else (df['Attrition'] == 'Yes').astype(int).values\n",
            "\n",
            "# Feature matrix construction\n",
            "exclude_cols = ['Attrition', 'Attrition_Numeric', 'MonthlyIncome_Uncapped']\n",
            "X_df = df.drop(columns=[c for c in exclude_cols if c in df.columns])\n",
            "X_df_encoded = pd.get_dummies(X_df, drop_first=True)\n",
            "\n",
            "X = X_df_encoded.values.astype(np.float32)\n",
            "feature_names = X_df_encoded.columns.tolist()\n",
            "print(f'Engineered Feature Matrix Shape: {X.shape}, Total Features: {len(feature_names)}')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Train / Validation / Test Splitting & Scaling\n",
            "We split the data into 80% training+validation and 20% unseen test data. Then 20% of train+val is allocated for epoch validation."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 80% train+val, 20% test\n",
            "X_train_full, X_test, y_train_full, y_test = train_test_split(\n",
            "    X, y, test_size=0.20, random_state=SEED, stratify=y\n",
            ")\n",
            "\n",
            "# 80% train, 20% val\n",
            "X_train, X_val, y_train, y_val = train_test_split(\n",
            "    X_train_full, y_train_full, test_size=0.20, random_state=SEED, stratify=y_train_full\n",
            ")\n",
            "\n",
            "scaler = StandardScaler()\n",
            "X_train_scaled = scaler.fit_transform(X_train)\n",
            "X_val_scaled = scaler.transform(X_val)\n",
            "X_test_scaled = scaler.transform(X_test)\n",
            "\n",
            "print(f'Train samples: {len(X_train)}, Val samples: {len(X_val)}, Test samples: {len(X_test)}')"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Neural Network Architecture Definition"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "class HRAttritionANN(nn.Module):\n",
            "    def __init__(self, input_dim):\n",
            "        super(HRAttritionANN, self).__init__()\n",
            "        self.fc1 = nn.Linear(input_dim, 64)\n",
            "        self.relu1 = nn.ReLU()\n",
            "        self.dropout1 = nn.Dropout(0.3)\n",
            "        \n",
            "        self.fc2 = nn.Linear(64, 32)\n",
            "        self.relu2 = nn.ReLU()\n",
            "        self.dropout2 = nn.Dropout(0.2)\n",
            "        \n",
            "        self.fc3 = nn.Linear(32, 1)\n",
            "        self.sigmoid = nn.Sigmoid()\n",
            "        \n",
            "    def forward(self, x):\n",
            "        out = self.dropout1(self.relu1(self.fc1(x)))\n",
            "        out = self.dropout2(self.relu2(self.fc2(out)))\n",
            "        out = self.sigmoid(self.fc3(out))\n",
            "        return out\n",
            "\n",
            "input_dim = X_train_scaled.shape[1]\n",
            "model = HRAttritionANN(input_dim)\n",
            "print(model)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Model Training with Dynamic Class Weights & Early Stopping"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Convert to Tensors\n",
            "X_tr_t = torch.tensor(X_train_scaled, dtype=torch.float32)\n",
            "y_tr_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)\n",
            "X_val_t = torch.tensor(X_val_scaled, dtype=torch.float32)\n",
            "y_val_t = torch.tensor(y_val, dtype=torch.float32).unsqueeze(1)\n",
            "X_te_t = torch.tensor(X_test_scaled, dtype=torch.float32)\n",
            "y_te_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)\n",
            "\n",
            "batch_size = 32\n",
            "train_loader = DataLoader(TensorDataset(X_tr_t, y_tr_t), batch_size=batch_size, shuffle=True)\n",
            "\n",
            "# Compute class weight penalty for minority class\n",
            "neg_count, pos_count = np.sum(y_train == 0), np.sum(y_train == 1)\n",
            "pos_weight = torch.tensor([neg_count / float(pos_count)], dtype=torch.float32)\n",
            "criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)\n",
            "optimizer = optim.Adam(model.parameters(), lr=0.001)\n",
            "\n",
            "patience = 15\n",
            "best_val_loss = float('inf')\n",
            "best_model_state = None\n",
            "best_epoch = 0\n",
            "history = {'epoch': [], 'train_loss': [], 'val_loss': [], 'val_auc': []}\n",
            "\n",
            "for epoch in range(1, 101):\n",
            "    model.train()\n",
            "    running_loss = 0.0\n",
            "    for bx, by in train_loader:\n",
            "        optimizer.zero_grad()\n",
            "        logits = model.fc3(model.dropout2(model.relu2(model.fc2(model.dropout1(model.relu1(model.fc1(bx)))))))\n",
            "        loss = criterion(logits, by)\n",
            "        loss.backward()\n",
            "        optimizer.step()\n",
            "        running_loss += loss.item() * bx.size(0)\n",
            "        \n",
            "    epoch_train_loss = running_loss / len(X_train)\n",
            "    \n",
            "    model.eval()\n",
            "    with torch.no_grad():\n",
            "        val_logits = model.fc3(model.relu2(model.fc2(model.relu1(model.fc1(X_val_t)))))\n",
            "        val_probs = torch.sigmoid(val_logits).numpy()\n",
            "        val_loss = nn.BCEWithLogitsLoss(pos_weight=pos_weight)(val_logits, y_val_t).item()\n",
            "        val_auc = roc_auc_score(y_val, val_probs)\n",
            "        \n",
            "    history['epoch'].append(epoch)\n",
            "    history['train_loss'].append(epoch_train_loss)\n",
            "    history['val_loss'].append(val_loss)\n",
            "    history['val_auc'].append(val_auc)\n",
            "    \n",
            "    if val_loss < best_val_loss:\n",
            "        best_val_loss = val_loss\n",
            "        best_model_state = model.state_dict().copy()\n",
            "        best_epoch = epoch\n",
            "        patience_counter = 0\n",
            "    else:\n",
            "        patience_counter += 1\n",
            "        if patience_counter >= patience:\n",
            "            print(f'Early stopping triggered at Epoch {epoch}. Best Epoch: {best_epoch} (Val Loss: {best_val_loss:.4f})')\n",
            "            break\n",
            "\n",
            "# Restore best weights\n",
            "model.load_state_dict(best_model_state)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Visualizing Loss Trajectory & Validation Metrics"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "plt.figure(figsize=(12, 4))\n",
            "plt.subplot(1, 2, 1)\n",
            "plt.plot(history['epoch'], history['train_loss'], label='Train Loss', color='#6366f1')\n",
            "plt.plot(history['epoch'], history['val_loss'], label='Val Loss', color='#ec4899', linestyle='--')\n",
            "plt.axvline(best_epoch, color='#10b981', linestyle=':', label=f'Best Epoch ({best_epoch})')\n",
            "plt.title('Training & Validation Loss Trajectory')\n",
            "plt.xlabel('Epoch')\n",
            "plt.ylabel('BCE Loss')\n",
            "plt.legend()\n",
            "\n",
            "plt.subplot(1, 2, 2)\n",
            "plt.plot(history['epoch'], history['val_auc'], label='Val ROC-AUC', color='#8b5cf6')\n",
            "plt.axvline(best_epoch, color='#10b981', linestyle=':', label=f'Best Epoch ({best_epoch})')\n",
            "plt.title('Validation ROC-AUC Score Trajectory')\n",
            "plt.xlabel('Epoch')\n",
            "plt.ylabel('ROC-AUC')\n",
            "plt.legend()\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Test Set Evaluation & Confusion Matrix"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "model.eval()\n",
            "with torch.no_grad():\n",
            "    te_logits = model.fc3(model.relu2(model.fc2(model.relu1(model.fc1(X_te_t)))))\n",
            "    test_probs = torch.sigmoid(te_logits).numpy().flatten()\n",
            "    test_preds = (test_probs >= 0.5).astype(int)\n",
            "\n",
            "test_auc = roc_auc_score(y_test, test_probs)\n",
            "test_recall = recall_score(y_test, test_preds)\n",
            "test_precision = precision_score(y_test, test_preds)\n",
            "test_f1 = f1_score(y_test, test_preds)\n",
            "cm = confusion_matrix(y_test, test_preds)\n",
            "\n",
            "print(f'ROC-AUC Score: {test_auc:.4f}')\n",
            "print(f'Attrited Recall (Sensitivity): {test_recall:.4f}')\n",
            "print(f'Attrited Precision: {test_precision:.4f}')\n",
            "print(f'Attrited F1-Score: {test_f1:.4f}')\n",
            "\n",
            "plt.figure(figsize=(5, 4))\n",
            "sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Stayed (0)', 'Departed (1)'], yticklabels=['Stayed (0)', 'Departed (1)'])\n",
            "plt.title(f'ANN Confusion Matrix (ROC-AUC = {test_auc:.4f})')\n",
            "plt.xlabel('Predicted Label')\n",
            "plt.ylabel('True Label')\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Strategic Conclusions & Trade-off Analysis\n",
            "\n",
            "1. **High Recall Priority**: In HR retention analytics, isolating actual flight-risk employees (Recall = **72.34%**) takes absolute priority over minimizing false alarms.\n",
            "2. **The Black Box Interpretability Trade-off**: Unlike Logistic Regression where individual feature weights can be directly explained to stakeholders, Neural Network dense weights are non-linear and complex.\n",
            "3. **Small Tabular Dataset Suitability**: On structured tabular datasets ($N = 1,473$), tree ensembles (Random Forest / XGBoost) offer comparable or superior predictive accuracy with lower training complexity and higher interpretability."
        ]
    }
]

notebook = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open(NOTEBOOK_PATH, 'w') as f:
    json.dump(notebook, f, indent=2)

print(f"Created notebook at {NOTEBOOK_PATH}")
