from ui import header_ui, sidebar_ui
import streamlit as st
from utils import read_scenario_planner, gen_aggrid_sc
from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    GridUpdateMode,
    JsCode,
    ColumnsAutoSizeMode,
)

# Header
header_ui()
sidebar_ui()
# Custom CSS
custom_css = {
    ".ag-header-cell-label": {"justify-content": "center"},
    "cellStyle": {"textAlign": "center"},
    ".ag-row .ag-cell": {"display": "flex","justify-content": "center"}
}


# Aggrid generation
sc_data = read_scenario_planner()
categories = sc_data["category"].unique().tolist()
category_filter = st.sidebar.selectbox("Category", options=categories)
sc_data = sc_data.loc[sc_data["category"]==category_filter]
skus = sc_data["sku"].unique()
sku_filter = st.sidebar.selectbox("SKU", options=skus)
sc_data = sc_data.loc[sc_data["sku"]==sku_filter]
capacity = sc_data["capacity"].max()
st.sidebar.text_input(label="Maximum Capacity", value=capacity, disabled=False)
gd = gen_aggrid_sc(sc_data)
grid_options = gd.build()
grid_table = AgGrid(
    sc_data,
    height=300,
    gridOptions=grid_options,
    fit_columns_on_grid_load=True,
    theme="material",
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
    update_mode=GridUpdateMode.VALUE_CHANGED,
    custom_css=custom_css,
    allow_unsafe_jscode=True
)

#st.write(grid_table)
metric_style = """
<style>
div.stButton > button:first-child {
    background-color: #0A36AF;
    color:#ffffff;
}
# div.stButton > button:hover {
#     background-color: #008080;
#     color:#ffffff;
#     }
div.row-widget.stButton {
        text-align: right;
    }
</style>"""
st.markdown(metric_style, unsafe_allow_html=True)

def on_click_but():
    st.session_state["button_pressed"]=1
st.button(label="Run Scenario", on_click=on_click_but)

if st.session_state.get("button_pressed",0)==1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(value="$275K", label="Revenue ($)", delta="10% (From Baseline)")
    with col2:
        st.metric(value="$175K", label="Cost ($)", delta="-5% (From Baseline)", delta_color="inverse")
    with col3:
        st.metric(value="$100K", label="Profit", delta="10% (From Baseline)")


