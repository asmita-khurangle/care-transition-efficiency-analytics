import pandas as pd
from pathlib import Path

# Locate project folders
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# Read the raw dataset
file_path = data_folder / "care_transition_raw.csv"
df = pd.read_csv(file_path)

print("Original dataset shape:", df.shape)

# 1. Clean column names
df.columns = df.columns.str.strip()

# 2. Remove duplicate records
df = df.drop_duplicates()

# 3. Clean the Date column
df["Date"] = pd.to_datetime(
    df["Date"], errors="coerce"
)

# Remove rows with invalid dates
df = df.dropna(subset=["Date"])

# 4. Convert numeric columns
for col in df.columns:
    if col != "Date":
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "", regex=False),
            errors="coerce"
        )

# 5. Sort records by date
df = df.sort_values("Date")

# 6. Save the cleaned dataset
output_path = data_folder / "care_transition_clean.csv"
df.to_csv(output_path, index=False)

print("Cleaned dataset shape:", df.shape)
print("Missing values:")
print(df.isnull().sum())

print("\nData cleaning completed!")
print("Cleaned file saved at:", output_path)