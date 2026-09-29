# Care Transition Efficiency and Placement Outcome Analytics

## Project Overview

This project analyzes care transition data to understand movement through the care pipeline, identify operational bottlenecks, and study transition and discharge patterns.

## Key Analysis Areas

- Data cleaning and preprocessing
- Exploratory data analysis
- Care pipeline flow analysis
- CBP to HHS transfer analysis
- HHS discharge analysis
- Backlog and bottleneck detection
- Monthly trend analysis
- Outcome stability analysis
- KPI-based operational monitoring
- Interactive Streamlit dashboard

## Technologies Used

- Python
- Pandas
- Matplotlib
- Streamlit
- Git and GitHub

## Project Structure

- `app/` – Streamlit dashboard
- `charts/` – Generated analysis charts
- `data/` – Raw and cleaned datasets and KPI summaries
- `notebooks/` – Data inspection, cleaning, and analysis scripts

## Data Limitation

The provided dataset does not contain a separate successful sponsor placement field. Therefore, placement-related analysis is interpreted using the available transfer and discharge data rather than claiming individual sponsor placement success.

## Dashboard

The project includes an interactive Streamlit dashboard with date filtering, KPI monitoring, trend analysis, bottleneck indicators, threshold alerts, and executive insights.
