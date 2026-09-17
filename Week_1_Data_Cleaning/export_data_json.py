import pandas as pd
import json

df = pd.read_csv('/Users/bhagath/Desktop/AIO/Yuva_intern/HR_Analytics_Cleaned.csv')
# Select key columns for dashboard performance
records = df.to_dict(orient='records')

with open('/Users/bhagath/Desktop/AIO/Yuva_intern/hr_data.json', 'w') as f:
    json.dump(records, f)

print(f"Exported {len(records)} employee records to hr_data.json")
