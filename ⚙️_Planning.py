import streamlit as st
import capacity_planning, cash_planning, inventory_planning
from ui import header_ui, sidebar_ui

# Header
st.set_page_config(layout="wide")
header_ui()
sidebar_ui()

with st.expander("Click for Inventory planning"):
    inventory_planning.gen_inv_ui()

with st.expander("Click for Capacity planning"):
    capacity_planning.gen_cap_ui()

with st.expander("Click for Cash Planning"):
    cash_planning.gen_cash_ui()
