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
├── Week_4_Data_Supervised/
│   ├── HR_Supervised_Learning_Final.docx   # Executive Report on Supervised Attrition Classification & Algorithm Benchmarking
│   ├── notebook_Week4_Supervised.ipynb     # Jupyter Notebook documenting Feature Engineering, Train/Test Split, 5-Fold CV & ROC Curves
│   ├── supervised_analysis.py              # Automated Python ML Script executing Classification Pipeline & Metrics Export
│   ├── supervised_summary.json             # Model Metrics, Confusion Matrices, ROC Data & Top Drivers for Web Dashboard
│   ├── HR_Analytics_Supervised.csv         # Enriched Dataset with Predicted Flight Risk Scores & Risk Categories
│   ├── HR_Analytics_Supervised_Dashboard.twb  # Native Tableau Supervised Learning Workbook XML
│   ├── HR_Analytics_Supervised_Dashboard.twbx # Packaged Tableau Supervised Learning Workbook (Embedded Data)
│   ├── index.html                          # Interactive Executive Cyberpunk Web Dashboard & Real-Time Flight Risk Simulator
│   ├── styles.css                          # Cyberpunk Glassmorphism Dark Theme Styling
│   ├── app.js                              # Chart.js Visualizations, Confusion Matrix Renderers & Interactive Simulator Logic
│   ├── create_notebook.py                  # Generator Script for Jupyter Notebook
│   └── create_tableau_supervised_workbook.py # Builder Script for Tableau XML & TWBX Workbooks
│
├── Week_5_Data_Deep_Learning_HR/
│   ├── Deep_Learning_HR.docx               # Executive Report on Artificial Neural Networks (ANN) for HR Attrition
│   ├── notebook_Week5_Deep_Learning.ipynb   # Jupyter Notebook documenting PyTorch Sequential ANN, Loss Trajectory & Early Stopping
│   ├── deep_learning_analysis.py           # Automated PyTorch ML Script executing ANN Training, Early Stopping & Metrics Export
│   ├── deep_learning_summary.json          # Training Epoch Trajectory, Loss Curves, Confusion Matrix & Metrics JSON
│   ├── figures/
│   │   ├── loss_trajectory.png             # Training & Validation BCE Loss / Validation ROC-AUC Trajectory Plot
│   │   └── confusion_matrix.png            # Heatmap Visualization of ANN Confusion Matrix
│   ├── index.html                          # Interactive Glassmorphism Web Dashboard & Real-Time ANN Risk Simulator
│   ├── styles.css                          # Modern Cyberpunk/Glassmorphic Theme Styling
│   ├── app.js                              # Chart.js Training Trajectory Chart & Dynamic Neural Network Risk Simulator
│   └── create_notebook.py                  # Generator Script for Jupyter Notebook
│
└── Week_6/
    ├── Bhagath_Capstone_HR_Pipeline.docx    # Integrative Capstone Project Executive Report & Pipeline Documentation
    ├── HR_Clustering_Analysis.pages        # Capstone Analytics Documentation File
    ├── HR_Analytics_Capstone.csv           # Processed Capstone Dataset with Encoded Features & Cluster Assignments
    ├── capstone_pipeline.py                # End-to-End Automated Data Science Pipeline Script
    ├── capstone_summary.json               # End-to-End Metrics, Benchmark Scores & Cluster Profiles JSON
    ├── notebook_Week6_Capstone.ipynb       # Integrative Capstone Jupyter Notebook covering Preprocessing to Deep Learning
    ├── create_notebook.py                  # Generator Script for Capstone Jupyter Notebook
    ├── create_tableau_capstone_workbook.py # Builder Script for Capstone Tableau XML & TWBX Workbooks
    ├── HR_Analytics_Capstone_Dashboard.twb # Native Tableau Capstone Dashboard XML
    ├── HR_Analytics_Capstone_Dashboard.twbx# Packaged Tableau Capstone Dashboard (Embedded Dataset)
    ├── index.html                          # Interactive Glassmorphism Capstone Web Dashboard & Real-Time Risk Simulator
    ├── styles.css                          # Modern Glassmorphic Dark Theme Styling
    ├── app.js                              # Interactive Tab Management, Department Charts & Real-Time Flight Risk Calculator
    └── figures/
        ├── eda_overview.png                # EDA Overview Visualizations
        ├── kmeans_clusters.png             # K-Means Employee Persona Cluster Scatter Plot
        └── roc_comparison.png              # Logistic Regression vs PyTorch ANN ROC-AUC Curves Plot
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

