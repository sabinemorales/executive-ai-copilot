"""
app.py
Executive AI Copilot - main dashboard application.
"""

import streamlit as st
import pandas as pd

# Page configuration - must be the first Streamlit command in the script
st.set_page_config(page_title="Executive AI Copilot", layout="wide")

st.title("Executive AI Copilot")
st.caption("Your AI-powered command center for business performance")

# Load the sales data we generated earlier
sales_df = pd.read_csv("data/sales.csv")

# --- KPI Section ---
st.header("Sales KPIs")

total_revenue = sales_df["revenue"].sum()
total_units = sales_df["units_sold"].sum()
avg_monthly_revenue = sales_df.groupby("month")["revenue"].sum().mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue (YTD)", f"${total_revenue:,.0f}")
col2.metric("Total Units Sold", f"{total_units:,}")
col3.metric("Avg Monthly Revenue", f"${avg_monthly_revenue:,.0f}")

# --- Revenue Trend Chart ---
st.header("Monthly Revenue Trend")
monthly_revenue = sales_df.groupby("month")["revenue"].sum().reset_index()
st.line_chart(monthly_revenue.set_index("month"))

# --- Raw Data Table (for transparency/debugging) ---
st.header("Raw Sales Data")
st.dataframe(sales_df)