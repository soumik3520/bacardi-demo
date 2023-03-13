from ui import header_ui, sidebar_ui
from utils import read_app_data, build_line_chart,format_layout_fig, gen_sku_metrics
import streamlit as st
import numpy as np

# Header
st.set_page_config(layout="wide")
header_ui()
sidebar_ui()
# Read data
df = read_app_data()

# dropdown variables
markets = df["Market"].unique()

with st.sidebar:
    market_filter = st.selectbox(label="Market",options=markets)

categories = df.loc[df["Market"]==market_filter]["Category"].unique()
with st.sidebar:
    cat_filter = st.selectbox(label="Category",options=categories)

sub_categories = df.loc[(df["Category"]==cat_filter) & (df["Market"]==market_filter)]["Sub-Category"].unique()
with st.sidebar:
    subcat_filter = st.selectbox(label="Sub Category",options=sub_categories)

sku = df.loc[df["Sub-Category"]==subcat_filter]["SKU"].unique()
with st.sidebar:
    sku_filter = st.multiselect(label="SKU",options=sku, default=sku[0])

cond1 = df["Market"] == market_filter
cond2 = df["Category"] == cat_filter
cond3 = df["Sub-Category"] == subcat_filter
cond4 = df["SKU"].isin(sku_filter)
filt_df = df.loc[cond1 & cond2 & cond3 & cond4]

# # Metric Boxes
# sku_metrics = gen_sku_metrics(filt_df)
# value_sales = f"${sku_metrics['value_sales']:,.0f}"
# value_delta = f"{np.round(sku_metrics['value_yoy_grth']*100,0):,.0f}%"
# unit_sales = f"${sku_metrics['units_sales']:,.0f}"
# units_delta = f"{np.round(sku_metrics['unit_yoy_grth']*100,0):,.0f}%"
# MAPE = f"{sku_metrics['MAPE']:,.0f}%"
# R2 = f"{sku_metrics['R2']:,.0f}%"

# col1, col2, col3, col4 = st.columns(4)
# with col1:
#     st.metric(value=value_sales, label="Value Sales", delta=value_delta)

# with col2:
#     st.metric(value=unit_sales, label="Units Sales", delta=units_delta)
# with col3:
#     st.metric(value=MAPE, label="MAPE", delta=None)
# with col4:
#     st.metric(value=R2, label="R-Square", delta=None)

units_fig = build_line_chart(filt_df, x_col="Date", y_col="Units", color_col="SKU")
units_fig = format_layout_fig(units_fig, title=f"Units Sales Actual and Forecasts")
value_fig = build_line_chart(filt_df, x_col="Date", y_col="Price", color_col="SKU")
value_fig = format_layout_fig(value_fig, title=f"Price ($)", prefix=True)

st.plotly_chart(units_fig, use_container_width=True)
st.plotly_chart(value_fig, use_container_width=True)
