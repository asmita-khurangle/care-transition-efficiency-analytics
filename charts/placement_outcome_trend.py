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

# Sort by date
df = df.sort_values("Date")

# Create the chart
plt.figure(figsize=(12, 6))

# Plot transfer and discharge outcomes
plt.plot(
    df["Date"],
    df["Children transferred out of CBP custody"],
    marker="o",
    label="Children transferred out of CBP custody"
)

plt.plot(
    df["Date"],
    df["Children discharged from HHS Care"],
    marker="o",
    label="Children discharged from HHS Care"
)

# Chart title and labels
plt.title("Monthly Placement Outcome Trend")
plt.xlabel("Month")
plt.ylabel("Number of Children")

# Legend
plt.legend()

# Improve layout
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
output_path = project_folder / "charts" / "placement_outcome_trend.png"
plt.savefig(output_path, dpi=300)

# Display chart
plt.show()

print("Placement outcome trend chart saved successfully:")
print(output_path)