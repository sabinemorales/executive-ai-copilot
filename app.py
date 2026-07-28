"""
app.py
Executive AI Copilot - main dashboard application.
"""

import streamlit as st
import pandas as pd
from ai_engine import generate_executive_briefing, generate_root_cause_analysis, generate_recommended_actions, chat_with_data

st.set_page_config(page_title="Executive AI Copilot", layout="wide")

st.title("Executive AI Copilot")
st.caption("Your AI-powered command center for business performance")

# Load all six datasets once, at the top
sales_df = pd.read_csv("data/sales.csv")
finance_df = pd.read_csv("data/finance.csv")
cs_df = pd.read_csv("data/customer_success.csv")
product_df = pd.read_csv("data/product.csv")
marketing_df = pd.read_csv("data/marketing.csv")
ops_df = pd.read_csv("data/operations.csv")

# --- Executive Briefing (AI-generated) ---
st.header("Executive Briefing")
if st.button("Generate Today's Briefing"):
    with st.spinner("Analyzing your business data..."):
        briefing = generate_executive_briefing(
            sales_df, finance_df, cs_df, product_df, marketing_df, ops_df
        )
    st.markdown(briefing)

# --- Root Cause Analysis (AI-generated) ---
st.header("Root Cause Analysis")
if st.button("Investigate Anomalies"):
    with st.spinner("Digging into the data..."):
        root_cause = generate_root_cause_analysis(
            sales_df, finance_df, cs_df, product_df, marketing_df, ops_df
        )
    st.markdown(root_cause)

# --- Recommended Actions (AI-generated) ---
st.header("Recommended Actions")
if st.button("Get This Week's Priorities"):
    with st.spinner("Prioritizing..."):
        actions = generate_recommended_actions(
            sales_df, finance_df, cs_df, product_df, marketing_df, ops_df
        )
    st.markdown(actions)

# --- Interactive Executive Chat ---
st.header("Ask a Question")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_question = st.chat_input("Ask anything about this data...")

if user_question:
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.spinner("Thinking..."):
        answer = chat_with_data(
            sales_df, finance_df, cs_df, product_df, marketing_df, ops_df,
            st.session_state.chat_history, user_question
        )

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.chat_history.append({"role": "user", "content": user_question})
    st.session_state.chat_history.append({"role": "assistant", "content": answer})

# Tabs let us organize 6 domains without one giant scrolling page
tab_sales, tab_finance, tab_cs, tab_product, tab_marketing, tab_ops = st.tabs(
    ["Sales", "Finance", "Customer Success", "Product", "Marketing", "Operations"]
)

with tab_sales:
    st.header("Sales KPIs")
    total_revenue = sales_df["revenue"].sum()
    total_units = sales_df["units_sold"].sum()
    avg_monthly_revenue = sales_df.groupby("month")["revenue"].sum().mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue (YTD)", f"${total_revenue:,.0f}")
    col2.metric("Total Units Sold", f"{total_units:,}")
    col3.metric("Avg Monthly Revenue", f"${avg_monthly_revenue:,.0f}")

    st.subheader("Monthly Revenue Trend")
    monthly_revenue = sales_df.groupby("month")["revenue"].sum().reset_index()
    st.line_chart(monthly_revenue.set_index("month"))

with tab_finance:
    st.header("Finance KPIs")
    total_expense = finance_df["expense"].sum()
    avg_monthly_expense = finance_df.groupby("month")["expense"].sum().mean()

    col1, col2 = st.columns(2)
    col1.metric("Total Expenses (YTD)", f"${total_expense:,.0f}")
    col2.metric("Avg Monthly Expense", f"${avg_monthly_expense:,.0f}")

    st.subheader("Expenses by Category Over Time")
    expense_by_cat = finance_df.pivot_table(index="month", columns="category", values="expense")
    st.line_chart(expense_by_cat)

with tab_cs:
    st.header("Customer Success KPIs")
    avg_churn = cs_df["churn_rate_pct"].mean()
    latest_month = cs_df["month"].max()
    latest_churn = cs_df[cs_df["month"] == latest_month]["churn_rate_pct"].mean()

    col1, col2 = st.columns(2)
    col1.metric("Avg Churn Rate", f"{avg_churn:.2f}%")
    col2.metric("Latest Month Churn", f"{latest_churn:.2f}%")

    st.subheader("Churn Rate by Region Over Time")
    churn_by_region = cs_df.pivot_table(index="month", columns="region", values="churn_rate_pct")
    st.line_chart(churn_by_region)

with tab_product:
    st.header("Product KPIs")
    total_tickets = product_df["support_tickets"].sum()
    col1 = st.columns(1)[0]
    col1.metric("Total Support Tickets (YTD)", f"{total_tickets:,}")

    st.subheader("Support Tickets by Feature Over Time")
    tickets_by_feature = product_df.pivot_table(index="month", columns="feature", values="support_tickets")
    st.line_chart(tickets_by_feature)

with tab_marketing:
    st.header("Marketing KPIs")
    total_spend = marketing_df["spend"].sum()
    avg_roi = marketing_df["roi"].mean()

    col1, col2 = st.columns(2)
    col1.metric("Total Marketing Spend (YTD)", f"${total_spend:,.0f}")
    col2.metric("Avg ROI", f"{avg_roi:.2f}x")

    st.subheader("ROI by Channel Over Time")
    roi_by_channel = marketing_df.pivot_table(index="month", columns="channel", values="roi")
    st.line_chart(roi_by_channel)

with tab_ops:
    st.header("Operations KPIs")
    avg_delivery = ops_df["on_time_delivery_pct"].mean()
    avg_shipping = ops_df["avg_shipping_days"].mean()

    col1, col2 = st.columns(2)
    col1.metric("Avg On-Time Delivery", f"{avg_delivery:.1f}%")
    col2.metric("Avg Shipping Days", f"{avg_shipping:.1f}")

    st.subheader("On-Time Delivery Rate Over Time")
    st.line_chart(ops_df.set_index("month")["on_time_delivery_pct"])