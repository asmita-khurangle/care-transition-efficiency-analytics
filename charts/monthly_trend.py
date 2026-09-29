import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Read the monthly summary file
file_path = project_folder / "data" / "monthly_summary.csv"
df = pd.read_csv(file_path)

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Sort by date
df = df.sort_values("Date")

# Create the chart
plt.figure(figsize=(12, 6))

# Plot every category except Date
for col in df.columns:
    if col != "Date":
        plt.plot(df["Date"], df[col], marker="o", label=col)

# Chart title and labels
plt.title("Monthly Care Transition Trend")
plt.xlabel("Month")
plt.ylabel("Number of Children")

# Show legend
plt.legend()

# Improve layout
plt.xticks(rotation=45)
plt.tight_layout()

# Save the chart
output_path = project_folder / "charts" / "monthly_trend.png"
plt.savefig(output_path, dpi=300)

# Display the chart
plt.show()

print("Monthly trend chart saved successfully:")
print(output_path)