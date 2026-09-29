import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =========================================================
# PROJECT PATHS
# =========================================================

project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"
charts_folder = project_folder / "charts"

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Care Transition Analytics",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("Care Transition Efficiency and Placement Outcome Analytics")

st.write(
    "Interactive analytics dashboard for evaluating care-transition "
    "efficiency, workload, discharge outcomes, and potential bottlenecks."
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(data_folder / "care_transition_clean.csv")

df.columns = df.columns.str.strip()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

df = df.sort_values("Date")

# =========================================================
# FIND DATASET COLUMNS SAFELY
# =========================================================

def find_column(columns, keywords):
    for column in columns:
        normalized = column.lower().strip()
        if all(word.lower() in normalized for word in keywords):
            return column
    return None


intake_col = find_column(
    df.columns,
    ["apprehended", "CBP", "custody"]
)

cbp_load_col = find_column(
    df.columns,
    ["children", "CBP", "custody"]
)

transfer_col = find_column(
    df.columns,
    ["transferred", "CBP", "custody"]
)

hhs_load_col = find_column(
    df.columns,
    ["children", "HHS", "care"]
)

discharge_col = find_column(
    df.columns,
    ["discharged", "HHS", "care"]
)

# Show detected columns
st.sidebar.subheader("Detected Dataset Columns")

st.sidebar.write("Intake:", intake_col)
st.sidebar.write("CBP Load:", cbp_load_col)
st.sidebar.write("Transfers:", transfer_col)
st.sidebar.write("HHS Load:", hhs_load_col)
st.sidebar.write("Discharges:", discharge_col)

# Stop if any required column was not detected
required_columns = {
    "Intake": intake_col,
    "CBP Load": cbp_load_col,
    "Transfers": transfer_col,
    "HHS Load": hhs_load_col,
    "Discharges": discharge_col
}

missing = [
    name for name, column in required_columns.items()
    if column is None
]

if missing:
    st.error(
        "The following required columns could not be detected: "
        + ", ".join(missing)
    )
    st.write("Actual columns in your dataset:")
    st.write(df.columns.tolist())
    st.stop()

# Convert numeric columns
numeric_columns = [
    intake_col,
    cbp_load_col,
    transfer_col,
    hhs_load_col,
    discharge_col
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# =========================================================
# SIDEBAR FILTER
# =========================================================

st.sidebar.header("Dashboard Controls")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered_df = df[
        (df["Date"] >= start_date) &
        (df["Date"] <= end_date)
    ].copy()

else:
    filtered_df = df.copy()

if filtered_df.empty:
    st.warning("No data available for the selected date range.")
    st.stop()

# =========================================================
# HEADER INFORMATION
# =========================================================

st.info(
    f"Analysis period: {filtered_df['Date'].min().strftime('%d %b %Y')} "
    f"to {filtered_df['Date'].max().strftime('%d %b %Y')}"
)

# =========================================================
# CORE CALCULATIONS
# =========================================================

total_intake = filtered_df[intake_col].sum()
total_transfers = filtered_df[transfer_col].sum()
total_discharges = filtered_df[discharge_col].sum()

average_cbp_load = filtered_df[cbp_load_col].mean()
average_hhs_load = filtered_df[hhs_load_col].mean()

# Transfer Efficiency Ratio
if filtered_df[cbp_load_col].sum() > 0:
    transfer_efficiency = (
        total_transfers /
        filtered_df[cbp_load_col].sum()
    ) * 100
else:
    transfer_efficiency = 0

# Discharge Effectiveness Index
if filtered_df[hhs_load_col].sum() > 0:
    discharge_effectiveness = (
        total_discharges /
        filtered_df[hhs_load_col].sum()
    ) * 100
else:
    discharge_effectiveness = 0

# Pipeline throughput
total_entries = total_intake + total_transfers
total_exits = total_transfers + total_discharges

if total_entries > 0:
    pipeline_throughput = (
        total_exits / total_entries
    ) * 100
else:
    pipeline_throughput = 0

# Backlog indicator
filtered_df["Net Movement"] = (
    filtered_df[intake_col]
    - filtered_df[discharge_col]
)

backlog_accumulation = filtered_df["Net Movement"].sum()

# Average daily imbalance
average_daily_imbalance = filtered_df["Net Movement"].mean()

# =========================================================
# KPI SECTION
# =========================================================

st.header("Key Performance Indicators")

st.caption(
    "Note: These ratios compare aggregate flows with the corresponding "
    "dataset volumes. They should not be interpreted as percentages of "
    "individual cases successfully completed."
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Transfer Efficiency Ratio",
        f"{transfer_efficiency:.2f}%"
    )

with kpi2:
    st.metric(
        "Discharge Effectiveness",
        f"{discharge_effectiveness:.2f}%"
    )

with kpi3:
    st.metric(
        "Pipeline Throughput",
        f"{pipeline_throughput:.2f}%"
    )

with kpi4:
    st.metric(
        "Backlog Accumulation",
        f"{backlog_accumulation:,.0f}"
    )

# =========================================================
# ADDITIONAL KPI INFORMATION
# =========================================================

st.subheader("Operational Indicators")

op1, op2, op3, op4 = st.columns(4)

with op1:
    st.metric(
        "Total CBP Intake",
        f"{total_intake:,.0f}"
    )

with op2:
    st.metric(
        "Total CBP → HHS Transfers",
        f"{total_transfers:,.0f}"
    )

with op3:
    st.metric(
        "Total HHS Discharges",
        f"{total_discharges:,.0f}"
    )

with op4:
    st.metric(
        "Average HHS Care Load",
        f"{average_hhs_load:,.0f}"
    )

# =========================================================
# CARE PIPELINE
# =========================================================

st.header("Care Pipeline Flow")

st.write("CBP Custody")
st.write("      |")
st.write("      v")
st.write("CBP to HHS Transfer")
st.write("      |")
st.write("      v")
st.write("HHS Care")
st.write("      |")
st.write("      v")
st.write("Discharge")

st.write(f"Average CBP Active Load: {average_cbp_load:,.0f}")
st.write(f"Total CBP to HHS Transfers: {total_transfers:,.0f}")
st.write(f"Average HHS Active Load: {average_hhs_load:,.0f}")
st.write(f"Total HHS Discharges: {total_discharges:,.0f}")

# =========================================================
# MONTHLY TREND
# =========================================================

st.header("Monthly Care Transition Trend")

monthly = filtered_df.copy()

monthly["Month"] = monthly["Date"].dt.to_period("M").astype(str)

monthly_summary = (
    monthly
    .groupby("Month")[
        [
            intake_col,
            transfer_col,
            discharge_col
        ]
    ]
    .sum()
)

st.line_chart(monthly_summary)

# =========================================================
# TRANSFER AND DISCHARGE EFFICIENCY
# =========================================================

st.header("Transfer and Discharge Efficiency")

efficiency_df = pd.DataFrame({
    "Metric": [
        "CBP Transfer Flow Ratio",
        "HHS Discharge Flow Ratio"
    ],
    "Percentage": [
        transfer_efficiency,
        discharge_effectiveness
    ]
})

st.bar_chart(
    efficiency_df.set_index("Metric")
)

# =========================================================
# BACKLOG ANALYSIS
# =========================================================

st.header("Backlog and Bottleneck Analysis")

filtered_df["Daily Inflow"] = filtered_df[intake_col]

filtered_df["Daily Successful Exit Proxy"] = (
    filtered_df[transfer_col] +
    filtered_df[discharge_col]
)

filtered_df["Daily Imbalance"] = (
    filtered_df["Daily Inflow"] -
    filtered_df["Daily Successful Exit Proxy"]
)

st.line_chart(
    filtered_df.set_index("Date")[
        [
            "Daily Inflow",
            "Daily Successful Exit Proxy"
        ]
    ]
)

# =========================================================
# ALERT SYSTEM
# =========================================================

st.header("Threshold-Based Alerts")

threshold = st.slider(
    "Backlog Alert Threshold",
    min_value=0,
    max_value=10000,
    value=1000,
    step=100
)

high_backlog_days = filtered_df[
    filtered_df["Daily Imbalance"] > threshold
]

if len(high_backlog_days) > 0:

    st.warning(
        f"⚠️ {len(high_backlog_days)} day(s) exceeded the "
        f"selected backlog threshold."
    )

else:

    st.success(
        "✅ No days exceeded the selected backlog threshold."
    )

# =========================================================
# DELAY SEVERITY
# =========================================================

st.header("Delay Severity")

positive_imbalance = filtered_df[
    filtered_df["Daily Imbalance"] > 0
]

if len(positive_imbalance) > 0:

    delay_severity = positive_imbalance["Daily Imbalance"].mean()

else:

    delay_severity = 0

st.metric(
    "Average Daily Delay/Imbalance",
    f"{delay_severity:,.2f}"
)

# =========================================================
# OUTCOME TREND
# =========================================================

st.header("Placement and Outcome Trend")

outcome_df = filtered_df[
    [
        "Date",
        transfer_col,
        discharge_col
    ]
].copy()

outcome_df = outcome_df.set_index("Date")

st.line_chart(outcome_df)

st.caption(
    "Note: The supplied internship dataset does not contain a separate "
    "'Successful sponsor placements' field. Therefore, placement-success "
    "metrics are not independently calculated."
)

# =========================================================
# OUTCOME STABILITY
# =========================================================

st.header("Outcome Stability Analysis")

discharge_mean = filtered_df[discharge_col].mean()
discharge_std = filtered_df[discharge_col].std()

if discharge_mean > 0:
    discharge_cv = (
        discharge_std / discharge_mean
    ) * 100
else:
    discharge_cv = 0

st.metric(
    "Discharge Variability (CV)",
    f"{discharge_cv:.2f}%"
)

if discharge_cv < 20:
    st.success(
        "Discharge performance shows relatively low variability "
        "within the selected period."
    )
elif discharge_cv < 40:
    st.warning(
        "Discharge performance shows moderate variability."
    )
else:
    st.error(
        "Discharge performance shows high variability."
    )

# =========================================================
# CATEGORY TOTALS
# =========================================================

st.header("Total Volume by Category")

totals = {
    "CBP Intake": filtered_df[intake_col].sum(),
    "CBP Transfers": filtered_df[transfer_col].sum(),
    "HHS Discharges": filtered_df[discharge_col].sum()
}

totals_df = pd.DataFrame(
    {
        "Category": totals.keys(),
        "Total": totals.values()
    }
)

st.bar_chart(
    totals_df.set_index("Category")
)

# =========================================================
# DATA TABLE
# =========================================================

st.header("Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

st.header("Executive Summary")

st.write(
    f"""
**Analysis Period:** {filtered_df['Date'].min().strftime('%d %b %Y')}
to {filtered_df['Date'].max().strftime('%d %b %Y')}

**Transfer Efficiency:** {transfer_efficiency:.2f}%

**Discharge Effectiveness:** {discharge_effectiveness:.2f}%

**Overall Pipeline Flow Ratio:** {pipeline_throughput:.2f}%

**Backlog Accumulation Indicator:** {backlog_accumulation:,.0f}

The dashboard evaluates movement through the available care-transition
stages using the internship-provided dataset. It highlights transfer
efficiency, discharge performance, workload imbalance and periods that
may require further operational investigation.
"""
)

# =========================================================
# DATA LIMITATION
# =========================================================

st.header("Data Limitation")

st.info(
    "The internship-provided dataset does not include a separate "
    "Successful Sponsor Placements column. Sponsor-placement-specific "
    "metrics therefore cannot be independently calculated from the "
    "supplied dataset."
)

# =========================================================
# EXISTING CHARTS
# =========================================================

st.header("Generated Analysis Charts")

chart_files = [
    ("Monthly Care Transition Trend", "monthly_trend.png"),
    ("Total Children by Category", "category_totals.png"),
    ("Monthly Placement Outcome Trend", "placement_outcome_trend.png"),
    ("KPI Summary", "kpi_summary_chart.png")
]

for title, filename in chart_files:

    chart_path = charts_folder / filename

    if chart_path.exists():

        st.subheader(title)

        st.image(
            str(chart_path),
            use_container_width=True
        )

# =========================================================
# FOOTER
# =========================================================

st.success(
    "Care Transition Analytics Dashboard loaded successfully."
)