from ui import header_ui, sidebar_ui
from utils import read_app_data, build_line_chart, format_layout_fig, gen_sku_metrics
import streamlit as st
import numpy as np

# Header
header_ui()
sidebar_ui()

# Read data
df = read_app_data()

# dropdown variables
markets = df["Market"].unique()
categories = df["Category"].unique()

with st.sidebar:
    market_filter = st.selectbox(label="Market", options=markets)
    cat_filter = st.selectbox(label="Category", options=categories)

sub_categories = df.loc[df["Category"] == cat_filter]["Sub-Category"].unique()
with st.sidebar:
    subcat_filter = st.selectbox(label="Sub Category", options=sub_categories)

sku = df.loc[df["Sub-Category"] == subcat_filter]["SKU"].unique()
with st.sidebar:
    # sku_filter = st.selectbox(label="SKU", options=sku)
    sku_filter = st.multiselect("SKU", options=sku)


cond1 = df["Market"] == market_filter
cond2 = df["Category"] == cat_filter
cond3 = df["Sub-Category"] == subcat_filter
cond4 = df["SKU"].isin(sku_filter)
filt_df = df.loc[cond1 & cond2 & cond3 & cond4]


units_fig = build_line_chart(filt_df, x_col="Year", y_col="Units(in million cases)")
units_fig = format_layout_fig(units_fig, title=f"Unit Sales")
# value_fig = build_line_chart(filt_df, x_col="Date", y_col="Unit Price")
# value_fig = format_layout_fig(value_fig, title=f"Price ($) - {sku_filter}", prefix=True)

st.plotly_chart(units_fig, use_container_width=True)
# st.plotly_chart(value_fig, use_container_width=True)
