# YuvaIntern-Data-Science

Repository for Yuva Internship Data Science projects and tasks.

## 📂 Repository Structure

```
.
├── Week_1_Data_Cleaning/
│   ├── Bhagath_HR_Data_Cleaning.docx       # Data Cleaning & Preprocessing Report
│   ├── notebooks_Yuva.ipynb                # Exploratory Data Analysis & Cleaning Notebook
│   ├── clean_hr_data.py                    # Python Preprocessing Pipeline Script
│   ├── HR_Analytics.csv                    # Raw HR Dataset (1,480 rows × 38 features)
│   ├── HR_Analytics_Cleaned.csv            # Cleaned & Sanitized Dataset (1,473 rows × 35 features)
│   ├── HR_Analytics_Dashboard.twb          # Native Tableau Workbook File
│   ├── HR_Analytics_Dashboard.twbx         # Packaged Tableau Workbook (Embedded Data)
│   ├── index.html                          # Interactive Tableau-Inspired Web Dashboard
│   ├── styles.css                          # Glassmorphism Dark Theme Styling
│   ├── app.js                              # Chart.js Visualizations & Multi-Filter Logic
│   ├── hr_data.json                        # Preprocessed JSON Data for Web Dashboard
│   ├── create_tableau_workbook.py          # Python Script Generating .twb File
│   ├── create_twbx.py                      # Python Script Generating .twbx File
│   └── export_data_json.py                 # Python Script Exporting JSON Data
│
├── Week_2_Data_Cleaning/
│   ├── HR_Attrition_EDA_Report.docx        # Week 2 Executive EDA Report & Actionable Roadmap
│   ├── notebook_Week2_EDA.ipynb            # Jupyter Notebook with Heatmaps, Boxplots & Distribution Analyses
│   ├── eda_analysis.py                     # Automated Python EDA Data Extraction & Metric Calculations
│   ├── eda_summary.json                    # Extracted Metrics & Heatmap Data for Visualizations
│   ├── HR_Analytics_EDA_Dashboard.twb      # Native Tableau EDA Workbook File
│   ├── HR_Analytics_EDA_Dashboard.twbx     # Packaged Tableau EDA Workbook (Embedded Dataset)
│   ├── index.html                          # Interactive Glassmorphism Web EDA Dashboard
│   ├── styles.css                          # Modern Cyberpunk/Glassmorphism Theme Styling
│   ├── app.js                              # Interactive Correlation Matrix & Multi-Dimensional EDA Visuals
│   ├── create_notebook.py                  # Jupyter Notebook Builder Script
│   └── create_tableau_eda_workbook.py      # Tableau EDA XML & TWBX Builder Script
│
├── Week_3_Data_Cleaning/
│   ├── HR_Clustering_Analysis.docx         # Executive Report on Unsupervised Clustering & Workforce Personas
│   ├── notebook_Week3_Clustering.ipynb     # Jupyter Notebook documenting StandardScaler, Elbow Curve, 2D PCA & Cluster Profiles
│   ├── clustering_analysis.py              # Automated Python Script executing K-Means Clustering & Exporting Clustered Dataset
│   ├── clustering_summary.json             # WCSS, Silhouette Scores & Persona Metrics for Web Visualizations
│   ├── HR_Analytics_Clustered.csv          # Preprocessed Dataset with Assigned Clusters, Personas & 2D PCA Coordinates
│   ├── HR_Analytics_Clustering_Dashboard.twb  # Native Tableau Clustering Workbook XML
│   ├── HR_Analytics_Clustering_Dashboard.twbx # Packaged Tableau Clustering Workbook (Embedded Data)
│   ├── index.html                          # Interactive Glassmorphism Web Clustering Dashboard
│   ├── styles.css                          # Cyberpunk Glassmorphism Dark Mode Styling
│   ├── app.js                              # Interactive Chart.js Elbow Curve, 2D PCA Scatter Plot & Directory Filters
│   ├── create_notebook.py                  # Generator Script for Jupyter Notebook
│   └── create_tableau_clustering_workbook.py # Builder Script for Tableau XML & TWBX Workbooks
│
└── Week_4_Data_Supervised/
    ├── HR_Supervised_Learning_Final.docx   # Executive Report on Supervised Attrition Classification & Algorithm Benchmarking
    ├── notebook_Week4_Supervised.ipynb     # Jupyter Notebook documenting Feature Engineering, Train/Test Split, 5-Fold CV & ROC Curves
    ├── supervised_analysis.py              # Automated Python ML Script executing Classification Pipeline & Metrics Export
    ├── supervised_summary.json             # Model Metrics, Confusion Matrices, ROC Data & Top Drivers for Web Dashboard
    ├── HR_Analytics_Supervised.csv         # Enriched Dataset with Predicted Flight Risk Scores & Risk Categories
    ├── HR_Analytics_Supervised_Dashboard.twb  # Native Tableau Supervised Learning Workbook XML
    ├── HR_Analytics_Supervised_Dashboard.twbx # Packaged Tableau Supervised Learning Workbook (Embedded Data)
    ├── index.html                          # Interactive Executive Cyberpunk Web Dashboard & Real-Time Flight Risk Simulator
    ├── styles.css                          # Cyberpunk Glassmorphism Dark Theme Styling
    ├── app.js                              # Chart.js Visualizations, Confusion Matrix Renderers & Interactive Simulator Logic
    ├── create_notebook.py                  # Generator Script for Jupyter Notebook
    └── create_tableau_supervised_workbook.py # Builder Script for Tableau XML & TWBX Workbooks
```

