# YuvaIntern-Data-Science

Repository for Yuva Internship Data Science projects and tasks.

## 📂 Repository Structure

```
.
└── Week_1_Data_Cleaning/
    ├── Bhagath_HR_Data_Cleaning.docx       # Data Cleaning & Preprocessing Report
    ├── notebooks_Yuva.ipynb                # Exploratory Data Analysis & Cleaning Notebook
    ├── clean_hr_data.py                    # Python Preprocessing Pipeline Script
    ├── HR_Analytics.csv                    # Raw HR Dataset (1,480 rows × 38 features)
    ├── HR_Analytics_Cleaned.csv            # Cleaned & Sanitized Dataset (1,473 rows × 35 features)
    ├── HR_Analytics_Dashboard.twb          # Native Tableau Workbook File
    ├── HR_Analytics_Dashboard.twbx         # Packaged Tableau Workbook (Embedded Data)
    ├── index.html                          # Interactive Tableau-Inspired Web Dashboard
    ├── styles.css                          # Glassmorphism Dark Theme Styling
    ├── app.js                              # Chart.js Visualizations & Multi-Filter Logic
    ├── hr_data.json                        # Preprocessed JSON Data for Web Dashboard
    ├── create_tableau_workbook.py          # Python Script Generating .twb File
    ├── create_twbx.py                      # Python Script Generating .twbx File
    └── export_data_json.py                 # Python Script Exporting JSON Data
```

## 🚀 Tasks Overview

### Week 1: Data Cleaning, Preprocessing & Tableau Dashboard
- **Median Imputation**: Imputed missing values in `YearsWithCurrManager`.
- **Dimensionality Reduction**: Removed zero-variance and non-predictive columns (`EmpID`, `AgeGroup`, `EmployeeNumber`, `Over18`, `EmployeeCount`, `StandardHours`).
- **Outlier Mitigation**: Applied 1.5 × IQR capping on `MonthlyIncome`.
- **Business Intelligence**: Constructed pre-packaged Tableau workbook (`.twbx`) and interactive web dashboard featuring Pie charts, Bar charts, Donut charts, Radar charts, and cross-filtering.
