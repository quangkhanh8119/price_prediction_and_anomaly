import streamlit as st

from ui.ui_components import UIComponents

# Khởi tạo class
ui = UIComponents()

def show():
    import streamlit as st

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

    # Bài toán 1
    st.markdown("""
    ## 🏷️ **Price Prediction – Dự đoán giá xe máy**
    Xây dựng mô hình hồi quy (Regression Model) dự đoán giá bán hợp lý dựa trên các đặc trưng:
    - Thương hiệu  
    - Dòng xe  
    - Loại xe  
    - Dung tích  
    - Số km đã đi  
    - Năm đăng ký  
    - Tình trạng xe  
    - Xuất xứ  

    👉 *Ứng dụng*: hỗ trợ người bán định giá, giúp người mua tham khảo mức giá thị trường.
    """)

    # Bài toán 2
    st.markdown("""
    ## 🚨 **Anomaly Detection – Phát hiện giá bất thường**
    Mô hình phát hiện liệu mức giá rao bán có **bình thường** hay **bất thường** dựa trên dự đoán từ mô hình regression và phân tích độ lệch.

    👉 *Ứng dụng*: cảnh báo các tin đăng quá rẻ hoặc quá đắt, tăng tính minh bạch cho thị trường rao vặt.
    """)

    # Bài toán 3
    st.markdown("""
    ## ⭐ **Recommendation System – Gợi ý xe tương tự**
    Hệ thống gợi ý xe tương tự dựa trên:
    - Nội dung mô tả xe  
    - Sự tương đồng đặc trưng  
    - Khoảng cách vector giữa các tin  

    👉 *Ứng dụng*: giúp người dùng tìm được chiếc xe phù hợp nhu cầu.
    """)

    # Bài toán 4
    st.markdown("""
    ## 📊 **Recommendation System with Clustering – Gợi ý theo cụm**
    Sử dụng thuật toán **KMeans Clustering** để phân nhóm xe theo các đặc trưng chung và gợi ý theo phân khúc:

    👉 *Ứng dụng*:  
    - Hiểu phân khúc thị trường  
    - Gợi ý theo nhóm (cluster)  
    - Tối ưu trải nghiệm người dùng theo phân loại xe
    """)

    st.markdown("---")

    # Kết luận
    st.markdown("""
    ## 🎯 **Kết luận**
    Dự án ứng dụng các kỹ thuật học máy hiện đại như:
    - Regression  
    - Statistical Anomaly Detection  
    - NLP-based Recommendation  
    - Clustering (K-Means)

    Kết quả mang lại một bộ công cụ hỗ trợ phân tích và đưa ra gợi ý hiệu quả trong hệ thống mua bán xe máy trực tuyến.
    """)
