import pandas as pd
from pathlib import Path

# 1. Locate the project folder
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# 2. Load the cleaned dataset
file_path = data_folder / "care_transition_clean.csv"
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

print(df.columns.tolist())

# Convert Date to datetime format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Sort data by date
df = df.sort_values("Date")

print("\n====================================")
print("   CARE TRANSITION DATA ANALYSIS")
print("====================================")

# 3. Display dataset information
print("\n--- DATASET INFORMATION ---")
print("Total records:", len(df))
print("Start date:", df["Date"].min())
print("End date:", df["Date"].max())

# 4. Calculate total children across each category
print("\n--- TOTAL CHILDREN ---")

columns = df.columns.drop("Date").tolist()

for col in columns:
    if col in df.columns:
        print(f"{col}: {df[col].sum():,.0f}")

# 5. Calculate average daily values
print("\n--- AVERAGE DAILY VALUES ---")

for col in columns:
    if col in df.columns:
        print(f"{col}: {df[col].mean():,.2f}")

# 6. Calculate total transfers
if "Children transferred out of CBP custody" in df.columns:
    total_transfers = df[
        "Children transferred out of CBP custody"
    ].sum()

    print("\n--- TRANSFER ANALYSIS ---")
    print("Total transfers:", f"{total_transfers:,.0f}")

# 7. Calculate transfer rate
if (
    "Children apprehended and placed in CBP custody" in df.columns
    and "Children transferred out of CBP custody" in df.columns
):
    total_placed = df[
        "Children apprehended and placed in CBP custody"
    ].sum()

    if total_placed > 0:
        transfer_rate = (total_transfers / total_placed) * 100
        print("Transfer-to-placement ratio:", f"{transfer_rate:.2f}%")
    else:
        print("Transfer-to-placement ratio: Not available")

# 8. Calculate total children discharged from HHS care
if "Children discharged from HHS Care" in df.columns:
    total_discharged = df[
        "Children discharged from HHS Care"
    ].sum()

    print("\n--- DISCHARGE ANALYSIS ---")
    print("Total children discharged:", f"{total_discharged:,.0f}")

# 9. Calculate monthly summary
print("\n--- MONTHLY SUMMARY ---")

monthly = df.set_index("Date")[columns].resample("MS").sum()

print(monthly)

# Save monthly summary
monthly_path = data_folder / "monthly_summary.csv"
monthly.to_csv(monthly_path)

# 10. Save KPI summary
kpi_data = {
    "Metric": [],
    "Value": []
}

for col in columns:
    if col in df.columns:
        kpi_data["Metric"].append(col)
        kpi_data["Value"].append(df[col].sum())

kpi_df = pd.DataFrame(kpi_data)

kpi_path = data_folder / "kpi_summary.csv"
kpi_df.to_csv(kpi_path, index=False)

print("\n====================================")
print("DATA ANALYSIS COMPLETED!")
print("====================================")
print("Monthly summary saved:", monthly_path)
print("KPI summary saved:", kpi_path)