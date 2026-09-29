import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Locate project folder
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# Load cleaned dataset
file_path = data_folder / "care_transition_clean.csv"
df = pd.read_csv(file_path)

# Clean column names
df.columns = df.columns.str.strip()

# Convert Date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Select all numerical categories except Date
columns = df.columns.drop("Date")

# Calculate total for each category
totals = {}

for col in columns:
    totals[col] = pd.to_numeric(df[col], errors="coerce").sum()

# Create chart
plt.figure(figsize=(12, 6))

plt.bar(totals.keys(), totals.values())

plt.title("Total Children by Care Transition Category")
plt.xlabel("Care Transition Category")
plt.ylabel("Total Number of Children")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save chart
output_path = project_folder / "charts" / "category_totals.png"
plt.savefig(output_path, dpi=300)

# Display chart
plt.show()

print("Category totals chart saved successfully:")
print(output_path)