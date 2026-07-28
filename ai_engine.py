"""
ai_engine.py
Handles all communication with the Anthropic API (Claude).
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def generate_executive_briefing(sales_df, finance_df, cs_df, product_df, marketing_df, ops_df):
    """
    Sends a summary of all six business domains to Claude and asks for
    a concise executive briefing in plain English.
    """
    sales_summary = sales_df.groupby("month")["revenue"].sum().to_string()
    finance_summary = finance_df.groupby("month")["expense"].sum().to_string()
    churn_summary = cs_df.groupby("month")["churn_rate_pct"].mean().to_string()
    tickets_summary = product_df.groupby("month")["support_tickets"].sum().to_string()
    roi_summary = marketing_df.groupby("month")["roi"].mean().to_string()
    delivery_summary = ops_df.groupby("month")["on_time_delivery_pct"].mean().to_string()

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

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def generate_root_cause_analysis(sales_df, finance_df, cs_df, product_df, marketing_df, ops_df):
    """
    Asks Claude to dig into WHY the most significant anomaly happened,
    connecting signals across domains rather than describing one metric alone.
    """
    sales_summary = sales_df.groupby("month")["revenue"].sum().to_string()
    finance_summary = finance_df.groupby("month")["expense"].sum().to_string()
    churn_summary = cs_df.groupby("month")["churn_rate_pct"].mean().to_string()
    tickets_summary = product_df.groupby("month")["support_tickets"].sum().to_string()
    roi_summary = marketing_df.groupby("month")["roi"].mean().to_string()
    delivery_summary = ops_df.groupby("month")["on_time_delivery_pct"].mean().to_string()

    prompt = f"""You are a sharp business analyst investigating root causes for a CEO.

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

Identify the SINGLE most significant anomaly across all this data (the biggest dip, spike, or inflection point).

Then write a root cause analysis (under 300 words) that:
1. Names the anomaly precisely (which metric, which month, how large)
2. Traces possible causes by looking for correlated movements in OTHER domains around the same time
3. States your confidence level in the causal link (high/medium/low) and why
4. Notes what data would confirm or rule out this theory

Write like an analyst who is genuinely investigating, not just describing numbers."""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=700,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def generate_recommended_actions(sales_df, finance_df, cs_df, product_df, marketing_df, ops_df):
    """
    Asks Claude for specific, prioritized actions leadership should take this week.
    """
    sales_summary = sales_df.groupby("month")["revenue"].sum().to_string()
    finance_summary = finance_df.groupby("month")["expense"].sum().to_string()
    churn_summary = cs_df.groupby("month")["churn_rate_pct"].mean().to_string()
    tickets_summary = product_df.groupby("month")["support_tickets"].sum().to_string()
    roi_summary = marketing_df.groupby("month")["roi"].mean().to_string()
    delivery_summary = ops_df.groupby("month")["on_time_delivery_pct"].mean().to_string()

    prompt = f"""You are a decisive Chief of Staff giving a CEO their prioritized action list for this week.

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

Give exactly 3 recommended actions, ranked by priority. For each one:
- The specific action (concrete, not generic advice like "improve retention")
- Which team owns it
- What you expect to happen if it's NOT done

Keep the whole response under 200 words. Be direct and specific, not diplomatic."""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text