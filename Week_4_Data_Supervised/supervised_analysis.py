import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, roc_curve

def run_supervised_pipeline():
    print("Initializing Supervised Learning Pipeline for HR Attrition Prediction...")
    
    # 1. Load Cleaned Dataset
    base_dir = os.path.dirname(__file__)
    input_csv = os.path.join(base_dir, '..', 'Week_1_Data_Cleaning', 'HR_Analytics_Cleaned.csv')
    if not os.path.exists(input_csv):
        input_csv = os.path.join(base_dir, 'HR_Analytics_Cleaned.csv')
        
    df = pd.read_csv(input_csv)
    print(f"Loaded clean dataset shape: {df.shape}")

    # 2. Separate Target & Predictor Features
    target = (df['Attrition'] == 'Yes').astype(int)
    
    # Exclude non-predictive, redundant, or target leakage columns
    leakage_cols = [
        'Attrition', 'Attrition_Numeric', 'EmpID', 'EmployeeNumber', 
        'Over18', 'EmployeeCount', 'StandardHours', 'MonthlyIncome_Uncapped', 
        'SalarySlab', 'Age_Group', 'Tenure_Group'
    ]
    drop_list = [col for col in leakage_cols if col in df.columns]
    X_raw = df.drop(columns=drop_list)
    print(f"Initial raw predictor features: {X_raw.shape[1]}")

    # 3. One-Hot Encoding with drop_first=True
    X_encoded = pd.get_dummies(X_raw, drop_first=True)
    feature_names = list(X_encoded.columns)
    print(f"Engineered features after One-Hot Encoding: {len(feature_names)}")

    # 4. Stratified 80/20 Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, target, test_size=0.20, random_state=42, stratify=target
    )
    print(f"Train set: {X_train.shape[0]} samples | Test holdout set: {X_test.shape[0]} samples")

    # 5. Feature Scaling (StandardScaler fit strictly on train set)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    X_all_scaled = scaler.transform(X_encoded)

    # 6. Stratified 5-Fold Cross-Validation Setup
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # 7. Model 1: Logistic Regression (Parametric Benchmark)
    lr = LogisticRegression(solver='lbfgs', max_iter=1000, class_weight='balanced', random_state=42)
    lr_cv_scores = cross_val_score(lr, X_train_scaled, y_train, cv=skf, scoring='roc_auc')
    lr.fit(X_train_scaled, y_train)
    
    lr_preds = lr.predict(X_test_scaled)
    lr_probs = lr.predict_proba(X_test_scaled)[:, 1]
    lr_auc = float(roc_auc_score(y_test, lr_probs))
    lr_cm = confusion_matrix(y_test, lr_preds)
    
    # 8. Model 2: Random Forest Classifier (Non-Parametric Ensemble)
    rf = RandomForestClassifier(
        n_estimators=100, max_depth=10, min_samples_split=5, 
        min_samples_leaf=2, class_weight='balanced', random_state=42
    )
    rf_cv_scores = cross_val_score(rf, X_train, y_train, cv=skf, scoring='roc_auc')
    rf.fit(X_train, y_train)
    
    rf_preds = rf.predict(X_test)
    rf_probs = rf.predict_proba(X_test)[:, 1]
    rf_auc = float(roc_auc_score(y_test, rf_probs))
    rf_cm = confusion_matrix(y_test, rf_preds)

    # 9. Compute ROC Curves
    lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probs)
    rf_fpr, rf_tpr, _ = roc_curve(y_test, rf_probs)

    # Sample ROC points for crisp Chart.js visual rendering (15 downsampled points)
    indices_lr = np.linspace(0, len(lr_fpr) - 1, 15, dtype=int)
    indices_rf = np.linspace(0, len(rf_fpr) - 1, 15, dtype=int)

    roc_curve_data = {
        "logistic_regression": [
            {"fpr": float(round(lr_fpr[i], 4)), "tpr": float(round(lr_tpr[i], 4))} for i in indices_lr
        ],
        "random_forest": [
            {"fpr": float(round(rf_fpr[i], 4)), "tpr": float(round(rf_tpr[i], 4))} for i in indices_rf
        ]
    }

    # 10. Extract Feature Coefficients & Importances
    lr_coefs = pd.DataFrame({
        'feature': feature_names,
        'coefficient': lr.coef_[0]
    }).sort_values(by='coefficient', ascending=False)

    rf_importances = pd.DataFrame({
        'feature': feature_names,
        'importance': rf.feature_importances_
    }).sort_values(by='importance', ascending=False)

    top_lr_features = lr_coefs.head(10).to_dict(orient='records')
    top_rf_features = rf_importances.head(10).to_dict(orient='records')

    # Convert numpy data types for dict
    for item in top_lr_features:
        item['coefficient'] = float(round(item['coefficient'], 4))
    for item in top_rf_features:
        item['importance'] = float(round(item['importance'], 4))

    # 11. Full Dataset Predictions & Enriched Export
    df['FlightRiskScore_LR'] = np.round(lr.predict_proba(X_all_scaled)[:, 1], 4)
    df['FlightRiskScore_RF'] = np.round(rf.predict_proba(X_encoded)[:, 1], 4)
    df['Predicted_Attrition_LR'] = lr.predict(X_all_scaled)
    
    # Categorize Risk Levels based on Logistic Regression Probability
    def assign_risk_cat(score):
        if score >= 0.65:
            return 'High Risk'
        elif score >= 0.35:
            return 'Medium Risk'
        else:
            return 'Low Risk'

    df['Risk_Category'] = df['FlightRiskScore_LR'].apply(assign_risk_cat)

    output_csv = os.path.join(base_dir, 'HR_Analytics_Supervised.csv')
    df.to_csv(output_csv, index=False)
    print(f"Exported enriched dataset to: {output_csv}")

    # 12. Classification Reports Breakdown
    tn_lr, fp_lr, fn_lr, tp_lr = lr_cm.ravel()
    tn_rf, fp_rf, fn_rf, tp_rf = rf_cm.ravel()

    lr_recall = float(round(tp_lr / (tp_lr + fn_lr), 4))
    lr_precision = float(round(tp_lr / (tp_lr + fp_lr), 4))
    lr_f1 = float(round(2 * (lr_precision * lr_recall) / (lr_precision + lr_recall), 4))

    rf_recall = float(round(tp_rf / (tp_rf + fn_rf), 4))
    rf_precision = float(round(tp_rf / (tp_rf + fp_rf), 4))
    rf_f1 = float(round(2 * (rf_precision * rf_recall) / (rf_precision + rf_recall), 4))

    # Department Flight Risk Breakdown
    dept_risk = df.groupby('Department')['Risk_Category'].value_counts().unstack().fillna(0).to_dict(orient='index')
    dept_risk_clean = {}
    for d, counts in dept_risk.items():
        dept_risk_clean[d] = {k: int(v) for k, v in counts.items()}

    summary_data = {
        "dataset_summary": {
            "total_records": int(len(df)),
            "attrition_count": int(target.sum()),
            "attrition_rate": float(round(target.mean() * 100, 2)),
            "feature_count": len(feature_names),
            "train_samples": X_train.shape[0],
            "test_samples": X_test.shape[0]
        },
        "logistic_regression": {
            "model_name": "Logistic Regression (Parametric Benchmark)",
            "cv_roc_auc_mean": float(round(lr_cv_scores.mean(), 4)),
            "cv_roc_auc_std": float(round(lr_cv_scores.std(), 4)),
            "test_roc_auc": round(lr_auc, 4),
            "confusion_matrix": {
                "true_negatives": int(tn_lr),
                "false_positives": int(fp_lr),
                "false_negatives": int(fn_lr),
                "true_positives": int(tp_lr)
            },
            "metrics": {
                "precision": lr_precision,
                "recall": lr_recall,
                "f1_score": lr_f1,
                "accuracy": float(round((tp_lr + tn_lr) / len(y_test), 4))
            },
            "top_drivers": top_lr_features
        },
        "random_forest": {
            "model_name": "Random Forest Classifier (Ensemble Method)",
            "cv_roc_auc_mean": float(round(rf_cv_scores.mean(), 4)),
            "cv_roc_auc_std": float(round(rf_cv_scores.std(), 4)),
            "test_roc_auc": round(rf_auc, 4),
            "confusion_matrix": {
                "true_negatives": int(tn_rf),
                "false_positives": int(fp_rf),
                "false_negatives": int(fn_rf),
                "true_positives": int(tp_rf)
            },
            "metrics": {
                "precision": rf_precision,
                "recall": rf_recall,
                "f1_score": rf_f1,
                "accuracy": float(round((tp_rf + tn_rf) / len(y_test), 4))
            },
            "top_drivers": top_rf_features
        },
        "roc_curves": roc_curve_data,
        "risk_category_counts": {
            "High Risk": int((df['Risk_Category'] == 'High Risk').sum()),
            "Medium Risk": int((df['Risk_Category'] == 'Medium Risk').sum()),
            "Low Risk": int((df['Risk_Category'] == 'Low Risk').sum())
        },
        "department_risk_breakdown": dept_risk_clean,
        "sample_employees": df[['Age', 'Department', 'JobRole', 'MonthlyIncome', 'OverTime', 'YearsAtCompany', 'FlightRiskScore_LR', 'Risk_Category']].head(15).to_dict(orient='records')
    }

    summary_path = os.path.join(base_dir, 'supervised_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary_data, f, indent=2)
    print(f"Exported supervised summary JSON to: {summary_path}")

if __name__ == '__main__':
    run_supervised_pipeline()
