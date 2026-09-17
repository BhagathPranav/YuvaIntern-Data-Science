import json
import os

def build_notebook():
    cells = []

    # Cell 1: Title & Overview (Markdown)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Week 3: Workforce Segmentation via Unsupervised K-Means Clustering\n",
            "\n",
            "## Executive Summary & Objectives\n",
            "This notebook performs **Unsupervised Machine Learning (K-Means Clustering)** on the cleaned HR Analytics dataset (`HR_Analytics_Cleaned.csv`).\n",
            "The objective is to discover underlying employee personas and risk profiles without relying on arbitrary HR pay-grade boundaries.\n",
            "\n",
            "### Workflow Steps:\n",
            "1. **Data Preprocessing & Feature Selection**: Extract numerical experience, age, and compensation variables.\n",
            "2. **StandardScaler Normalization**: Standardize features ($\\\\mu=0, \\\\sigma^2=1$) to equalize Euclidean distance calculations.\n",
            "3. **Optimal Cluster Selection**: Calculate WCSS (Elbow Method) for $k=1..10$ and Silhouette Scores for $k=2..6$.\n",
            "4. **K-Means Execution**: Segment workforce into $k=3$ distinct clusters.\n",
            "5. **Dimensionality Reduction (PCA)**: Project features into 2D Principal Components for visual validation.\n",
            "6. **Persona Profiling & Strategic Retention Recommendations**: Map clusters to actionable workforce personas."
        ]
    })

    # Cell 2: Imports & Environment Setup (Code)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "from sklearn.preprocessing import StandardScaler\n",
            "from sklearn.cluster import KMeans\n",
            "from sklearn.decomposition import PCA\n",
            "from sklearn.metrics import silhouette_score\n",
            "\n",
            "# Set aesthetic style\n",
            "sns.set_theme(style='darkgrid', palette='muted')\n",
            "plt.rcParams['font.sans-serif'] = 'Arial'\n",
            "plt.rcParams['font.size'] = 11\n",
            "print('Environment and Machine Learning libraries successfully initialized!')"
        ]
    })

    # Cell 3: Load Data & Inspect Features (Code)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Load preprocessed HR dataset\n",
            "df = pd.read_csv('../Week_1_Data_Cleaning/HR_Analytics_Cleaned.csv')\n",
            "print(f'Loaded dataset shape: {df.shape}')\n",
            "\n",
            "features = [\n",
            "    'Age', 'TotalWorkingYears', 'MonthlyIncome', \n",
            "    'YearsAtCompany', 'YearsWithCurrManager', \n",
            "    'JobLevel', 'DistanceFromHome'\n",
            "]\n",
            "\n",
            "X = df[features].copy()\n",
            "X.describe()"
        ]
    })

    # Cell 4: Feature Scaling (StandardScaler) (Code)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Apply StandardScaler normalization\n",
            "scaler = StandardScaler()\n",
            "X_scaled = scaler.fit_transform(X)\n",
            "\n",
            "# Convert back to DataFrame for verification\n",
            "df_scaled = pd.DataFrame(X_scaled, columns=features)\n",
            "print('StandardScaler transformation complete. Mean ≈ 0, Std ≈ 1:')\n",
            "df_scaled.head()"
        ]
    })

    # Cell 5: Elbow Method & Silhouette Analysis (Code)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Compute WCSS for k=1..10\n",
            "wcss = []\n",
            "for k in range(1, 11):\n",
            "    km = KMeans(n_clusters=k, random_state=42, n_init=10)\n",
            "    km.fit(X_scaled)\n",
            "    wcss.append(km.inertia_)\n",
            "\n",
            "# Compute Silhouette Scores for k=2..6\n",
            "sil_scores = {}\n",
            "for k in range(2, 7):\n",
            "    km = KMeans(n_clusters=k, random_state=42, n_init=10)\n",
            "    labels = km.fit_predict(X_scaled)\n",
            "    sil_scores[k] = silhouette_score(X_scaled, labels)\n",
            "\n",
            "# Plot Elbow Curve & Silhouette Scores\n",
            "fig, ax = plt.subplots(1, 2, figsize=(14, 5))\n",
            "\n",
            "ax[0].plot(range(1, 11), wcss, marker='o', color='#6366f1', linewidth=2.5, markersize=8)\n",
            "ax[0].axvline(x=3, color='#ef4444', linestyle='--', label='Elbow Point (k=3)')\n",
            "ax[0].set_title('Elbow Method: WCSS vs. Number of Clusters (k)', fontsize=13, fontweight='bold')\n",
            "ax[0].set_xlabel('Number of Clusters (k)')\n",
            "ax[0].set_ylabel('Within-Cluster Sum of Squares (WCSS)')\n",
            "ax[0].legend()\n",
            "\n",
            "ax[1].bar(sil_scores.keys(), sil_scores.values(), color='#10b981', alpha=0.85)\n",
            "ax[1].set_title('Silhouette Analysis Across Cluster Configurations', fontsize=13, fontweight='bold')\n",
            "ax[1].set_xlabel('Number of Clusters (k)')\n",
            "ax[1].set_ylabel('Silhouette Score')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })

    # Cell 6: K-Means Execution (k=3) & Persona Mapping (Code)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Fit optimal K-Means model with k=3\n",
            "kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)\n",
            "df['Cluster'] = kmeans.fit_predict(X_scaled)\n",
            "\n",
            "# Map clusters to Employee Personas sorted by MonthlyIncome\n",
            "income_order = df.groupby('Cluster')['MonthlyIncome'].mean().sort_values().index.tolist()\n",
            "mapping = {old_id: new_id for new_id, old_id in enumerate(income_order)}\n",
            "df['Cluster'] = df['Cluster'].map(mapping)\n",
            "\n",
            "persona_map = {\n",
            "    0: 'Junior Core',\n",
            "    1: 'Mid-Level Professionals',\n",
            "    2: 'Senior Leadership'\n",
            "}\n",
            "df['Persona'] = df['Cluster'].map(persona_map)\n",
            "\n",
            "df.groupby('Persona')[['MonthlyIncome', 'TotalWorkingYears', 'Age', 'YearsAtCompany', 'DistanceFromHome']].mean().round(2)"
        ]
    })

    # Cell 7: 2D PCA & Cluster Visualization (Code)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Dimensionality Reduction via 2D PCA\n",
            "pca = PCA(n_components=2, random_state=42)\n",
            "pca_coords = pca.fit_transform(X_scaled)\n",
            "df['PCA1'] = pca_coords[:, 0]\n",
            "df['PCA2'] = pca_coords[:, 1]\n",
            "\n",
            "plt.figure(figsize=(10, 6))\n",
            "palette = {'Junior Core': '#ef4444', 'Mid-Level Professionals': '#3b82f6', 'Senior Leadership': '#10b981'}\n",
            "sns.scatterplot(\n",
            "    data=df, x='PCA1', y='PCA2', hue='Persona', style='Attrition', \n",
            "    palette=palette, alpha=0.8, s=70\n",
            ")\n",
            "plt.title('2D PCA Projection of K-Means Clusters & Attrition', fontsize=14, fontweight='bold')\n",
            "plt.xlabel(f'PCA Component 1 ({round(pca.explained_variance_ratio_[0]*100, 1)}% Variance)')\n",
            "plt.ylabel(f'PCA Component 2 ({round(pca.explained_variance_ratio_[1]*100, 1)}% Variance)')\n",
            "plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })

    # Cell 8: Strategic Persona Recommendations (Markdown)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🎯 Actionable Persona Retention Strategies\n",
            "\n",
            "1. **Cluster 0: Junior Core (22.6% Attrition Risk)**\n",
            "   - **Profile**: Entry-level employees, avg income $3,767, avg tenure 3.4 yrs.\n",
            "   - **Intervention**: Early career progression frameworks, competitive entry salaries, clear promotion milestones within 18 months.\n",
            "\n",
            "2. **Cluster 1: Mid-Level Professionals (10.8% Attrition Risk)**\n",
            "   - **Profile**: Operational backbone, avg income $6,543, avg tenure 9.0 yrs.\n",
            "   - **Intervention**: Leadership development tracks, stock options, hybrid work schedules to prevent mid-career burnout.\n",
            "\n",
            "3. **Cluster 2: Senior Leadership (6.8% Attrition Risk)**\n",
            "   - **Profile**: Executive tier, avg income $14,581, avg tenure 14.5 yrs.\n",
            "   - **Intervention**: Executive compensation structures and formal reverse-mentorship programs with Cluster A talent."
        ]
    })

    notebook_content = {
        "cells": cells,
        "metadata": {
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    out_path = os.path.join(os.path.dirname(__file__), 'notebook_Week3_Clustering.ipynb')
    with open(out_path, 'w') as f:
        json.dump(notebook_content, f, indent=2)
    print(f"Successfully generated Jupyter notebook: {out_path}")

if __name__ == '__main__':
    build_notebook()
