"""
ai_engine.py
Handles all communication with the Anthropic API (Claude).
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load variables from our .env file into the environment
load_dotenv()

# Create one client we can reuse for every API call in this app
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def generate_executive_briefing(sales_df, finance_df, cs_df, product_df, marketing_df, ops_df):
    """
    Sends a summary of all six business domains to Claude and asks for
    a concise executive briefing in plain English.
    """

    # Step 1: Turn our data into simple text summaries Claude can read.
    # We don't send the raw CSVs - we send pre-computed summaries, which
    # keeps the prompt small, fast, and cheap.
    sales_summary = sales_df.groupby("month")["revenue"].sum().to_string()
    finance_summary = finance_df.groupby("month")["expense"].sum().to_string()
    churn_summary = cs_df.groupby("month")["churn_rate_pct"].mean().to_string()
    tickets_summary = product_df.groupby("month")["support_tickets"].sum().to_string()
    roi_summary = marketing_df.groupby("month")["roi"].mean().to_string()
    delivery_summary = ops_df.groupby("month")["on_time_delivery_pct"].mean().to_string()

    # Step 2: Build the prompt - clear instructions + the data
    prompt = f"""You are an experienced Chief of Staff preparing a weekly executive briefing for a CEO.

Here is this company's data across six domains for the past 12 months:

SALES REVENUE BY MONTH:
{sales_summary}

FINANCE - TOTAL EXPENSES BY MONTH:
{finance_summary}

CUSTOMER SUCCESS - AVG CHURN RATE (%) BY MONTH:
{churn_summary}

PRODUCT - TOTAL SUPPORT TICKETS BY MONTH:
{tickets_summary}

MARKETING - AVG ROI BY MONTH:
{roi_summary}

OPERATIONS - AVG ON-TIME DELIVERY (%) BY MONTH:
{delivery_summary}

Write a concise executive briefing (under 250 words) covering:
1. What happened - the 2-3 most important trends or anomalies across all domains
2. Why it matters - the business implication of each
3. What to focus on today - a short, prioritized list

Write in plain, direct, confident language a CEO would expect from a sharp Chief of Staff. No fluff, no generic statements."""

    # Step 3: Send it to Claude
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=800,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Step 4: Extract just the text from Claude's response
    return response.content[0].text
    