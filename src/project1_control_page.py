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

# ============================================================
# HÀM LOAD DATA VÀ MODELS
# ============================================================
@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
        
    df = pd.read_csv(file_path)
    return df

@st.cache_resource
def load_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(model_path)

    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Load ngay khi import module
data = load_data("./data/data_motobikes_cleaned.csv")
model = load_model("./models/model_regression_best.pkl")

# ============================================================
# CÁC HÀM TIỆN ÍCH & STYLE
# ============================================================
def format_vnd(x):
    try:
        return f"{int(x):,} VND"
    except:
        return str(x)

def suggest_price(g):
    return dict(
        recommended=g,
        fast_sell=int(g*0.95),
        max_profit=int(g*1.05),
        fair_low=int(g*0.9),
        fair_high=int(g*1.1),
        fair_min=int((g*0.9)-(g/2)),
        fair_max=int((g*1.1)+(g/2)),
    )

# ============================================================
# HÀM MAIN SHOW & INIT
# ============================================================
def show():
    # Set page layout    
    ui.set_page_layout(width=960, hide_branding=False)

    # Tạo Menu ở Sidebar
    with st.sidebar:
        # st.title("Điều hướng")
        selected_page = st.radio(                        
            "Chọn chức năng:",
            ["Dự đoán giá xe", "Phát hiện xe bất thường", "Thống kê xe bất thường", "Quản lý tin bất thường"]
        )
    
    # Routing logic (Gọi hàm tương ứng theo lựa chọn)
    if selected_page == "Dự đoán giá xe":
        du_doan_gia_xe(data, model)
    elif selected_page == "Phát hiện xe bất thường":
        phat_hien_xe_bat_thuong(data, model)
    elif selected_page == "Thống kê xe bất thường":
        # list_xe_bat_thuong()
        xe_bat_thuong_dashboard()
        # main_price_dashboard()
    elif selected_page == "Quản lý tin bất thường":        
        quan_ly_tin_bat_thuong()

# ============================================================
# HÀM XỬ LÝ DỰ ĐOÁN GIÁ XE 
# ============================================================
def show_price_suggestion(gia_ban_nhanh, gia_de_xuat, gia_toi_da):
    """Hiển thị toàn bộ phần gợi ý giá bán"""
    
    # Header
    st.markdown("### 💡 Gợi ý giá bán")
    st.markdown("*Chọn mức giá phù hợp với mục tiêu của bạn*")    

    # 3. Cards chi tiết
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                    padding: 15px; border-radius: 5px; border: 2px solid #28a745;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size: 24px; margin-bottom: 5px;">Giá bán nhanh</div>            
            <h2 style="color: #28a745; margin: 0px 0;">{gia_ban_nhanh:,.0f} VNĐ</h2>
            <p style="margin: 5px 0; font-size: 14px; color: #155724;">✅ Giá cạnh tranh tốt</p>
            <p style="margin: 5px 0; font-size: 14px; color: #155724;">✅ Thu hút nhiều người mua</p>            
            <p style="margin: 5px 0; font-size: 14px; color: #856404;">⚠️ Lợi nhuận <b>thấp hơn -5%</b></p>            
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                    padding: 15px; border-radius: 5px; border: 3px solid #ffc107;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15);">
            <div style="font-size: 24px; margin-bottom: 5px;">Giá đề xuất</div>            
            <h2 style="color: #d39e00; margin: 5px 0;">{gia_de_xuat:,.0f} VNĐ</h2>
            <p style="margin: 5px 0; font-size: 14px; color: #856404;">✅ Giá canh tranh công bằng</p>
            <p style="margin: 5px 0; font-size: 14px; color: #856404;">✅ Khách hàng tin tưởng</p>
            <p style="margin: 5px 0; font-size: 14px; color: #28a745; font-weight: bold;">⭐ KHUYẾN NGHỊ</p>             
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
                    padding: 15px; border-radius: 5px; border: 2px solid #dc3545;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-size: 24px; margin-bottom: 5px;">Giá tối đa lợi nhuận</div>            
            <h2 style="color: #dc3545; margin: 5px 0;">{gia_toi_da:,.0f} VNĐ</h2>
            <p style="margin: 5px 0; font-size: 13px; color: #721c24;">✅ Lợi nhuận <b>cao hơn +10%</b></p>
            <p style="margin: 5px 0; font-size: 13px; color: #721c24;">✅ Kén khách mua, bán chậm</p>
            <p style="margin: 5px 0; font-size: 13px; color: #856404;">⚠️ Cần phải có thêm ưu điểm đặc biệt</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")

    # Lưu ý
    st.info("💡 **Lưu ý:** Giá đề xuất (⭐) là mức giá cân bằng tốt nhất giữa tốc độ bán và lợi nhuận, dựa trên phân tích thị trường và đặc điểm xe của bạn.")

