import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Locate project folder
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# Load KPI summary
file_path = data_folder / "kpi_summary.csv"
df = pd.read_csv(file_path)

# Clean column names
df.columns = df.columns.str.strip()

print("KPI Summary:")
print(df)

# Convert the KPI table into a simple chart
# First column = KPI names, second column = KPI values
kpi_names = df.iloc[:, 0].astype(str)
kpi_values = pd.to_numeric(df.iloc[:, 1], errors="coerce")

# Create chart
plt.figure(figsize=(12, 6))

plt.bar(kpi_names, kpi_values)

plt.title("Key Performance Indicators (KPI) Summary")
plt.xlabel("KPI")
plt.ylabel("Value")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save chart
output_path = project_folder / "charts" / "kpi_summary_chart.png"
plt.savefig(output_path, dpi=300)

plt.show()

print("KPI summary chart saved successfully:")
print(output_path)