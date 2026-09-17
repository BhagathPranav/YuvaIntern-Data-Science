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
└── Week_2_Data_Cleaning/
    ├── HR_Attrition_EDA_Report.docx        # Week 2 Executive EDA Report & Actionable Roadmap
    ├── notebook_Week2_EDA.ipynb            # Jupyter Notebook with Heatmaps, Boxplots & Distribution Analyses
    ├── eda_analysis.py                     # Automated Python EDA Data Extraction & Metric Calculations
    ├── eda_summary.json                    # Extracted Metrics & Heatmap Data for Visualizations
    ├── HR_Analytics_EDA_Dashboard.twb      # Native Tableau EDA Workbook File
    ├── HR_Analytics_EDA_Dashboard.twbx     # Packaged Tableau EDA Workbook (Embedded Dataset)
    ├── index.html                          # Interactive Glassmorphism Web EDA Dashboard
    ├── styles.css                          # Modern Cyberpunk/Glassmorphism Theme Styling
    ├── app.js                              # Interactive Correlation Matrix & Multi-Dimensional EDA Visuals
    ├── create_notebook.py                  # Jupyter Notebook Builder Script
    └── create_tableau_eda_workbook.py      # Tableau EDA XML & TWBX Builder Script
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

