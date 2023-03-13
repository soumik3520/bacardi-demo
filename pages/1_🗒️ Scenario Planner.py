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
}

# Aggrid generation
sc_data = read_scenario_planner()
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
        text-align: center;
    }
</style>"""
st.markdown(metric_style, unsafe_allow_html=True)

st.button(label="Run Scenario")