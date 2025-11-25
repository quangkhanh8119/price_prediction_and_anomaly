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
    "Thực hiện Project 3": "src.user_price_module",
    "Thực hiện Project 4": "src.user_anomaly_module",
    "Thực hiện Project 5": "src.admin_dashboard",
    "Thực hiện Project 5a": "src.00_vehicle_price_main_app",
    "Thực hiện Project 6": "src.user_price_gauge",
    "Thực hiện Project 7a": "src.07_price_suggestion_tool",    
    "Thực hiện Project 7": "src.01_user_post_vehicle_page",
    "Thực hiện Project 8": "src.02_user_search_page",
    "Thực hiện Project 9": "src.03_admin_dashboard__page",
    "Thực hiện Project 10": "src.04_admin_anomaly_page",
    "Thực hiện Project 11": "src.05_price_suggestion_tool", 
    "Thực hiện Project 12": "src.08_price-suggestion-streamlit", 
    "Thực hiện Project 13": "src.16_phat_hien_bat_thuong", 
    "Thực hiện Project 14": "src.project1_control_page_bk",     
    
    # "UI Components": "ui.ui_components_demo",
}

# Sidebar
choice = st.sidebar.selectbox("Menu", list(MENU.keys()))

# Import dynamic file
module = importlib.import_module(MENU[choice])
module.show()



