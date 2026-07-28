# Executive AI Copilot

**An AI-powered command center for business performance** — turning raw data across six business domains into an executive briefing, root cause analysis, recommended actions, and a conversational assistant, in seconds instead of hours.

![Executive AI Copilot dashboard](docs/screenshot.png)

## What it does

Most executives spend hours every week having someone manually pull, reconcile, and summarize data before they can even start deciding what to do about it. Executive AI Copilot compresses that into one click:

- **Executive Briefing** — a plain-language summary of what happened across Sales, Finance, Customer Success, Product, Marketing, and Operations, and why it matters
- **Root Cause Analysis** — identifies the single most significant anomaly in the data and investigates likely causes by correlating signals across domains, not just describing one metric in isolation
- **Recommended Actions** — three specific, prioritized, owner-assigned actions for the week, not generic advice
- **Interactive Chat** — ask any question in plain English, grounded in the real data, with full conversation memory for natural follow-ups
- **Full KPI Dashboard** — six tabbed views with live charts across every domain

## Why this matters

This isn't a chatbot bolted onto a spreadsheet. Every AI feature follows a deliberate pattern: **pre-computed data summaries in, structured reasoning out** — keeping prompts small, fast, and inexpensive, while ensuring the AI reasons over real numbers rather than guessing. The chat feature is explicitly instructed to say "not available in this dataset" rather than inventing an answer when asked about something the data doesn't contain — a small design choice that matters a great deal once real, messy company data replaces the synthetic demo data.

## Tech stack

| Layer | Tool |
|---|---|
| UI / dashboard | [Streamlit](https://streamlit.io) |
| Data handling | pandas |
| AI reasoning | [Claude](https://www.anthropic.com) via the Anthropic API |
| Charts | Streamlit native charting |
| Secrets management | python-dotenv |

## Getting started

Clone the repo:

    git clone https://github.com/sabinemorales/executive-ai-copilot.git
    cd executive-ai-copilot

Set up a virtual environment:

    python3.12 -m venv venv
    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Add your Anthropic API key:

    echo "ANTHROPIC_API_KEY=your_key_here" > .env

Generate the synthetic demo data:

    python3 generate_data.py

Run the app:

    streamlit run app.py

Get an API key at [console.anthropic.com](https://console.anthropic.com/settings/keys).

## Project structure

    executive-ai-copilot/
    ├── app.py              # Streamlit dashboard and UI
    ├── ai_engine.py        # All Claude API calls and prompt engineering
    ├── generate_data.py    # Synthetic data generator for all 6 domains
    ├── data/               # Generated CSVs (not committed — reproducible via generate_data.py)
    ├── requirements.txt
    └── .env                # API key (not committed)

## The data

The demo runs on realistic synthetic data with deliberately planted business stories — a March sales dip, a Q2 cost overrun, rising APAC churn, a Checkout bug spike, a Paid Social ROI decline, and a September delivery delay — so the AI features have real patterns to discover and explain, not a flat, uneventful dataset.

## What I learned building this

This project was built as a hands-on learning exercise covering Python fundamentals, Git/GitHub workflows, REST API integration, prompt engineering, and application architecture (specifically, separating data logic, AI logic, and presentation logic into distinct files). It's the first project in a broader portfolio of AI-powered business applications.

## Roadmap

- [ ] Deploy live on Streamlit Community Cloud
- [ ] Support uploading real company CSVs in place of synthetic data
- [ ] Add data validation and error handling for missing/malformed files
- [ ] Explore a Microsoft-stack equivalent (Fabric/OneLake + Copilot Studio) for enterprise deployment

## License

MIT
