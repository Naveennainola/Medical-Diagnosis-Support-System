import pandas as pd

df = pd.read_csv('C:/Users/Sai Kumar/OneDrive/Desktop/healthcare_assistant/assistant/dataset/disease_medications_final.csv')
df_columns = ['Disease', 'Medications', 'Time-based guidance and preventive measures']

print("Columns: ", df_columns)
# Preview
for index, row in df.iterrows():
    print(f"\n--- Entry {index+1} ---")
    print(f"Disease: {row['Disease']}")

    medic = [med.strip() for med in str(row['Medications']).split(';')]
    print("Medications:")
    for med in medic:
        print(f"  - {med}")
    
    guide = [point.strip() for point in str(row['Time-Based Guidance  and Preventive Measures']).split(';')]
    print("Time-based guidance and preventive measures:")
    for point in guide:
        print(f"  - {point}")