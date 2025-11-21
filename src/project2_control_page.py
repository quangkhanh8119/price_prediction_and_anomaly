import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

from ui.ui_components import UIComponents

# Set page config
st.set_page_config(layout="wide")

# Khởi tạo class
ui = UIComponents()

def show():
    # Set page layout    
    ui.set_page_layout(width=960, hide_branding=False)
    
    # st.title("Điều khiển Project 2 - Recommendation System")    
    # Tạo Menu ở Sidebar
    with st.sidebar:
        # st.title("Điều hướng")
        selected_page = st.radio(                        
            "Chọn chức năng:",
            ["Đề xuất xe theo id", "Đề xuất xe theo yêu cầu", "Nhóm xe theo đặc điểm"]
        )
    
    # Routing logic (Gọi hàm tương ứng theo lựa chọn)
    if selected_page == "Đề xuất xe theo id":
        de_xuat_theo_id()
    elif selected_page == "Đề xuất xe theo yêu cầu":
        de_xuat_theo_query()
    elif selected_page == "Nhóm xe theo đặc điểm":
        group_xe_theo_dac_diem()
# ============================================================
# HÀM XỬ LÝ DỰ ĐOÁN GIÁ XE 
# ============================================================
def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    
    # Đọc dữ liệu từ file data_motobikes_cleaned.csv    
    df = pd.read_csv(file_path)
    return df

def load_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(model_path)

    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

# ============================================================
# 3. CÁC HÀM XỬ LÝ THEO LỰA CHỌN Ở MENU
# ============================================================

def de_xuat_theo_id():
    ui.centered_text("Danh sách xe máy cũ", color="#1f77b4", size="36px")

      # Đọc dữ liệu từ file data_motobikes_cleaned.csv        
    df_bikes = load_data("./data/data_motobikes_cleaned.csv")   
    st.subheader("Đề xuất n xe máy theo id")

    # Lấy 10 xe máy
    random_bikes = df_bikes.head(n=10)    
    st.session_state.random_bikes = random_bikes

    # Kiểm tra xem 'selected_bike_id' đã có trong session_state hay chưa
    if 'selected_bike_id' not in st.session_state:
        # Nếu chưa có, thiết lập giá trị mặc định là None hoặc ID khách sạn đầu tiên
        st.session_state.selected_bike_id = None

    # Theo cách cho người dùng chọn khách sạn từ dropdown
    # Tạo một tuple cho mỗi khách sạn, trong đó phần tử đầu là tên và phần tử thứ hai là ID
    bike_options = [(row['tieu_de'], row['id']) for index, row in st.session_state.random_bikes.iterrows()]
    # st.session_state.random_bikes
    # Tạo một dropdown với options là các tuple này
    selected_bike = st.selectbox(
        "Chọn xe may bạn quan tâm:",
        options=bike_options,
        format_func=lambda x: x[0]  # Hiển thị tên xe máy
    )
    # Display the selected bike
    # st.write("Bạn đã chọn:", selected_bike)

    # Cập nhật session_state dựa trên lựa chọn hiện tại
    st.session_state.selected_bike_id = selected_bike[1]

    if st.session_state.selected_bike_id:
        st.write("bike_ID: ", st.session_state.selected_bike_id)
        # Hiển thị thông tin xe máy được chọn
        selected_bike = df_bikes[df_bikes['id'] == st.session_state.selected_bike_id]

        if not selected_bike.empty:
            st.write('#### Bạn vừa chọn:')
            st.write('### ', selected_bike['tieu_de'].values[0])

            bike_description = selected_bike['mo_ta_chi_tiet'].values[0]
            truncated_description = ' '.join(bike_description.split()[:100])
            st.write('##### Thông tin:')
            st.write(truncated_description, '...')

            st.write('##### Các xe máy khác bạn cũng có thể quan tâm:')
            # recommendations = get_recommendations(df_bikes, st.session_state.selected_bike_id, cosine_sim=cosine_sim_new, nums=3) 
            # display_recommended_bikes(recommendations, cols=3)
        else:
            st.write(f"Không tìm thấy xe máy với ID: {st.session_state.selected_bike_id}")

    def de_xuat_theo_query():    
        st.subheader("Đề xuất n xe máy theo yêu cầu người dùng nhập")

    def group_xe_theo_dac_diem():    
        st.subheader("Nhóm các xe máy theo đặc điểm chung")