## 🚀 Tasks Overview

### Week 1: Data Cleaning, Preprocessing & Tableau Dashboard
- **Median Imputation**: Imputed missing values in `YearsWithCurrManager`.
- **Dimensionality Reduction**: Removed zero-variance and non-predictive columns (`EmpID`, `AgeGroup`, `EmployeeNumber`, `Over18`, `EmployeeCount`, `StandardHours`).
- **Outlier Mitigation**: Applied 1.5 × IQR capping on `MonthlyIncome`.
- **Business Intelligence**: Constructed pre-packaged Tableau workbook (`.twbx`) and interactive web dashboard featuring Pie charts, Bar charts, Donut charts, Radar charts, and cross-filtering.

### Week 2: Exploratory Data Analysis & Diagnostic Dashboards
- **Class Imbalance Audit**: Quantified 16.1% baseline turnover (237 Yes vs. 1,233 No).
- **Loyalty Penalty Diagnostics**: Identified significant correlation drop between total experience ($r = 0.77$) vs. tenure at company ($r = 0.51$), highlighting internal wage stagnation.
- **Departmental Risk Profile**: Isolated Sales (20.6% attrition) and Human Resources (19.0% attrition) as primary flight-risk departments.
- **Compensation Deficit Analysis**: Revealed a $2,130 median monthly salary deficit for departing staff ($3,200 vs. $5,330).
- **Multi-Platform Visualizations**: Generated Jupyter Notebook (`notebook_Week2_EDA.ipynb`), Tableau Packaged Dashboard (`HR_Analytics_EDA_Dashboard.twbx`), and interactive Web EDA Dashboard (`index.html`).

### Week 3: Workforce Segmentation & K-Means Clustering Analysis
- **StandardScaler Normalization**: Standardized numerical experience and compensation features to ensure unbiased Euclidean distance calculations.
- **Elbow Method & Silhouette Optimization**: Verified inflection point at $k=3$ (WCSS drop and optimal silhouette scores).
- **Workforce Persona Profiling**:
  - **Cluster 0 (Junior Core)**: 740 employees (50.2%), avg income $3,767, avg experience 6.2 yrs, highest attrition risk (**22.6%**).
  - **Cluster 1 (Mid-Level Professionals)**: 511 employees (34.7%), avg income $6,543, avg experience 12.4 yrs, turnover rate **10.8%**.
  - **Cluster 2 (Senior Leadership)**: 222 employees (15.1%), avg income $14,581, avg experience 25.7 yrs, turnover rate **6.8%**.
- **Dimensionality Reduction**: Applied 2D Principal Component Analysis (PCA) to map cluster separation.
- **Multi-Platform Visualizations**: Generated Jupyter Notebook (`notebook_Week3_Clustering.ipynb`), Tableau Packaged Dashboard (`HR_Analytics_Clustering_Dashboard.twbx`), and interactive Web Clustering Dashboard (`index.html`).

### Week 4: Supervised Learning — Predicting Employee Attrition & Early Warning System
- **Feature Engineering & One-Hot Encoding**: Transformed categorical features with `drop_first=True`, expanding the dataset to **45 mathematical features**.
- **Data Partitioning & Data Leakage Prevention**: Split into an 80/20 train-test split (`stratify=y`) and fit `StandardScaler` strictly on the training set.
- **Class Imbalance Mitigation (`class_weight='balanced'`)**: Applied inverse class weighting to penalize False Negatives on the 84/16 imbalanced target.
- **5-Fold Stratified Cross-Validation**:
  - **Logistic Regression (Parametric Benchmark)**: 5-Fold CV ROC-AUC of **0.7979**, Test ROC-AUC of **0.8854**, test set **Recall of 83%** (catches 39 out of 47 departing employees).
  - **Random Forest Classifier (Ensemble Method)**: 5-Fold CV ROC-AUC of **0.7796**, Test ROC-AUC of **0.8341**, test set **Precision of 70%** (16 True Positives, 7 False Positives).
- **Model Selection Verdict**: Selected Logistic Regression as the optimal early warning estimator because in HR attrition, a **False Negative** (losing an employee without intervention) is vastly more costly than a **False Positive** (a stay interview or bonus given to an employee planning to stay).
- **Interactive Web Flight Risk Simulator**: Built a dynamic real-time web flight risk calculator for HR managers to simulate flight risk scores and receive automated retention recommendations.
- **Multi-Platform Visualizations**: Generated Jupyter Notebook (`notebook_Week4_Supervised.ipynb`), Tableau Packaged Dashboard (`HR_Analytics_Supervised_Dashboard.twbx`), and interactive Web Dashboard (`index.html`).



