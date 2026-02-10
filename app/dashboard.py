import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import time

st.markdown("""
<style>
h1 {
    font-weight: 700;
}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Apply font globally */
* {
    font-family: 'Inter', sans-serif !important;
}

/* Fix metric cards */
div[data-testid="metric-container"] {
    background-color: #f9fafb;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
}

/* Metric label */
div[data-testid="metric-container"] > label {
    color: #6b7280 !important;
    font-size: 14px;
}

/* Metric value */
div[data-testid="metric-container"] > div {
    color: #111827 !important;
    font-size: 28px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Client Portfolio Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------ DATA LOADING ------------------
BASE_DIR = Path(__file__).resolve().parent.parent

portfolio = pd.read_csv(BASE_DIR / "data" / "client_portfolio.csv")
prices = pd.read_csv(BASE_DIR / "data" / "market_prices.csv")

df = portfolio.merge(prices, on="asset_name")
df["current_value"] = df["units"] * df["current_price"]
df["pnl"] = df["current_value"] - df["investment_amount"]
df["return_pct"] = (df["pnl"] / df["investment_amount"]) * 100

# ------------------ HEADER ------------------
st.title("📊 Client Portfolio Analysis & Optimization Dashboard")

st.markdown(
    """
    <div style="
        background-color:#0f172a;
        padding:12px 18px;
        border-radius:12px;
        margin-top:10px;
        margin-bottom:25px;
        border:1px solid #1f2937;
    ">
        <span style="font-size:15px; color:#e5e7eb;">
            <strong>Client Name:</strong> Rasika Talwar
        </span>
        &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
        <span style="font-size:15px; color:#e5e7eb;">
            <strong>Client ID:</strong> C001
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------ KPIs ------------------
total_invested = df["investment_amount"].sum()
current_value = df["current_value"].sum()
total_pnl = df["pnl"].sum()

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    placeholder = st.empty()
    steps = 30
    for i in range(0, steps + 1):
        value = int(total_invested * i / steps)
        placeholder.metric("💰 Total Invested", f"₹{value:,.0f}")
        time.sleep(0.015)

    placeholder.metric("💰 Total Invested", f"₹{total_invested:,.0f}")

kpi2.metric("📈 Current Value", f"₹{current_value:,.0f}")
kpi3.metric("📊 Total P&L", f"₹{total_pnl:,.0f}")

st.divider()

# ------------------ ALLOCATION CHART ------------------
st.subheader("📌 Asset Allocation")

allocation = (
    df.groupby("asset_class")["investment_amount"]
    .sum()
    .reset_index()
)

fig_alloc = px.pie(
    allocation,
    values="investment_amount",
    names="asset_class",
    hole=0.45,
    title="Asset Allocation by Class"
)

fig_alloc.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig_alloc.update_layout(
    transition_duration=600
)

st.plotly_chart(fig_alloc, use_container_width=True)

st.divider()

# ------------------ PERFORMANCE BY ASSET ------------------
st.subheader("📊 Asset-wise Performance")

fig_pnl = px.bar(
    df,
    x="asset_name",
    y="pnl",
    color="asset_class",
    title="Profit / Loss by Asset",
    text_auto=".2s"
)

fig_pnl.update_layout(
    transition_duration=700
)

st.plotly_chart(fig_pnl, use_container_width=True)


st.divider()

# ------------------ TABLE ------------------
st.subheader("📋 Portfolio Details")

st.dataframe(
    df[
        [
            "asset_name",
            "asset_class",
            "risk_category",
            "investment_amount",
            "current_value",
            "pnl",
            "return_pct"
        ]
    ].style.format({
        "investment_amount": "₹{:,.0f}",
        "current_value": "₹{:,.0f}",
        "pnl": "₹{:,.0f}",
        "return_pct": "{:.2f}%"
    }),
    use_container_width=True
)

st.divider()

# ------------------ INSIGHTS ------------------
st.subheader("🧠 Rebalancing Insights")

st.markdown("""
- 📈 Portfolio has **strong performance** with positive overall returns  
- ⚠️ **Equity exposure is high**, increasing volatility risk  
- 🛡️ **Debt allocation is low**, reducing downside protection  
- 🔄 Rebalancing toward debt can improve **risk-adjusted returns**
""")
