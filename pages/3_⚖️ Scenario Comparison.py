import streamlit as st
from ui import header_ui, sidebar_ui
from utils import (
    read_scenario_data,
    gen_aggrid,
    read_scenario_details,
    format_layout_fig,
)
from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    GridUpdateMode,
    JsCode,
    ColumnsAutoSizeMode,
)
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import plotly.express as px

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

# Custom CSS
custom_css = {
    ".ag-header-cell-label": {"justify-content": "center"},
    "cellStyle": {"textAlign": "center"},
    ".ag-cell": {"display": "flex", "justify-content": "center",},
    # ".ag-cell": {"white-space": "break-spaces"},
}


# Aggrid generation
gd = gen_aggrid(sc_data)
gd.configure_column(
    field="Name", header_name="Name", cellStyle={"white-sapces": "break-spaces"}
)
gd.configure_selection(
    selection_mode="multiple", use_checkbox=True,
)
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

if len(selected_row) > 0:
    st.write("## Comparison of Selected Scenarios")
    selected_df = pd.DataFrame(selected_row)
    sel_cols = ["Name", "revenue", "cost", "profit"]
    selected_df = selected_df[sel_cols]

    selected_df = selected_df.rename(
        columns={
            "index": "Metric",
            "Name": "Scenario",
            "revenue": "Revenue",
            "cost": "Cost",
            "profit": "Profit",
        }
    )
    selected_df = selected_df.set_index("Scenario")
    selected_df = selected_df.T.reset_index()
    # st.dataframe(selected_df)
    fig = px.histogram(
        selected_df,
        x="index",
        y=[x for x in selected_df.columns if x != "index"],
        barmode="group",
        text_auto=".2s",
    )
    fig = format_layout_fig(fig, title="Scenario Comparison", x_axis_title="")
    fig = fig.update_layout(
        legend=dict(
            yanchor="bottom", xanchor="center", orientation="h", y=-0.5, x=0.5, title=""
        ),
        yaxis_title="Value ($show)",
    )
    st.plotly_chart(fig, use_container_width=True)

# sel_scenario = [x["Name"] for x in selected_row]
# if len(sel_scenario) > 0:
#     st.write("## Comparison of Selected Scenarios")
#     sel_cols = ["Metric"] + sel_scenario
#     details_df = read_scenario_details()
#     details_df = details_df[sel_cols]
#     details_df = details_df.set_index("Metric")

#     temp = LinearSegmentedColormap.from_list("rg", ["r", "w", "g"], N=256)
#     details_df = details_df.style.background_gradient(
#         cmap=temp, axis=1, subset=pd.IndexSlice[["Profit", "% Profit"], :]
#     )

#     details_df = details_df.format(
#         formatter="{:.0%}",
#         subset=pd.IndexSlice[
#             [
#                 "% Profit",
#                 "Allocation Current",
#                 "Allocation Year 1",
#                 "Allocation Year 2",
#                 "Allocation Year 3",
#             ],
#             :,
#         ],
#     )

#     details_df = details_df.format(
#         formatter="{:,.0f}",
#         subset=pd.IndexSlice[
#             [
#                 "Profit",
#                 "Price Current",
#                 "Price Year 1",
#                 "Price Year 2",
#                 "Price Year 3",
#                 "Inventory Holding Cost Current",
#                 "Inventory Holding Cost Year 1",
#                 "Inventory Holding Cost Year 2",
#                 "Inventory Holding Cost Year 3",
#                 "Demand Current",
#                 "Demand Year 1",
#                 "Demand Year 2",
#                 "Demand Year 3",
#                 "Revenue",
#                 "Cost",
#             ],
#             :,
#         ],
#     )
#     st.dataframe(details_df, use_container_width=True)