def du_doan_gia_xe(df, model_regression_best):    
    # st.markdown("## 💰 Công Cụ Đề Xuất Giá Xe Máy")
    # st.markdown("*Nhập thông tin xe của bạn để nhận được đề xuất giá hợp lý từ hệ thống*")
    ui.centered_title("💰 Đề Xuất Giá Xe Máy","Nhập thông tin xe của bạn để nhận được đề xuất giá hợp lý từ hệ thống")
 
    st.markdown("### 📋 Nhập Thông Tin Xe Của Bạn")

    with st.form("price_form"):
        # Input section with columns
        col1, col2, col3 = st.columns(3)
        with col1:
            thuong_hieu = st.selectbox("⚙️ Chọn hãng xe", df['thuong_hieu'].unique())
            
            so_km_min = int(df['so_km_da_di'].min())
            so_km_max = int(df['so_km_da_di'].max())
            so_km_da_di = st.number_input("🛣️ Số km đã đi", min_value=so_km_min, max_value=so_km_max, value=50000, step=1000)        

        with col2:
            dong_xe = st.selectbox("🏍️ Chọn dòng xe", df['dong_xe'].unique())
            dung_tich_xi_lanh = st.selectbox("🔧 Dung tích xi lanh (cc)", df['dung_tich_xe'].unique())        

        with col3:
            loai_xe = st.selectbox("🛵 Chọn loại xe", df['loai_xe'].unique())
            tinh_trang = st.selectbox("🛡️ Chọn tình trạng", df['tinh_trang'].unique())
        
        col1_ext, col2_ext = st.columns([1, 2])
        with col1_ext:
            xuat_xu = st.selectbox("🏭️ Xuất xứ", df['xuat_xu'].unique(), index=2)
        
        with col2_ext:
            nam_dk_min = int(df['nam_dang_ky'].min())
            nam_dk_max = int(df['nam_dang_ky'].max())
            nam_dang_ky = st.slider("📅 Năm đăng ký", nam_dk_min, nam_dk_max, 2010, label_visibility='visible')

        st.write('')
        # st.divider()

        # Nút Dự đoán và gợi ý giá 
        du_doan_gia_button = st.form_submit_button(f"💰 **Đề Xuất & Gợi ý giá**")
        
    if du_doan_gia_button:
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
        
        # Giá gợi ý
        gia_goi_y = suggest_price(gia_du_doan)
        
        st.write("")

        col1_kq, col2_kq = st.columns([1, 1])
        
        with col1_kq:            
            st.markdown("### ⭐ Kết quả đề xuất giá")
            ui.colored_text(f"{gia_du_doan:,.0f} VND", color="#0d6efd", size="30px", bold=True)            
            
            st.write("##### **✨ Gợi ý giá**")
            st.markdown(f"- Giá bán nhanh: **{format_vnd(gia_goi_y['fast_sell'])}**")
            # st.markdown(f"- Giá đề xuất: **{format_vnd(gia_goi_y['recommended'])}**")
            st.markdown(f"- Giá bán tối đa lợi nhuận: **{format_vnd(gia_goi_y['max_profit'])}**")
            st.markdown(f"- Khoảng giá hợp lý: **{format_vnd(gia_goi_y['fair_low'])} - {format_vnd(gia_goi_y['fair_high'])}**")

        with col2_kq:
            # In ra các thông tin đã chọn
            summary={
                "Hãng xe": thuong_hieu,
                "Dòng xe": dong_xe,
                "Loại xe": loai_xe,
                "Tình trạng xe": tinh_trang,
                "Dung tích xi lanh": dung_tich_xi_lanh,
                "Số km đã đi": so_km_da_di,
                "Năm đăng ký": nam_dang_ky,
                "Giá dự đoán": f"{gia_du_doan:,.0f} VND",
            }            
            st.table(pd.DataFrame(summary.items(), columns=["Đặc Trưng", "Giá Trị"]))
            """
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
                ],            
                centered=True
            )
            """
        st.divider()
        # Hiển thị toàn bộ phần gợi ý giá bán
        show_price_suggestion(gia_goi_y['fast_sell'], gia_du_doan, gia_goi_y['max_profit'])
        
    

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
    col1, col2 = st.columns(2)    
    col1.metric("Tổng tin bất thường", len(anomalies))
    col2.metric("Tỉ lệ", f"{len(anomalies)/max(1,total)*100:.2f}%")

    st.divider()
    st.subheader("Bộ lọc")
    brand_list = df_results["thuong_hieu"].dropna().unique().tolist() if "thuong_hieu" in df_results.columns else []
    chosen_brands = st.multiselect("Thương hiệu", options=brand_list)
    score_min = st.slider("Chỉ sớ bất thường tối thiểu", 0, 100, 10)
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
    page_size = 20
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
    st.dataframe(df_page, use_container_width=True, height=280)

    st.markdown("---")
    st.subheader("Duyệt tin chi tiết")
    idx = st.number_input("Index trong bảng (index trang)", min_value=0, max_value=max(0,len(df_page)-1), value=0)
    if len(df_page)>0:
        row = df_page.iloc[int(idx)].to_dict()
        # st.json(row)
        st.dataframe(row, height=280)
        label = st.radio("Đánh dấu tin này:", ["Hợp lệ","Không hợp lệ","Lừa đảo"])
        remark = st.text_area("Ghi chú (tuỳ chọn)", height=60)
        if st.button("Lưu đánh dấu"):
            # Lưu nhãn & ghi log (append csv)
            log_row = {**row, "admin_label": label, "admin_remark": remark}
            try:
                log_df = pd.DataFrame([log_row])
                log_df.to_csv("./data/anomaly_admin_log.csv", mode="a", header=not pd.io.common.file_exists("./data/anomaly_admin_log.csv"), index=False)
                st.success("Đã lưu đánh dấu admin.")
            except Exception as e:
                st.error(f"Lưu log thất bại: {e}")
            st.dataframe(log_df.head())

