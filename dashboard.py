# Streamlit dashboard for visualizing job application data stored in SQLite.
#
# Install Streamlit first:
#   pip install streamlit
#
# Run dashboard:
#   streamlit run dashboard.py

import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st


# Database file used by the project.
DB_FILE = "job_applications.db"


# Load application records from SQLite into a pandas DataFrame.
def load_applications():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            query = """
                SELECT id, company, title, url, status, applied_date
                FROM applications
                ORDER BY applied_date DESC
            """
            df = pd.read_sql_query(query, conn)
            return df
    except sqlite3.Error as exc:
        st.error(f"Database error: {exc}")
        return pd.DataFrame(columns=["id", "company", "title", "url", "status", "applied_date"])


# Build key metrics used at the top of the dashboard.
def calculate_metrics(df):
    # Total applications = total rows.
    total_applications = len(df)

    # Unique companies = unique non-empty company values.
    unique_companies = df["company"].fillna("").str.strip().replace("", pd.NA).dropna().nunique()

    # Applications made today.
    today = datetime.now().date()
    if "applied_date" in df.columns:
        parsed_dates = pd.to_datetime(df["applied_date"], errors="coerce")
        applications_today = (parsed_dates.dt.date == today).sum()
    else:
        applications_today = 0

    return total_applications, unique_companies, int(applications_today)


# Prepare chart data grouped by day for the "Applications per day" chart.
def build_applications_per_day(df):
    if "applied_date" not in df.columns or df.empty:
        return pd.DataFrame(columns=["day", "applications"])

    # Convert text timestamps to datetime; invalid values become NaT.
    parsed = pd.to_datetime(df["applied_date"], errors="coerce")

    # Group by date only and count rows per day.
    chart_df = (
        pd.DataFrame({"day": parsed.dt.date})
        .dropna()
        .groupby("day")
        .size()
        .reset_index(name="applications")
        .sort_values("day")
    )

    return chart_df


# -------------------------------
# Streamlit App Layout Starts Here
# -------------------------------

# Header section.
st.set_page_config(page_title="Job Applications Dashboard", layout="wide")
st.title("📊 Job Applications Dashboard")
st.caption("Visual overview of your automated job application records.")

# Load data once at startup.
applications_df = load_applications()

# Metrics section.
total_applications, unique_companies, applications_today = calculate_metrics(applications_df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", total_applications)
col2.metric("Unique Companies", unique_companies)
col3.metric("Applications Today", applications_today)

# Charts section.
st.subheader("Applications per Day")
chart_df = build_applications_per_day(applications_df)

if chart_df.empty:
    st.info("No chart data available yet. Run the application pipeline to add records.")
else:
    # Use a line chart to show trend over time.
    chart_data = chart_df.set_index("day")
    st.line_chart(chart_data["applications"])

# Application table section.
st.subheader("All Applications")

# Display only the requested columns in the table.
if applications_df.empty:
    st.info("No application records found in job_applications.db yet.")
else:
    table_df = applications_df[["company", "title", "status", "applied_date"]].copy()
    st.dataframe(table_df, use_container_width=True)
