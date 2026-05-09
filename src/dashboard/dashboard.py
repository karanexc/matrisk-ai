import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import sys
import os
from pathlib import Path

# ---------------------------------------------------
# PROJECT ROOT PATH
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))

from src.utils.helpers import generate_risk_commentary

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="MatRisk AI",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("MatRisk AI")

st.subheader(
    "AI-Powered Commodity & Financial Risk Intelligence Platform"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

risk_scores_path = PROJECT_ROOT / "data" / "processed" / "risk_scores.csv"

risk_scores = pd.read_csv(risk_scores_path)

risk_scores['Date'] = pd.to_datetime(
    risk_scores['Date']
)

risk_scores.set_index('Date', inplace=True)

# ---------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------

st.sidebar.header("Simulation Controls")

commodity = st.sidebar.selectbox(
    "Select Commodity",
    risk_scores.columns
)

shock_multiplier = st.sidebar.slider(
    "Shock Multiplier",
    1.0,
    3.0,
    1.5
)

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Selected Commodity",
    commodity
)

col2.metric(
    "Average Risk",
    round(risk_scores[commodity].mean(), 2)
)

col3.metric(
    "Shock Multiplier",
    shock_multiplier
)

# ---------------------------------------------------
# COMMODITY RISK ANALYSIS
# ---------------------------------------------------

st.markdown("---")

st.subheader("Commodity Risk Analysis")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    risk_scores[commodity],
    linewidth=2
)

ax.set_title(
    f"{commodity} Risk Trend"
)

ax.set_xlabel("Year")
ax.set_ylabel("Risk Score")

plt.tight_layout()

st.pyplot(fig, clear_figure=True)

# ---------------------------------------------------
# SHOCK SIMULATION
# ---------------------------------------------------

st.markdown("---")

st.subheader("Financial Shock Simulation")

shocked_risk = (
    risk_scores[commodity]
    *
    shock_multiplier
)

fig2, ax2 = plt.subplots(figsize=(12, 5))

ax2.plot(
    risk_scores[commodity],
    label='Original Risk',
    linewidth=2
)

ax2.plot(
    shocked_risk,
    label='Shock Scenario Risk',
    linewidth=2
)

ax2.set_title(
    f"{commodity} Shock Simulation"
)

ax2.set_xlabel("Year")
ax2.set_ylabel("Risk Score")

ax2.legend()

plt.tight_layout()

st.pyplot(fig2, clear_figure=True)

# ---------------------------------------------------
# PORTFOLIO RISK ANALYSIS
# ---------------------------------------------------

st.markdown("---")

st.subheader("Portfolio Risk Under Crisis Scenario")

portfolio_before = risk_scores.mean(axis=1)

portfolio_after = (
    risk_scores.mean(axis=1)
    *
    shock_multiplier
)

fig3, ax3 = plt.subplots(figsize=(12, 5))

ax3.plot(
    portfolio_before,
    label="Normal Portfolio Risk",
    linewidth=2
)

ax3.plot(
    portfolio_after,
    label="Crisis Portfolio Risk",
    linewidth=2
)

ax3.set_title(
    "Portfolio Risk Under Crisis Scenario"
)

ax3.set_xlabel("Year")
ax3.set_ylabel("Portfolio Risk")

ax3.legend()

plt.tight_layout()

st.pyplot(fig3, clear_figure=True)

# ---------------------------------------------------
# AI RISK INSIGHTS
# ---------------------------------------------------

st.markdown("---")

st.subheader("AI Risk Intelligence")

risk_increase = (
    shocked_risk.mean()
    -
    risk_scores[commodity].mean()
)

commentary = generate_risk_commentary(
    commodity,
    risk_increase,
    shock_multiplier
)

st.markdown(
    f"""
    ### AI Risk Insight

    {commentary}
    """
)