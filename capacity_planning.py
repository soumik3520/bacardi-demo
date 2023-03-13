import streamlit as st
import pandas as pd
from utils import read_app_data, format_layout_fig, mult_yaxis_plot
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def gen_cap_ui():
    df = read_app_data()

    # dropdown variables
    markets = df["Market"].unique()

    # Divide into columns
    col1, col2 = st.columns(2)
    col1.selectbox(label="Factory", options=["Factory 1", "Factory 2"])
    time_per = df["Year"].unique().tolist()
    time_filter = col2.slider(
        "Time Period", min_value=min(time_per), max_value=max(time_per)
    )

    cond1 = df["Market"] == "US"
    cond2 = df["Category"] == "Rum"
    cond3 = df["Sub-Category"] == "Dark"
    cond4 = df["SKU"] == "BACARDÍ CARTA ORO"
    cond5 = df["Year"] <= time_filter
    filt_df = df.loc[cond1 & cond2 & cond3 & cond4 & cond5]
    filt_df = filt_df[["Date", "Year", "SKU", "Price"]].drop_duplicates(subset=["Date"])
    filt_df["Inventory Holding"] = np.random.randint(
        low=10_000, high=25_000, size=filt_df.shape[0]
    )
    filt_df["Inventory Holding"] = np.random.randint(
        low=10_000, high=25_000, size=filt_df.shape[0]
    )
    filt_df["Revenue"] = filt_df["Inventory Holding"] * filt_df["Price"]
    filt_df["Margin"] = np.random.randint(low=10, high=34, size=filt_df.shape[0]) / 100
    # st.dataframe(filt_df)

    inv_fig = px.line(filt_df, x="Date", y="Inventory Holding")
    inv_fig = format_layout_fig(inv_fig, title="Factory Capacity", x_axis_title="")
    inv_fig = inv_fig.update_layout(yaxis_title="# Units", showlegend=False,)

    fig = mult_yaxis_plot(
        filt_df["Date"],
        filt_df["Inventory Holding"],
        filt_df["Margin"],
        "Revenue",
        "Margin %",
    )
    fig = format_layout_fig(fig, title="Revenue & Margin", x_axis_title="")
    fig.update_layout(
        yaxis2={"tickformat": ",.0%", "showgrid": True},
        xaxis=dict(showgrid=False),
        xaxis2=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        legend=dict(yanchor="bottom", xanchor="center", orientation="h", y=-0.5, x=0.5),
        yaxis_title="Revenue ($)",
        yaxis2_title="Margin %",
        showlegend=False,
    )

    col1, col2 = st.columns(2)
    col1.plotly_chart(inv_fig, use_container_width=True)
    col2.plotly_chart(fig, use_container_width=True)
    filt_df = filt_df.set_index("Year")
    filt_df = filt_df[["Revenue", "Margin"]].T
    filt_df1 = filt_df.iloc[[0]]
    filt_df2 = filt_df.iloc[[1]]
    filt_df2 = filt_df2.style.format(
        formatter="{:.0%}", subset=pd.IndexSlice[["Margin"], :,],
    )
    filt_df1 = filt_df1.style.format(
        formatter="{:,.0f}", subset=pd.IndexSlice[["Revenue"], :,],
    )
    col1, col2 = st.columns(2)
    col1.dataframe(filt_df1, use_container_width=True)
    col2.dataframe(filt_df2, use_container_width=True)


if __name__ == "__main__":
    gen_cap_ui()