### Week 5: Deep Learning — Artificial Neural Network (ANN) HR Attrition Classifier & Trade-off Analysis
- **Neural Network Architecture Topology**: Constructed a Sequential Multi-Layer Perceptron (MLP) within PyTorch/Keras mapping 56 input features through two hidden layers ($h_1 = 64$ neurons with `ReLU` & DropOut $0.3$, $h_2 = 32$ neurons with `ReLU` & DropOut $0.2$) to a single `Sigmoid` output neuron.
- **Optimization & Loss Minimization**: Utilized the Adam optimizer ($\eta = 0.001$) and Binary Cross-Entropy Loss ($L = -\frac{1}{N} \sum [y_i \log(\hat{y}_i) + (1-y_i) \log(1-\hat{y}_i)]$).
- **Dynamic Class Weighting & Overfitting Mitigation**: Implemented dynamic positive class weighting ($\text{pos\_weight} \approx 5.20$) to address the 84/16 class imbalance alongside an `EarlyStopping` callback (patience = 15 epochs monitoring `val_loss`), restoring optimal weights from Epoch 8 (Best Val Loss: `0.7375`).
- **Empirical Model Performance**:
  - **ROC-AUC Score**: **`0.8519`** (~85.2% discriminative capacity).
  - **Attrited Recall (Sensitivity)**: **`0.7234`** (**72.34%** — successfully isolated 34 out of 47 departing employees in unseen test holdout).
  - **Attrited Precision**: **`0.5152`** (51.52% — expected precision trade-off prioritization of recall).
  - **Confusion Matrix ($N=295$)**: 216 True Negatives, 32 False Positives, 13 False Negatives, 34 True Positives.
- **Strategic Trade-off & Interpretability Analysis**: Evaluated the "Black Box" interpretability trade-off of neural networks against linear models (Logistic Regression) and tree ensembles (Random Forest / XGBoost) on small structured tabular datasets.
- **Multi-Platform Visualizations & Interactive Simulator**: Generated Jupyter Notebook (`notebook_Week5_Deep_Learning.ipynb`), updated Word executive report (`Deep_Learning_HR.docx`), and built an interactive web dashboard (`index.html`) featuring real-time neural network forward-pass risk simulation.

### Week 6: Integrative Capstone Project — End-to-End HR Attrition Analytics Pipeline
- **End-to-End Data Science Pipeline**: Integrated all 5 project phases (Data Preprocessing, EDA & Loyalty Penalty, Unsupervised K-Means Clustering, Supervised & Deep Learning, Executive Business Intelligence) into a unified, reproducible pipeline script (`capstone_pipeline.py`).
- **Loyalty Penalty Ratio**: Formally quantified the compensation penalty gap ($1.50\times$), demonstrating that external market hiring offers higher salary growth ($r = 0.77$) than internal company tenure ($r = 0.51$).
- **Unsupervised Workforce Segmentation ($k=3$)**: Segmented the cohort into *Junior Core* (44.13% size, 23.08% turnover), *Mid-Level Professionals* (16.29% size, 7.50% turnover), and *Senior Leadership* (39.58% size, 11.84% turnover).
- **Model Benchmarking**: Benchmarked Logistic Regression (Parametric Baseline, **ROC-AUC: 0.8914**, **Recall: 89.36%**) against PyTorch Deep Learning ANN (**ROC-AUC: 0.8942**, **Recall: 87.23%**, **F1: 0.6119**).
- **Multi-Platform Deliverables**: Delivered the full suite including executive DOCX report (`Bhagath_Capstone_HR_Pipeline.docx`), automated Jupyter Notebook (`notebook_Week6_Capstone.ipynb`), Tableau Capstone Workbook & Packaged Dashboard (`HR_Analytics_Capstone_Dashboard.twbx`), and interactive glassmorphism Web Application (`index.html`).

