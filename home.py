import streamlit as st
import importlib
from ui.ui_components import UIComponents

st.set_page_config(
    page_title="Demo Streamlit",
    layout="wide",
)

# Set page layout
UIComponents.set_page_width_centered(width=960)
# UIComponents.show_logo_conditional('home', width=960, centered=False)

# st.image("assets/logo.jpg", width=960)

# MAP: Tên menu → file python
MENU = {
    "Giới thiệu": "src.gioi_thieu",
    "Capstone Project 1": "src.capstone_project1",
    "Capstone Project 2": "src.capstone_project2",
    "Thực hiện Project 1": "src.project1_control_page",
    "Thực hiện Project 2": "src.project2_control_page",
    # "UI Components": "ui.ui_components_demo",
}

# Sidebar
choice = st.sidebar.selectbox("Menu", list(MENU.keys()))

# Import dynamic file
module = importlib.import_module(MENU[choice])
module.show()



