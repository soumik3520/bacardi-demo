import streamlit as st
from ui import header_ui, sidebar_ui
from utils import read_scenario_data, gen_aggrid, read_scenario_details
from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    GridUpdateMode,
    JsCode,
    ColumnsAutoSizeMode,
)
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import plotly.graph_objects as go


# Header
header_ui()
sidebar_ui()

#
sc_data = read_scenario_data()

# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

custom_css = {
    ".ag-header-cell-label": {"justify-content": "center"},
    "cellStyle": {"textAlign": "center"},
}


# Aggrid generation
gd = gen_aggrid(sc_data)
gd.configure_selection(selection_mode="multiple", use_checkbox=True)
grid_options = gd.build()
grid_table = AgGrid(
    sc_data,
    height=250,
    gridOptions=grid_options,
    fit_columns_on_grid_load=True,
    theme="balham",
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    custom_css=custom_css,
)

selected_row = grid_table["selected_rows"]
sel_scenario = [x["Name"] for x in selected_row]

if len(sel_scenario) > 0:
    st.write("## Comparison of Selected Scenarios")
    sc_data = sc_data.loc[sc_data.Name.isin(sel_scenario)].set_index("Name")[
        ["revenue", "cost", "inv_cost", "profit", "prec_profit"]
    ]
    sc_data = sc_data.T

    traces = []

    for column in sc_data.columns:

        trace = go.Bar(x=sc_data.index, y=sc_data[column], name=column)
        traces.append(trace)
    layout = go.Layout(
        title=" Comparison of selected scenarios",
        xaxis=dict(title="Name"),
        yaxis=dict(title="values"),
        barmode="group",
    )
    comparison_fig = go.Figure(data=traces, layout=layout)
    st.plotly_chart(comparison_fig, use_container_width=True)
