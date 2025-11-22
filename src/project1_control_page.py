import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

import seaborn as sns
import matplotlib.pyplot as plt
import math

from ui.ui_components import UIComponents

# Set page config
st.set_page_config(layout="wide")

# Khởi tạo class
ui = UIComponents()

def show():    
    # Set page layout    
    ui.set_page_layout(width=960, hide_branding=False)

    # Tạo Menu ở Sidebar
    with st.sidebar:
        # st.title("Điều hướng")
        selected_page = st.radio(                        
            "Chọn chức năng:",
            ["Dự đoán giá xe", "Phát hiện xe bất thường", "Thống kê xe bất thường", "Quản lý Tin Bất Thường"]
        )
    
    # Routing logic (Gọi hàm tương ứng theo lựa chọn)
    if selected_page == "Dự đoán giá xe":
        du_doan_gia_xe()
    elif selected_page == "Phát hiện xe bất thường":
        phat_hien_xe_bat_thuong()
    elif selected_page == "Thống kê xe bất thường":
        # list_xe_bat_thuong()
        xe_bat_thuong_dashboard()
        # main_price_dashboard()
    elif selected_page == "Quản lý Tin Bất Thường":        
        quan_ly_tin_bat_thuong()

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

def prepare_input(input_dict, features):
    df = pd.DataFrame([{f: input_dict.get(f, np.nan) for f in features}])

    # numeric auto convert
    numeric_cols = ['so_km_da_di','nam_dang_ky']
    for c in numeric_cols:
        if c in df:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # categorical auto fill
    cat_cols = ['thuong_hieu','dong_xe','tinh_trang','loai_xe','dung_tich_xe', 'xuat_xu']
    for c in cat_cols:
        df[c] = df[c].fillna('unknown').astype(str)


    # Filll any all-NaN numeric → 0
    for c in df.columns:
        if df[c].dtype.kind in 'fiu' and df[c].isna().all():
            df[c] = df[c].fillna(0)
    
    return df

# --- Predict price -----------------------------------------------
def predict_price(info, model, features=None, inverse_log=True):
    
    if features is None:
        features = [
            'thuong_hieu','dong_xe', 'nam_dang_ky','so_km_da_di',
            'tinh_trang','loai_xe','dung_tich_xe','xuat_xu'
        ]        

    df = prepare_input(info, features)

    try:
        pred = model.predict(df)[0]
    except Exception as e:
        raise RuntimeError(f"Predict failed: {e}\nInput:\n{df}")

    return float(np.expm1(pred) if inverse_log else pred)

