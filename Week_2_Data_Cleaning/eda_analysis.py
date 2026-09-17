import pandas as pd
import numpy as np
import json
import os

def perform_eda():
    data_path = "/Users/bhagath/Desktop/AIO/Yuva_intern/Week_1_Data_Cleaning/HR_Analytics_Cleaned.csv"
    if not os.path.exists(data_path):
        data_path = "/Users/bhagath/Desktop/AIO/DATASETS/HR_Analytics.csv"
    
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)

    # 1. Attrition Class Imbalance
    if 'Attrition_Numeric' not in df.columns:
        df['Attrition_Numeric'] = df['Attrition'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)

    total_count = len(df)
    attrition_count = int(df['Attrition_Numeric'].sum())
    retained_count = total_count - attrition_count
    attrition_rate = round((attrition_count / total_count) * 100, 2)

    # 2. Correlation Analysis
    num_cols = ['Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EnvironmentSatisfaction',
                'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobSatisfaction', 'MonthlyIncome',
                'NumCompaniesWorked', 'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction',
                'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
                'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager',
                'Attrition_Numeric']
    
    available_num_cols = [c for c in num_cols if c in df.columns]
    corr_matrix = df[available_num_cols].corr().round(3).to_dict()

    # 3. Loyalty Penalty Calculation
    # Correlation between MonthlyIncome & TotalWorkingYears vs MonthlyIncome & YearsAtCompany
    corr_work_years = df['MonthlyIncome'].corr(df['TotalWorkingYears'])
    corr_company_years = df['MonthlyIncome'].corr(df['YearsAtCompany'])
    loyalty_penalty_gap = round(corr_work_years - corr_company_years, 3)

    # Median Income by Attrition
    income_retained = float(df[df['Attrition_Numeric'] == 0]['MonthlyIncome'].median())
    income_attrition = float(df[df['Attrition_Numeric'] == 1]['MonthlyIncome'].median())
    income_gap = round(income_retained - income_attrition, 2)

    # 4. Department Attrition Rates
    dept_stats = df.groupby('Department')['Attrition_Numeric'].agg(['count', 'sum', 'mean']).reset_index()
    dept_list = []
    for _, row in dept_stats.iterrows():
        dept_list.append({
            "department": row['Department'],
            "total": int(row['count']),
            "attrition": int(row['sum']),
            "rate": round(row['mean'] * 100, 2)
        })

    # Export EDA Summary JSON
    eda_summary = {
        "metrics": {
            "total_count": total_count,
            "attrition_count": attrition_count,
            "retained_count": retained_count,
            "attrition_rate": attrition_rate,
            "loyalty_penalty_gap": loyalty_penalty_gap,
            "corr_work_years": round(corr_work_years, 3),
            "corr_company_years": round(corr_company_years, 3),
            "income_retained_median": income_retained,
            "income_attrition_median": income_attrition,
            "income_gap": income_gap
        },
        "department_stats": dept_list,
        "correlations": corr_matrix,
        "sample_records": df[['JobRole', 'Department', 'Age', 'Gender', 'MonthlyIncome', 'TotalWorkingYears', 'YearsAtCompany', 'YearsSinceLastPromotion', 'OverTime', 'Attrition', 'Attrition_Numeric']].head(50).to_dict(orient='records')
    }

    out_json = "/Users/bhagath/Desktop/AIO/Yuva_intern/Week_2_Data_Cleaning/eda_summary.json"
    with open(out_json, 'w') as f:
        json.dump(eda_summary, f, indent=2)

    print(f"EDA Summary successfully exported to {out_json}")
    print(f"Class Imbalance: {attrition_rate}% Attrition ({attrition_count}/{total_count})")
    print(f"Loyalty Penalty Gap (Total Working Yrs Corr {corr_work_years:.2f} - Company Yrs Corr {corr_company_years:.2f}): {loyalty_penalty_gap:.3f}")
    return eda_summary

if __name__ == "__main__":
    perform_eda()
