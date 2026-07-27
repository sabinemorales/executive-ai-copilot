"""
generate_data.py
Creates realistic synthetic business data for the Executive AI Copilot.
Run this once to populate the data/ folder with CSV files.
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)
os.makedirs("data", exist_ok=True)

months = pd.date_range(start="2025-01-01", periods=12, freq="MS")


def generate_sales_data():
    """Monthly sales revenue by region, with a deliberate dip in March."""
    regions = ["North America", "EMEA", "APAC"]
    rows = []
    for month in months:
        for region in regions:
            base_revenue = {"North America": 500000, "EMEA": 300000, "APAC": 200000}[region]
            noise = np.random.normal(0, 15000)
            revenue = base_revenue + noise
            if month.month == 3:
                revenue *= 0.72
            rows.append({
                "month": month.strftime("%Y-%m"),
                "region": region,
                "revenue": round(revenue, 2),
                "units_sold": int(revenue / 250)
            })
    df = pd.DataFrame(rows)
    df.to_csv("data/sales.csv", index=False)
    print(f"Created data/sales.csv with {len(df)} rows")


def generate_finance_data():
    """Monthly expenses by category, with a Q2 cost overrun in Operations."""
    categories = ["Payroll", "Marketing", "Operations", "R&D", "G&A"]
    rows = []
    for month in months:
        for cat in categories:
            base_expense = {"Payroll": 400000, "Marketing": 120000,
                             "Operations": 90000, "R&D": 150000, "G&A": 60000}[cat]
            noise = np.random.normal(0, 8000)
            expense = base_expense + noise
            # Deliberate problem: Operations costs spike in Q2 (Apr-Jun)
            if cat == "Operations" and month.month in [4, 5, 6]:
                expense *= 1.45
            rows.append({
                "month": month.strftime("%Y-%m"),
                "category": cat,
                "expense": round(expense, 2)
            })
    df = pd.DataFrame(rows)
    df.to_csv("data/finance.csv", index=False)
    print(f"Created data/finance.csv with {len(df)} rows")


def generate_customer_success_data():
    """Monthly churn rate by region, with a deliberate spike in APAC."""
    regions = ["North America", "EMEA", "APAC"]
    rows = []
    for month in months:
        for region in regions:
            base_churn = {"North America": 2.1, "EMEA": 2.4, "APAC": 2.0}[region]
            noise = np.random.normal(0, 0.2)
            churn = base_churn + noise
            # Deliberate problem: APAC churn rises steadily after August
            if region == "APAC" and month.month >= 8:
                churn += (month.month - 7) * 0.6
            rows.append({
                "month": month.strftime("%Y-%m"),
                "region": region,
                "churn_rate_pct": round(max(churn, 0.1), 2)
            })
    df = pd.DataFrame(rows)
    df.to_csv("data/customer_success.csv", index=False)
    print(f"Created data/customer_success.csv with {len(df)} rows")


def generate_product_data():
    """Monthly support tickets by feature, with a bug spike in 'Checkout'."""
    features = ["Checkout", "Search", "Dashboard", "Mobile App", "Notifications"]
    rows = []
    for month in months:
        for feature in features:
            base_tickets = {"Checkout": 40, "Search": 25, "Dashboard": 20,
                             "Mobile App": 35, "Notifications": 15}[feature]
            noise = np.random.normal(0, 4)
            tickets = base_tickets + noise
            # Deliberate problem: Checkout has a bug spike in June-July
            if feature == "Checkout" and month.month in [6, 7]:
                tickets *= 2.8
            rows.append({
                "month": month.strftime("%Y-%m"),
                "feature": feature,
                "support_tickets": int(max(tickets, 0))
            })
    df = pd.DataFrame(rows)
    df.to_csv("data/product.csv", index=False)
    print(f"Created data/product.csv with {len(df)} rows")


def generate_marketing_data():
    """Monthly ROI by channel, with a deliberate decline in Paid Social."""
    channels = ["Paid Search", "Paid Social", "Email", "Organic", "Events"]
    rows = []
    for month in months:
        for channel in channels:
            base_roi = {"Paid Search": 3.2, "Paid Social": 2.8,
                        "Email": 4.5, "Organic": 5.1, "Events": 2.1}[channel]
            noise = np.random.normal(0, 0.15)
            roi = base_roi + noise
            ## Deliberate problem: Paid Social ROI steadily declines after month 6
            if channel == "Paid Social" and month.month >= 6:
                roi -= (month.month - 5) * 0.25
            spend = {"Paid Search": 80000, "Paid Social": 60000,
                     "Email": 15000, "Organic": 5000, "Events": 40000}[channel]
            rows.append({
                "month": month.strftime("%Y-%m"),
                "channel": channel,
                "spend": spend,
                "roi": round(max(roi, 0.1), 2)
            })
    df = pd.DataFrame(rows)
    df.to_csv("data/marketing.csv", index=False)
    print(f"Created data/marketing.csv with {len(df)} rows")


def generate_operations_data():
    """Monthly on-time delivery rate, with a deliberate dip from a supply chain delay."""
    rows = []
    for month in months:
        base_rate = 96.5
        noise = np.random.normal(0, 0.8)
        rate = base_rate + noise
        # Deliberate problem: a supply chain issue hits delivery in September
        if month.month == 9:
            rate -= 18
        rows.append({
            "month": month.strftime("%Y-%m"),
            "on_time_delivery_pct": round(min(max(rate, 0), 100), 2),
            "avg_shipping_days": round(3.2 if month.month != 9 else 6.8, 1)
        })
    df = pd.DataFrame(rows)
    df.to_csv("data/operations.csv", index=False)
    print(f"Created data/operations.csv with {len(df)} rows")


if __name__ == "__main__":
    generate_sales_data()
    generate_finance_data()
    generate_customer_success_data()
    generate_product_data()
    generate_marketing_data()
    generate_operations_data()
    print("Done generating all data.")