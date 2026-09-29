import pandas as pd
from pathlib import Path

# Locate the dataset
project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "care_transition_raw.csv"

# Read the dataset
df = pd.read_csv(file_path)

# Convert Date column into proper date format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# 1. Dataset size
print("\n--- DATASET SIZE ---")
print("Rows and columns:", df.shape)

# 2. Column names
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

# 3. Data types
print("\n--- DATA TYPES ---")
print(df.dtypes)

# 4. Missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# 5. Duplicate records
print("\n--- DUPLICATE ROWS ---")
print("Duplicate rows:", df.duplicated().sum())

# 6. Duplicate dates
print("\n--- DUPLICATE DATES ---")
print("Duplicate dates:", df["Date"].duplicated().sum())

# 7. Date range
print("\n--- DATE RANGE ---")
print("Start date:", df["Date"].min())
print("End date:", df["Date"].max())

# 8. Statistical summary
print("\n--- STATISTICAL SUMMARY ---")
print(df.describe())

# 9. First 5 records
print("\n--- FIRST 5 RECORDS ---")
print(df.head())

# 10. Last 5 records
print("\n--- LAST 5 RECORDS ---")
print(df.tail())

print("\nDataset inspection completed!")