# Hàm phân trang
def paginate_dataframe(df, rows_per_page=15):
    total_rows = len(df)
    total_pages = (total_rows // rows_per_page) + (1 if total_rows % rows_per_page != 0 else 0)

    page = st.number_input(
        "Trang", min_value=1, max_value=total_pages, value=1, step=1
    )

    start_idx = (page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page

    return df.iloc[start_idx:end_idx], total_pages, page


# ==============================
# DASHBOARD ANOMALY FULL
# ==============================
def xe_bat_thuong_dashboard():
    # st.title("Dashboard Phát Hiện Xe Máy Bất Thường")
    ui.centered_text("Thống kê danh sách xe máy bất thường", color="#1f77b4", size="36px")

    # Load dữ liệu bất thường
    df_results = pd.read_csv("./data/results_with_anomalies.csv")

    if "anomaly_flag" not in df_results:
        st.error("File results_with_anomalies.csv không chứa trường anomaly_flag!")
        return
    
    df_anom = df_results[df_results["anomaly_flag"] == 1]

    st.markdown(f"""
        ### 🔎 Tổng Quan Bất Thường
        - ##### Tổng số xe bất thường: `{len(df_anom)} xe`
        - ##### Tỉ lệ bất thường: `{len(df_anom) / len(df_results) * 100:.2f}%`
    """)

    col1, col2 = st.columns(2)

    with col1:
        # HISTOGRAM ANOMALY SCORE
        st.write("##### Phân bố điểm bất thường (Anomaly Score)")

        fig, ax = plt.subplots(figsize=(7,4))
        sns.histplot(df_anom["anomaly_score"], kde=True, bins=20, ax=ax)
        ax.set_xlabel("Anomaly Score (0 - 100)")
        st.pyplot(fig)

        #st.divider()
    
    with col2:    
        # SCATTER (ACTUAL vs PREDICTED)    
        st.write("##### Scatter Plot: Giá thực tế vs Giá dự đoán")

        fig, ax = plt.subplots(figsize=(6,6))
        ax.scatter(df_anom["gia_pred"], df_anom["gia_actual"], alpha=0.6)

        # đường y=x
        m = max(df_anom["gia_pred"].max(), df_anom["gia_actual"].max())
        ax.plot([0, m], [0, m], linestyle="--", color="red")

        ax.set_xlabel("Giá dự đoán (VNĐ)")
        ax.set_ylabel("Giá thực tế (VNĐ)")
        ax.set_title("Giá bất thường nằm xa đường y = x")
        st.pyplot(fig)

    st.divider()
    
    # DANH SÁCH XE BẤT THƯỜNG (PHÂN TRANG)
    st.subheader("📋 Danh sách xe bất thường")

    df_page, total_pages, current_page = paginate_dataframe(df_anom, rows_per_page=15)

    st.write(f"Trang {current_page}/{total_pages}")
    st.dataframe(df_page[['thuong_hieu','dong_xe','nam_dang_ky','so_km_da_di','dung_tich_xe','xuat_xu', 
                          'gia_actual','gia_pred','residual','residual_z','outside_p10p90','p10','p90', 
                          'iso_score_raw','lof_score_raw','resid_flag_cheap','resid_flag_expensive',
                          'resid_score_raw','resid_score','iso_score','lof_score','p10p90_score','anomaly_score']])    
    
    st.divider()

def quan_ly_tin_bat_thuong():
    ui.centered_text("🛡️ Admin - Quản lý tin bất thường", color="#1f77b4", size="36px")

    # Load dữ liệu bất thường
    df_results = pd.read_csv("./data/results_with_anomalies.csv")
    admin_page(df_results)

def paginate(df, page, page_size=15):
    """
    Phân trang dataframe df.
    page: số trang (1-based)
    page_size: số dòng mỗi trang
    return: df_page
    """
    if df is None or len(df) == 0:
        return df

    total_rows = len(df)
    total_pages = math.ceil(total_rows / page_size)

    # đảm bảo page hợp lệ
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    start = (page - 1) * page_size
    end = start + page_size
    return df.iloc[start:end]

# ---------------------------
# ADMIN PAGE
# ---------------------------
def admin_page(df_results):
    # st.title("🛡️ Admin – Quản lý Tin Bất Thường")
    st.markdown("Quản lý, lọc, duyệt và ghi log các tin rao bất thường")

    # basic KPI
    total = len(df_results)
    anomalies = df_results[df_results["anomaly_flag"] == 1]
    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng tin", total)
    col2.metric("Tổng tin bất thường", len(anomalies))
    col3.metric("Tỉ lệ", f"{len(anomalies)/max(1,total)*100:.2f}%")

    st.markdown("---")
    st.header("Bộ lọc")
    brand_list = df_results["thuong_hieu"].dropna().unique().tolist() if "thuong_hieu" in df_results.columns else []
    chosen_brands = st.multiselect("Thương hiệu", options=brand_list)
    score_min = st.slider("Anomaly score tối thiểu", 0, 100, 10)
    anomaly_types = st.multiselect("Loại bất thường", options=["Rẻ bất thường","Đắt bất thường","Khác"], default=None)

    # compute type column if not present
    if "type" not in df_results.columns:
        def _type(r):
            try:
                if r.get("residual",0) < 0: return "Rẻ bất thường"
                if r.get("residual",0) > 0: return "Đắt bất thường"
            except: pass
            return "Khác"
        df_results["type"] = df_results.apply(_type, axis=1)

    df_filtered = df_results.copy()
    if chosen_brands:
        df_filtered = df_filtered[df_filtered["thuong_hieu"].isin(chosen_brands)]
    df_filtered = df_filtered[df_filtered["anomaly_score"] >= score_min]
    if anomaly_types:
        df_filtered = df_filtered[df_filtered["type"].isin(anomaly_types)]

    st.write(f"Tin tìm thấy: **{len(df_filtered)}**")

    # pagination controls
    page_size = 15
    total_pages = math.ceil(len(df_filtered)/page_size) if len(df_filtered)>0 else 1
    if "admin_page_num" not in st.session_state:
        st.session_state.admin_page_num = 1
    cols = st.columns([1,1,1,6])
    with cols[0]:
        if st.button("⟵ Prev"):
            if st.session_state.admin_page_num > 1:
                st.session_state.admin_page_num -= 1
    with cols[1]:
        if st.button("Next ⟶"):
            if st.session_state.admin_page_num < total_pages:
                st.session_state.admin_page_num += 1
    with cols[2]:
        if st.button("Reset"):
            st.session_state.admin_page_num = 1

    page = st.session_state.admin_page_num
    df_page = paginate(df_filtered.reset_index(drop=True), page, page_size)
    st.write(f"Trang {page}/{total_pages}")
    st.dataframe(df_page, use_container_width=True, height=420)

    st.markdown("---")
    st.header("Duyệt tin chi tiết")
    idx = st.number_input("Index trong bảng (index trang)", min_value=0, max_value=max(0,len(df_page)-1), value=0)
    if len(df_page)>0:
        row = df_page.iloc[int(idx)].to_dict()
        st.json(row)
        label = st.radio("Đánh dấu tin này:", ["Hợp lệ","Không hợp lệ","Lừa đảo"])
        remark = st.text_area("Ghi chú (tuỳ chọn)")
        if st.button("Lưu đánh dấu"):
            # Lưu nhãn & ghi log (append csv)
            log_row = {**row, "admin_label": label, "admin_remark": remark}
            try:
                log_df = pd.DataFrame([log_row])
                log_df.to_csv("./data/anomaly_admin_log.csv", mode="a", header=not pd.io.common.file_exists("./data/anomaly_admin_log.csv"), index=False)
                st.success("Đã lưu đánh dấu admin.")
            except Exception as e:
                st.error(f"Lưu log thất bại: {e}")

# =============================================================

def du_doan_gia_xe():    
    ui.centered_text("Dự đoán giá xe máy", color="#1f77b4", size="36px")

    
    # Đọc dữ liệu từ file data_motobikes_cleaned.csv        
    df = load_data("./data/data_motobikes_cleaned.csv")   
    
    global df_data
    df_data = df  # gán dataframe toàn cục

    # st.write("##### Dữ liệu mẫu sau khi tiền xử lý")
    # ['thuong_hieu','dong_xe','nam_dang_ky','so_km_da_di','tinh_trang','loai_xe','dung_tich_xe','xuat_xu']    
    # st.dataframe(df[['gia','tieu_de','thuong_hieu','dong_xe','loai_xe','dung_tich_xe','so_km_da_di','nam_dang_ky']].head())

    # Load model từ file pickle
    model_regression_best = load_model("./models/model_regression_best.pkl")

    # Trường hợp 2: Đọc dữ liệu từ file csv, excel do người dùng tải lên
    """
    st.write("### Đọc dữ liệu từ file csv do người dùng tải lên")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])   
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Dữ liệu đã nhập:")
        st.dataframe(df.head())
    st.write("### 1. Dự đoán giá xe máy cũ")
    """
    
    st.write("---")
    ui.centered_text("Chọn thông tin cho xe cần dự đoán giá", color="#1f77b4", size="28px")
    
    # Tạo điều khiển để người dùng nhập các thông tin về xe máy
    thuong_hieu = st.selectbox("Chọn hãng xe", df['thuong_hieu'].unique())
    dong_xe = st.selectbox("Chọn dòng xe", df['dong_xe'].unique())    
    loai_xe = st.selectbox("Chọn loại xe", df['loai_xe'].unique())
    tinh_trang = st.selectbox("Chọn tình trạng", df['tinh_trang'].unique())
    dung_tich_xi_lanh = st.selectbox("Dung tích xi lanh (cc)", df['dung_tich_xe'].unique())    
    
    nam_dk_min = int(df['nam_dang_ky'].min())
    nam_dk_max = int(df['nam_dang_ky'].max())
    nam_dang_ky = st.slider("Năm đăng ký", nam_dk_min, nam_dk_max, 2010)

    so_km_min = int(df['so_km_da_di'].min())
    so_km_max = int(df['so_km_da_di'].max())
    so_km_da_di = st.number_input("Số km đã đi", min_value=so_km_min, max_value=so_km_max, value=50000, step=1000)

    xuat_xu = st.selectbox("Xuất xứ", df['xuat_xu'].unique())    
    
    # Button dự đoán giá
    du_doan_gia = st.button("💰 Dự đoán giá")
        
    if du_doan_gia:
        st.write("---")
        ui.centered_text("Kết quả dự đoán giá xe máy cũ", color="#1f77b4", size="28px")

        # Thực hiện dự đoán giá khi nhấn nút    
        input_vehicle = {
            'thuong_hieu': thuong_hieu,
            'dong_xe': dong_xe,
            'loai_xe': loai_xe,
            'dung_tich_xe': dung_tich_xi_lanh,
            'so_km_da_di': so_km_da_di,
            'nam_dang_ky': nam_dang_ky,
            'xuat_xu': xuat_xu,
            'tinh_trang': tinh_trang
        }

        # Dự đoán giá
        try:
            gia_du_doan = predict_price(input_vehicle, model_regression_best)            
        except Exception as e:            
            st.error(f"Lỗi trong quá trình dự đoán: {e}")
            return
        # In ra các thông tin đã chọn
        ui.styled_table(
            headers=["Đặc Trưng", "Giá Trị"],
            rows=[
                ["Hãng xe", thuong_hieu],
                ["Dòng xe", dong_xe],
                ["Loại xe", loai_xe],
                ["Tình trạng xe", tinh_trang],
                ["Dung tích xi lanh", dung_tich_xi_lanh],
                ["Số km đã đi", so_km_da_di],
                ["Năm đăng ký", nam_dang_ky],
                # In đậm giá dự đoán                
                ["**💰 Giá dự đoán**", f"⭐ {gia_du_doan:,.0f} VND ⭐"],
                ["**Gợi ý** giá bán nhanh", f"**{gia_du_doan*0.95:,.0f} VND**"],
                ["**Gợi ý** giá có lợi nhuận tối đa", f"**{gia_du_doan*1.05:,.0f} VND**"],
                ["**Gợi ý** khoảng giá hợp lý", f"**{gia_du_doan*0.9:,.0f} - {gia_du_doan*1.1:,.0f} VND**"],
            ],            
            centered=True
        )

# ============================================================
# HÀM XỬ LÝ PHÁT HIỆN XE BẤT THƯỜNG 
# ============================================================
def detect_anomaly(model, info):
    df = pd.DataFrame([info])
    pred = model.predict(df)[0]
    pred = pred*1_000_000    

    residual = info['gia'] - pred

    # Z-score với sigma giả định
    sigma = 0.15 * pred
    z = residual / sigma

    is_anomaly = abs(z) > 2.5

    return {
        'gia_du_doan': pred,
        'residual': residual,
        'z_score': z,
        'ket_luan': '👎 Giá Bất thường' if is_anomaly else '👍 Giá Bình thường'
    }

def phat_hien_xe_bat_thuong():    
    ui.centered_text("Phát hiện xe máy bất thường", color="#1f77b4", size="36px")
    
    # Đọc dữ liệu từ df_data toàn cục        
    df = df_data

    # st.write("##### Dữ liệu mẫu sau khi tiền xử lý")
    # st.dataframe(df[['gia','tieu_de','thuong_hieu','dong_xe','loai_xe','dung_tich_xe','so_km_da_di','nam_dang_ky']].head())

    # Load model từ file pickle    
    model_best = load_model("./models/model_regression_best.pkl")

    st.write("---")

    ui.centered_text("Nhập thông tin cho xe cần kiểm tra", color="#1f77b4", size="28px")

    # Tạo điều khiển để người dùng nhập các thông tin về xe máy
    thuong_hieu = st.selectbox("Chọn hãng xe", df['thuong_hieu'].unique())
    dong_xe = st.selectbox("Chọn dòng xe", df['dong_xe'].unique())    
    loai_xe = st.selectbox("Chọn loại xe", df['loai_xe'].unique())
    tinh_trang = st.selectbox("Chọn tình trạng", df['tinh_trang'].unique())
    dung_tich_xi_lanh = st.selectbox("Dung tích xi lanh (cc)", df['dung_tich_xe'].unique())    
    
    nam_dk_min = int(df['nam_dang_ky'].min())
    nam_dk_max = int(df['nam_dang_ky'].max())
    nam_dang_ky = st.slider("Năm đăng ký", nam_dk_min, nam_dk_max, 2020)

    so_km_min = int(df['so_km_da_di'].min())
    so_km_max = int(df['so_km_da_di'].max())
    so_km_da_di = st.number_input("Số km đã đi", min_value=so_km_min, max_value=so_km_max, value=25000, step=1000)
    gia_ban = st.number_input("Giá bán (VND)", min_value=3000000, max_value=999000000, value=20000000, step=1000000)

    xuat_xu = st.selectbox("Xuất xứ", df['xuat_xu'].unique())

    # Button dò tìm bất thường
    kiem_tra_bat_thuong = st.button("🔍 Kiểm tra bất thường")

    if kiem_tra_bat_thuong:
        # Input tin đăng
        input_xe = {
            'thuong_hieu': thuong_hieu,
            'dong_xe': dong_xe,
            'loai_xe': loai_xe,
            'dung_tich_xe': dung_tich_xi_lanh,
            'so_km_da_di': so_km_da_di,
            'nam_dang_ky': nam_dang_ky,
            'xuat_xu': xuat_xu,
            'tinh_trang': tinh_trang,
            'gia': gia_ban,  # giá người bán đưa ra
        }
        
        # Dò tìm bất thường    
        ketqua = detect_anomaly(model_best, input_xe)

        st.write("---")
        ui.centered_text("Kết quả phát hiện xe máy bất thường", color="#1f77b4", size="28px")
        ui.styled_table(
            headers=["Đặc Trưng", "Giá Trị"],
            rows=[
                ["Hãng xe", thuong_hieu],
                ["Dòng xe", dong_xe],
                ["Loại xe", loai_xe],
                ["Tình trạng xe", tinh_trang],
                ["Dung tích xi lanh", dung_tich_xi_lanh],
                ["Số km đã đi", so_km_da_di],
                ["Năm đăng ký", nam_dang_ky],
                ["Giá bán (VND)", f"{gia_ban:,.0f} VND"],
                # In đậm kết quả dự đoán
                ["**Giá dự đoán (VND)**", f"**{ketqua['gia_du_doan']:,.0f} VND**"],
                ["**Residual (VND)**", f"**{ketqua['residual']:,.0f} VND**"],
                ["**Z-score**", f"**{ketqua['z_score']:.2f}**"],
                ["**Kết luận**", f"**{ketqua['ket_luan']}**"],
            ],        
            centered=True
        )

# ============================================================
# HÀM LIỆU KÊT DANH SÁCH XE BẤT THƯỜNG
# ============================================================

def list_xe_bat_thuong():    
    ui.centered_text("Thống kê danh sách xe máy bất thường", color="#1f77b4", size="36px")

    # Load dư liệu từ file results_with_anomalies.csv
    df_results = pd.read_csv("./data/results_with_anomalies.csv")    
    data_anomalies = df_results[df_results['anomaly_flag'] == 1]
    tong_so_xe_bat_thuong = len(data_anomalies)

    st.write(f"##### Tổng số xe máy bất thường: {tong_so_xe_bat_thuong} xe")    
    # st.dataframe(data_anomalies, height=2600)
    st.dataframe(data_anomalies, height=600)
