import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

# --- Streamlit UI ---
st.set_page_config(page_title="What-If NPV Simulator", layout="centered")
st.title("📊 What-If Analysis: NPV Based on Revenue Growth & Cost Growth")

# --- User Inputs ---
initial_investment = st.number_input("💰 Initial Investment ($)", value=50000)
revenue_base = st.number_input("📈 Base Annual Revenue ($)", value=20000)
cost_base = st.number_input("📉 Base Annual Cost ($)", value=10000)
years = st.slider("⏳ Project Duration (Years)", min_value=1, max_value=10, value=5)
discount_rate = st.slider("🏦 Discount Rate (WACC %)", 0.0, 20.0, 10.0) / 100

revenue_growth_range = st.slider("📊 Revenue Growth Range (%)", -50, 100, (-10, 50))
cost_growth_range = st.slider("📊 Cost Growth Range (%)", 0, 100, (0, 50))

# --- Simulation Grid ---
revenue_growths = np.linspace(revenue_growth_range[0], revenue_growth_range[1], 10) / 100
cost_growths = np.linspace(cost_growth_range[0], cost_growth_range[1], 10) / 100

results = []

for r_growth in revenue_growths:
    for c_growth in cost_growths:
        cash_flows = []
        for year in range(1, years + 1):
            revenue = revenue_base * ((1 + r_growth) ** year)
            cost = cost_base * ((1 + c_growth) ** year)
            cash_flows.append(revenue - cost)
        npv = npf.npv(discount_rate, [-initial_investment] + cash_flows)
        results.append({
            "Revenue Growth %": round(r_growth * 100, 1),
            "Cost Growth %": round(c_growth * 100, 1),
            "NPV ($)": round(npv, 2)
        })

# --- Create DataFrame ---
df = pd.DataFrame(results)

# --- Pivot for Heatmap ---
pivot_df = df.pivot(index="Revenue Growth %", columns="Cost Growth %", values="NPV ($)")

# --- Plot Heatmap ---
fig, ax = plt.subplots(figsize=(10, 6))
cmap = plt.get_cmap("RdYlGn")

heatmap = ax.imshow(pivot_df.values, cmap=cmap, origin="lower", aspect="auto")

# Set ticks and labels
ax.set_xticks(np.arange(len(pivot_df.columns)))
ax.set_yticks(np.arange(len(pivot_df.index)))
ax.set_xticklabels([f"{x}%" for x in pivot_df.columns])
ax.set_yticklabels([f"{y}%" for y in pivot_df.index])

# Rotate x-axis labels
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

# Titles and labels
ax.set_xlabel("Cost Growth %")
ax.set_ylabel("Revenue Growth %")
ax.set_title("NPV Heatmap: Revenue vs Cost Growth")

# Add color bar
cbar = plt.colorbar(heatmap)
cbar.set_label("NPV ($)")

# Display in Streamlit
st.pyplot(fig)

# --- Display Table ---
st.subheader("📋 Detailed Scenario Table")
st.dataframe(df.style.background_gradient(cmap="RdYlGn", subset=["NPV ($)"]))
