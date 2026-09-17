import pandas as pd
import numpy as np
import os

def clean_hr_data(input_path, output_path):
    print(f"Loading raw data from: {input_path}")
    df = pd.read_csv(input_path)
    print(f"Initial shape: {df.shape}")

    # 1. Check & impute missing values in YearsWithCurrManager with median
    missing_before = df['YearsWithCurrManager'].isnull().sum()
    median_tenure = df['YearsWithCurrManager'].median()
    df['YearsWithCurrManager'] = df['YearsWithCurrManager'].fillna(median_tenure)
    print(f"Imputed {missing_before} missing values in 'YearsWithCurrManager' with median ({median_tenure})")

    # 2. Drop duplicates
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    dropped_dups = initial_rows - len(df)
    print(f"Dropped {dropped_dups} duplicate rows")

    # Save original MonthlyIncome before capping for comparison
    df['MonthlyIncome_Uncapped'] = df['MonthlyIncome'].copy()

    # 3. IQR capping on MonthlyIncome
    Q1 = df['MonthlyIncome'].quantile(0.25)
    Q3 = df['MonthlyIncome'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df['MonthlyIncome'] = df['MonthlyIncome'].clip(lower_bound, upper_bound)
    print(f"MonthlyIncome capped between {lower_bound:.2f} and {upper_bound:.2f}")

    # 4. Drop zero-variance & non-predictive columns
    cols_to_drop = ['EmpID', 'AgeGroup', 'EmployeeNumber', 'Over18', 'EmployeeCount', 'StandardHours']
    existing_cols_to_drop = [c for c in cols_to_drop if c in df.columns]
    df.drop(columns=existing_cols_to_drop, inplace=True)
    print(f"Dropped columns: {existing_cols_to_drop}")

    # 5. Add Tableau Helper Features
    df['Attrition_Numeric'] = df['Attrition'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
    
    # Age Group Binning
    bins_age = [17, 25, 35, 45, 55, 100]
    labels_age = ['18-25', '26-35', '36-45', '46-55', '55+']
    df['Age_Group'] = pd.cut(df['Age'], bins=bins_age, labels=labels_age)

    # Years at Company Group
    bins_tenure = [-1, 2, 5, 10, 20, 100]
    labels_tenure = ['0-2 Yrs', '3-5 Yrs', '6-10 Yrs', '11-20 Yrs', '20+ Yrs']
    df['Tenure_Group'] = pd.cut(df['YearsAtCompany'], bins=bins_tenure, labels=labels_tenure)

    # Save cleaned dataframe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Successfully exported cleaned data to: {output_path}")
    print(f"Final shape: {df.shape}")
    return df

if __name__ == "__main__":
    input_file = "/Users/bhagath/Desktop/AIO/DATASETS/HR_Analytics.csv"
    output_file = "/Users/bhagath/Desktop/AIO/Yuva_intern/HR_Analytics_Cleaned.csv"
    clean_hr_data(input_file, output_file)
