"""pharmacy.py - Medicine inventory and low-stock alerts."""

import streamlit as st
import plotly.express as px
from utils.helpers import df_query


def render():
    st.markdown("## 💊 Pharmacy")
    st.caption("Simulated medicine inventory monitored by the Pharmacy Agent.")

    df = df_query("SELECT * FROM medicines ORDER BY stock_level ASC")

    low_stock = df[df["status"] == "Low Stock"]
    if len(low_stock):
        st.warning("⚠️ Low stock alert: " + ", ".join(low_stock["name"].tolist()))

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(
            df.rename(columns={
                "name": "Medicine", "category": "Category", "stock_level": "Stock Level",
                "reorder_threshold": "Reorder Threshold", "status": "Status",
            }).drop(columns=["id"]),
            width='stretch',
            hide_index=True,
        )
    with col2:
        fig = px.bar(
            df, x="name", y="stock_level", color="status",
            color_discrete_map={"Low Stock": "#d64545", "In Stock": "#1668a5"},
            labels={"name": "Medicine", "stock_level": "Stock Level"},
            title="Medicine Stock Levels",
        )
        fig.update_layout(xaxis_tickangle=-40)
        st.plotly_chart(fig, width='stretch')
