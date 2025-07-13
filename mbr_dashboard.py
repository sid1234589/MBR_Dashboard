import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Generate 6 months of data
months = pd.date_range(start="2025-02-01", periods=6, freq='MS')

# Simulate KPI data
df = pd.DataFrame({
    "Month": months.strftime("%b %Y"),
    "Uptime %": np.random.normal(99.3, 0.5, 6).round(2),
    "TAT (hrs)": np.random.normal(24, 3, 6).round(1),
    "Error Rate %": np.random.normal(0.7, 0.2, 6).round(2),
    "Customer Satisfaction %": np.random.normal(85, 2, 6).round(1)
})

# Define targets
targets = {
    "Uptime %": 99.5,
    "TAT (hrs)": 24,
    "Error Rate %": 1.0,
    "Customer Satisfaction %": 85
}

# RAG logic
def rag_status(actual, target, reverse=False):
    if reverse:
        if actual <= target: return '🟢'
        elif actual <= target * 1.1: return '🟠'
        else: return '🔴'
    else:
        if actual >= target: return '🟢'
        elif actual >= target * 0.9: return '🟠'
        else: return '🔴'

# Add calculated columns
for kpi in targets:
    df[f"{kpi} Target"] = targets[kpi]
    df[f"{kpi} Variance %"] = ((df[kpi] - targets[kpi]) / targets[kpi] * 100).round(2)
    reverse = True if "TAT" in kpi or "Error" in kpi else False
    df[f"{kpi} RAG"] = df[kpi].apply(lambda x: rag_status(x, targets[kpi], reverse))

# Streamlit UI
st.set_page_config(layout="wide")
st.title("📊 Monthly Business Review Dashboard")
st.markdown("### KPI Performance Overview")
st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)


# Chart section
selected_kpi = st.selectbox("📈 Select KPI to View Trend", list(targets.keys()))

fig, ax = plt.subplots()
ax.plot(df["Month"], df[selected_kpi], marker='o', label='Actual')
ax.axhline(targets[selected_kpi], color='red', linestyle='--', label='Target')
ax.set_title(f"{selected_kpi} Trend")
ax.set_ylabel(selected_kpi)
ax.legend()
st.pyplot(fig)

# Risk Summary
st.markdown("### ⚠ Risk Summary & Action Plan")
latest_row = df.iloc[-1]
if latest_row["TAT (hrs)"] > targets["TAT (hrs)"]:
    st.error("Turnaround Time exceeded target. Root cause: Ticket backlog. Action: Hire temp agents.")
if latest_row["Customer Satisfaction %"] < targets["Customer Satisfaction %"]:
    st.warning("Customer Satisfaction is below target. Root cause: Delays. Action: Improve response workflow.")
