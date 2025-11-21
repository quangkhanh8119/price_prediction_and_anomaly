import streamlit as st

from ui.ui_components import UIComponents

# Set page layout
st.set_page_config(
    page_title="Giới Thiệu Dự Án Môn Học",  
    layout="wide",
)

# Khởi tạo class
ui = UIComponents()

def show():
    # Set page layout    
    ui.set_page_layout(width=960, hide_branding=False)

    # st.title("🌟 GIỚI THIỆU DỰ ÁN MÔN HỌC")    
    # st.subheader("Phân tích & xây dựng mô hình hóa dữ liệu xe máy đã qua sử dụng – Chợ Tốt")
    ui.centered_title_normal("Giới Thiệu Dự Án Môn Học","Phân tích & xây dựng mô hình hóa dữ liệu xe máy đã qua sử dụng trên ChợTốt")

    st.markdown("---")

    # Giảng viên & Học viên
    st.markdown("""
    ### 👨‍🏫 **Giảng viên hướng dẫn**
    - **Cô Khuất Thùy Phương**

    ### 👨‍🎓 **Học viên thực hiện**
    - **Nguyễn Quang Khánh**  
    - **Nguyễn Đức Bằng**

    ---
    """)

    # Tổng quan
    st.markdown("""
    ### 🚀 Tổng Quan
    Dự án được triển khai dựa trên bộ dữ liệu thực tế từ **Chợ Tốt**, bao gồm thông tin về hàng chục nghìn tin rao bán xe máy.  
    Nhóm đã thực hiện 4 bài toán chính nhằm phân tích dữ liệu, xây dựng mô hình học máy và đề xuất giải pháp thực tế.
    """)

    st.markdown("---")

    # Bài toán 1
    st.markdown("""
    ### 🏷️ **Dự đoán giá xe máy - Price Prediction**
    Xây dựng mô hình hồi quy (Regression Model) dự đoán giá bán hợp lý dựa trên các đặc trưng như:
    - Thương hiệu, dòng xe, loại xe
    - Dung tích, số km đã đi
    - Năm đăng ký, tình trạng, xuất xứ  

    👉 *Ứng dụng*: hỗ trợ người bán định giá, giúp người mua tham khảo mức giá thị trường.
    """)

    # Bài toán 2
    st.markdown("""
    ### 🚨 **Phát hiện giá bất thường - Anomaly Detection**
    Sử dụng kết quả dự đoán từ mô hình giá (Regression) và phân tích độ lệch để nhận diện các tin đăng có mức giá rao bán **bình thường** hay **bất thường**

    👉 *Ứng dụng*: cảnh báo các tin đăng quá rẻ hoặc quá đắt, tăng tính minh bạch, hạn chế gian lận và cảnh báo tin đăng bất thường.
    """)

    # Bài toán 3
    st.markdown("""
    ### ⭐ **Gợi ý xe tương tự - Recommendation System**
    Hệ thống gợi ý xe tương tự dựa trên:
    - Nội dung mô tả xe      
    - Khoảng cách vector giữa các tin
    - Đặc trưng kỹ thuật                

    👉 *Ứng dụng*: hỗ trợ người dùng nhanh chóng tìm được mẫu xe phù hợp nhu cầu..
    """)

    # Bài toán 4
    st.markdown("""
    ### 📊 **Gợi ý theo cụm - Recommendation System with Clustering**
    Sử dụng thuật toán **KMeans Clustering** để phân nhóm xe theo các đặc trưng quan trọng, từ đó gợi ý theo phân khúc xe:
    - Phân nhóm theo thương hiệu, loại xe, dung tích
    - Phân nhóm theo mức giá, năm đăng ký

    👉 *Ứng dụng*: hiểu rõ phân khúc thị trường và cá nhân hóa trải nghiệm người dùng
    """)

    st.markdown("---")

    # Cấu truc dự án
    st.markdown("""
    ### 📂 Cấu trúc Dự Án
    """)
    st.code("""
    project/
    │
    ├── assets/
    │   ├── logo.png    
    │
    ├── data/
    │   ├── data_motobikes.xlsx    
    │   ├── model_regression_best.pkl
    │   ├── model_anomaly_best.pkl
    │
    ├── src/
    │   ├── gioi_thieu.py
    │   ├── capstone_project1.py
    │   ├── capstone_project2.py
    │   ├── project1_control_page.py
    │   ├── project2_control_page.py
    │
    ├── ui/
    │   ├── ui_components.py
    │
    ├── home.py
    """)

    st.markdown("---")

    # Kết luận
    st.markdown("""
    ## 🎯 **Kết luận**
    Cả bốn bài toán trên tạo thành một hệ thống phân tích & gợi ý toàn diện giúp:
    - Định giá chính xác
    - Phát hiện bất thường
    - Gợi ý thông minh
    - Phân khúc thị trường hiệu quả
                
    Kết quả mang lại một bộ công cụ hỗ trợ phân tích tốt cho cả Project 1 và Project 2 trong việc đưa ra gợi ý hiệu quả trong hệ thống mua bán xe máy trực tuyến.
    """)
