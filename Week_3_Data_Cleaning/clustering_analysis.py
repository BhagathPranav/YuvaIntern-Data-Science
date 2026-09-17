import os
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

def run_clustering_pipeline():
    # 1. Load Cleaned Dataset
    input_path = os.path.join(os.path.dirname(__file__), '..', 'Week_1_Data_Cleaning', 'HR_Analytics_Cleaned.csv')
    if not os.path.exists(input_path):
        input_path = os.path.join(os.path.dirname(__file__), 'HR_Analytics_Cleaned.csv')
    
    df = pd.read_csv(input_path)
    print(f"Loaded dataset with shape: {df.shape}")

    # 2. Select Numerical Features for K-Means Clustering
    features = [
        'Age', 'TotalWorkingYears', 'MonthlyIncome', 
        'YearsAtCompany', 'YearsWithCurrManager', 
        'JobLevel', 'DistanceFromHome'
    ]
    
    X = df[features].copy()

    # 3. Standardize Features (StandardScaler)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. Compute Elbow Curve (WCSS for k=1..10)
    wcss = []
    for k in range(1, 11):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        wcss.append(float(km.inertia_))

    # 5. Compute Silhouette Scores for k=2..6
    silhouette_scores = {}
    for k in range(2, 7):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        score = float(silhouette_score(X_scaled, labels))
        silhouette_scores[str(k)] = round(score, 4)

    # 6. Fit K-Means with Optimal k=3
    optimal_k = 3
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_scaled)

    # Sort cluster IDs by mean MonthlyIncome to ensure consistent Persona Mapping:
    # Cluster 0: Junior Core (lowest income)
    # Cluster 1: Mid-Level Professionals (medium income)
    # Cluster 2: Senior Leadership (highest income)
    cluster_income_order = df.groupby('Cluster')['MonthlyIncome'].mean().sort_values().index.tolist()
    cluster_mapping = {old_id: new_id for new_id, old_id in enumerate(cluster_income_order)}
    df['Cluster'] = df['Cluster'].map(cluster_mapping)

    persona_names = {
        0: 'Junior Core',
        1: 'Mid-Level Professionals',
        2: 'Senior Leadership'
    }
    df['Persona'] = df['Cluster'].map(persona_names)

    # 7. Apply 2D PCA for Visualization
    pca = PCA(n_components=2, random_state=42)
    pca_coords = pca.fit_transform(X_scaled)
    df['PCA1'] = np.round(pca_coords[:, 0], 4)
    df['PCA2'] = np.round(pca_coords[:, 1], 4)

    # 8. Save Clustered Dataset
    output_csv = os.path.join(os.path.dirname(__file__), 'HR_Analytics_Clustered.csv')
    df.to_csv(output_csv, index=False)
    print(f"Exported clustered dataset to: {output_csv}")

    # 9. Compute Cluster Summaries & Statistics
    cluster_stats = {}
    total_count = len(df)
    
    for c_id in range(optimal_k):
        sub = df[df['Cluster'] == c_id]
        persona = persona_names[c_id]
        
        attrition_count = int((sub['Attrition'] == 'Yes').sum())
        attrition_rate = float(round((attrition_count / len(sub)) * 100, 2))
        
        cluster_stats[str(c_id)] = {
            "cluster_id": c_id,
            "persona": persona,
            "count": int(len(sub)),
            "percentage": float(round((len(sub) / total_count) * 100, 2)),
            "attrition_count": attrition_count,
            "attrition_rate": attrition_rate,
            "mean_monthly_income": float(round(sub['MonthlyIncome'].mean(), 2)),
            "mean_total_working_years": float(round(sub['TotalWorkingYears'].mean(), 2)),
            "mean_years_at_company": float(round(sub['YearsAtCompany'].mean(), 2)),
            "mean_age": float(round(sub['Age'].mean(), 2)),
            "mean_job_level": float(round(sub['JobLevel'].mean(), 2)),
            "mean_distance_from_home": float(round(sub['DistanceFromHome'].mean(), 2))
        }

    # Department breakdown per cluster
    dept_breakdown = {}
    for c_id in range(optimal_k):
        sub = df[df['Cluster'] == c_id]
        dept_counts = sub['Department'].value_counts().to_dict()
        dept_breakdown[persona_names[c_id]] = {k: int(v) for k, v in dept_counts.items()}

    # Sample scatter data for Web Dashboard (first 300 points for crisp chart rendering)
    scatter_sample = df[['Age', 'TotalWorkingYears', 'MonthlyIncome', 'YearsAtCompany', 'Cluster', 'Persona', 'Attrition', 'PCA1', 'PCA2', 'Department', 'JobRole']].head(400).to_dict(orient='records')

    summary_data = {
        "total_employees": total_count,
        "overall_attrition_rate": float(round((df['Attrition'] == 'Yes').mean() * 100, 2)),
        "features_used": features,
        "elbow_curve": [{"k": i+1, "wcss": round(wcss[i], 2)} for i in range(10)],
        "silhouette_scores": silhouette_scores,
        "cluster_stats": cluster_stats,
        "department_breakdown": dept_breakdown,
        "scatter_sample": scatter_sample
    }

    summary_json_path = os.path.join(os.path.dirname(__file__), 'clustering_summary.json')
    with open(summary_json_path, 'w') as f:
        json.dump(summary_data, f, indent=2)
    print(f"Exported clustering summary JSON to: {summary_json_path}")

if __name__ == '__main__':
    run_clustering_pipeline()