# =============================================================



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
        'is_anomaly': is_anomaly,
        'ket_luan': '👎 Giá Bất thường' if is_anomaly else '👍 Giá Bình thường'
    }

def price_competitiveness(actual, predicted, is_anomaly):
    if predicted == 0: return ("Không có dự đoán", 0.0)
    diff_pct = (actual - predicted) / predicted * 100.0
    if diff_pct < 15.7:
        return ("🟢 Rất Rẻ bất thườn tranh (rẻ hơn thị trường)", diff_pct)
    elif diff_pct <= 13.7:
        return ("🟡 Giá hợp lý (gần thị trường)", diff_pct)
    else:
        return ("🔴 Giá cao (cần xem xét)", diff_pct)

def phat_hien_xe_bat_thuong(df, models):    
    # ui.centered_text("Phát hiện xe máy bất thường", color="#1f77b4", size="36px")
    ui.centered_title("Phát hiện xe máy bất thường","Nhập thông tin xe của bạn để kiểm tra giá từ hệ thống")
    
    # st.write("##### Dữ liệu mẫu sau khi tiền xử lý")
    # st.dataframe(df[['gia','tieu_de','thuong_hieu','dong_xe','loai_xe','dung_tich_xe','so_km_da_di','nam_dang_ky']].head())

    # Load model từ file pickle    
    model_best = load_model("./models/model_regression_best.pkl")

    # st.write("---")

    # ui.centered_text("Nhập thông tin cho xe cần kiểm tra bất thường", color="#1f77b4", size="28px")

    """
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
    """
    with st.form("price_form"):
        # Input section with columns
        col1, col2, col3 = st.columns(3)
        with col1:
            thuong_hieu = st.selectbox("⚙️ Chọn hãng xe", df['thuong_hieu'].unique())
            
            so_km_min = int(df['so_km_da_di'].min())
            so_km_max = int(df['so_km_da_di'].max())
            so_km_da_di = st.number_input("🛣️ Số km đã đi", min_value=so_km_min, max_value=so_km_max, value=50000, step=1000)        
            xuat_xu = st.selectbox("🏭️ Xuất xứ", df['xuat_xu'].unique(), index=2)

        with col2:
            dong_xe = st.selectbox("🏍️ Chọn dòng xe", df['dong_xe'].unique())
            dung_tich_xi_lanh = st.selectbox("🔧 Dung tích xi lanh (cc)", df['dung_tich_xe'].unique())
            gia_ban = st.number_input("Giá bán (VND)", min_value=3000000, max_value=999000000, value=20000000, step=1000000)

        with col3:
            loai_xe = st.selectbox("🛵 Chọn loại xe", df['loai_xe'].unique())
            tinh_trang = st.selectbox("🛡️ Chọn tình trạng", df['tinh_trang'].unique())
            nam_dk_min = int(df['nam_dang_ky'].min())
            nam_dk_max = int(df['nam_dang_ky'].max())
            nam_dang_ky = st.slider("📅 Năm đăng ký", nam_dk_min, nam_dk_max, 2010, label_visibility='visible')

        st.write('')
        # st.divider()

        # Nút Dự đoán và gợi ý giá 
        kiem_tra_bat_thuong = st.form_submit_button(f"🔍 **Kiểm tra bất thường**")
        

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

        col1_kq, col2_kq = st.columns([5, 4])
        
        with col1_kq:            
            st.markdown("### ⭐ Kết quả phát hiện bất thường")            
            
            ui.colored_text(f"Giá người bán: {format_vnd(gia_ban)}", color="#0d6efd", size="24px", bold=True)
            ui.colored_text(f"Giá dự đoán: {format_vnd(ketqua['gia_du_doan'])}", color="#e6a824", size="26px", bold=True)

            ui.colored_text(f"Lệch giá: **{ketqua['residual']:,.0f} VND - {ketqua['gia_du_doan']/ketqua['residual']:.1f}%**", color="#f54242", size="20px", bold=False)

            
            if not ketqua['is_anomaly']:
                st.success(f" 🟢 Kết luận: **Giá hợp lý (gần thị trường)**")
                st.write("")
                st.write("##### **✨ Gợi ý**")
                st.write("- Giá phù hợp với các thông tin của đặc điểm .") 
                st.write("- 📩 Nếu bạn là người mua: yêu cầu xem xe, giấy tờ rõ ràng.")
            if ketqua['is_anomaly']:
                if gia_ban > ketqua['gia_du_doan']:
                    st.error(f" 🔴 Kết luận: Giá này **CAO** bất thường so với thị trường. Vui lòng kiểm tra kỹ thông tin.")
                else:
                    st.warning(f" 🟡 Kết luận: Giá này **THẤP** bất thường so với thị trường. Vui lòng kiểm tra kỹ thông tin.")
                    
                st.write("")
                st.write("##### **✨ Gợi ý**")
                st.write("- ⚠️ Kiểm tra nguồn gốc, thông tin các đặc điểm xe, hoặc chỉnh lại giá.")
                st.write("- 📩 Nếu bạn là người mua: trao đổi kỹ, yêu cầu xem xe, giấy tờ rõ ràng.")

        with col2_kq:
            ui.styled_table_small(
                headers=["Đặc Trưng", "Giá Trị"],
                rows=[
                    ["Hãng xe", thuong_hieu],
                    ["Dòng xe", dong_xe],
                    ["Loại xe", loai_xe],
                    ["Tình trạng xe", tinh_trang],
                    ["Dung tích xi lanh", dung_tich_xi_lanh],
                    ["Số km đã đi", so_km_da_di],
                    ["Năm đăng ký", nam_dang_ky],
                    ["Giá người bán", f"{gia_ban:,.0f} VND"],
                    # In đậm kết quả dự đoán
                    ["**Giá dự đoán thị trường**", f"**{ketqua['gia_du_doan']:,.0f} VND**"],                    
                    # ["**Z-score**", f"**{ketqua['z_score']:.2f}**"],
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
