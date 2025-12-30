import pandas as pd
import os

RAW_DATA_PATH = "data/raw/Autism_Screening_Data_Combined.csv"

def extract_raw_data():
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError("CSV file not found")

    df = pd.read_csv(RAW_DATA_PATH)

    print("Raw Autism Screening Data Loaded")
    print("Shape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nSample records:")
    print(df.head())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nData types:")
    print(df.dtypes)

    return df

if __name__ == "__main__":
    extract_raw_data()
