import streamlit as st
from ui.ui_components import UIComponents

st.set_page_config(page_title="Capstone Project – Giá Xe Máy", layout="wide")

def show():
    # Set page layout    
    UIComponents.set_page_layout(width=960, hide_branding=False)
    
    # ============================================================
    # TITLE
    # ============================================================
    # st.title("CAPSTONE PROJECT – Dự đoán Giá Xe Máy & Phát hiện Giá Bất Thường")
    UIComponents.centered_title("Capstone Project", "Dự đoán Giá Xe Máy & Phát hiện Giá Bất Thường")
    st.write("---")

    # ============================================================
    # INTRO
    # ============================================================
    st.header("1. Giới thiệu")
    st.markdown("""
    Dự án tập trung phân tích và mô hình hoá dữ liệu **xe máy đã qua sử dụng từ Chợ Tốt**, 
    nhằm giải quyết hai bài toán quan trọng:

    ### 🔹 Bài toán 1 – *Price Prediction*
    Dự đoán **giá hợp lý** của một chiếc xe máy dựa trên thông tin đầu vào  
    (như thương hiệu, dòng xe, loại xe, dung tích xe, năm đăng ký, số km đã đi...).

    ### 🔹 Bài toán 2 – *Price Anomaly Detection*
    Xác định mức giá người dùng đưa vào **có bất thường hay không**, 
    dựa trên mô hình phát hiện anomaly.
    """)

    st.write("---")

    # ============================================================
    # PROJECT STRUCTURE
    # ============================================================
    st.header("2. Cấu trúc dự án")
    st.code("""
    project/
    │
    ├── Data/
    │   ├── raw_data.xlsx
    │   ├── cleaned_data.csv
    │   ├── model_regression_best.pkl
    │   ├── model_anomaly_best.pkl
    │
    ├── scripts/
    │   ├── EDA.ipynb
    │   ├── train_regression.ipynb
    │   ├── train_anomaly.ipynb
    │   ├── predict_price.py
    │   ├── predict_anomaly.py
    │
    ├── README.md
    """, language="text")

    st.write("---")

    # ============================================================
    # DATA PREPROCESSING
    # ============================================================
    st.header("3. Tiền xử lý dữ liệu")
    st.markdown("""
    Các bước xử lý dữ liệu chính:

    ### ✔ Làm sạch dữ liệu
    - Chuẩn hóa văn bản (thương hiệu, dòng xe, mô tả)
    - Xử lý ký tự đặc biệt, viết tắt, lỗi chính tả

    ### ✔ Xử lý biến categorical
    - One-Hot Encoding / Ordinal Encoding
    - Không chuyển `dung_tich_xe` sang số → giữ dạng chuỗi

    ### ✔ Xử lý numeric
    - Chuẩn hóa `so_km_da_di`, `nam_dang_ky`
    - Xử lý ngoại lệ, outlier theo phân phối

    ### ✔ Tạo thêm đặc trưng:
    - tuổi xe (year_now – nam_dang_ky)
    - khoảng giá min/max
    - phân lớp số km
    """)

    st.write("---")

    # ============================================================
    # REGRESSION MODEL
    # ============================================================
    st.header("4. Bài Toán 1 – Dự đoán Giá Xe (Regression)")

    st.subheader("Mục tiêu")
    st.markdown("""
    Dự đoán **giá bán hợp lý** dựa trên 8 trường thông tin:

    | Trường | Ý nghĩa |
    |--------|---------|
    | thuong_hieu | Honda, Yamaha... |
    | dong_xe | Air Blade, Vision... |
    | loai_xe | tay ga, xe số... |
    | dung_tich_xe | giữ dạng chuỗi (vd: "100 - 175 cc") |
    | so_km_da_di | số km đã chạy |
    | nam_dang_ky | năm đăng ký |
    | xuat_xu | Việt Nam, nhập khẩu |
    | tinh_trang | Cũ, mới |
    """)

    st.subheader("💡 Mô hình tốt nhất")
    st.markdown("""
    - **LightGBM Regressor** hoặc **XGBoost Regressor**
    - Dự đoán trên target đã chuẩn hoá: `log1p(gia)`
    - Sai số MAPE: **~8–12%**
    """)

    st.subheader("Hàm dự đoán giá (Price Prediction)")
    st.code("""
    def predict_price(info, model_path, features=None, inverse_log=True):
        if not os.path.exists(model_path):
            raise FileNotFoundError(model_path)

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        if features is None:
            try:
                features = model.named_steps["preprocessor"].feature_names_in_.tolist()
            except:
                features = [
                    'thuong_hieu','dong_xe','nam_dang_ky','so_km_da_di',
                    'tinh_trang','loai_xe','dung_tich_xe','xuat_xu'
                ]

        df = prepare_input(info, features)

        try:
            pred = model.predict(df)[0]
        except Exception as e:
            raise RuntimeError(f"[Predict Error] {e}\\nDF:\\n{df}")

        return float(np.expm1(pred) if inverse_log else pred)
    """, language="python")

    st.subheader("📝 Ví dụ dự đoán")
    st.code("""
    input_vehicle = {
        'thuong_hieu': 'Honda',
        'dong_xe': 'Air Blade',
        'loai_xe': 'Xe tay ga',
        'dung_tich_xe': '100 - 175 cc',
        'so_km_da_di': 25000,
        'nam_dang_ky': 2019,
        'xuat_xu': 'Việt Nam'
    }

    price = predict_price(input_vehicle, "./Data/model_regression_best.pkl")
    print(f"Giá dự đoán: {price:,.0f} VND")
    """, language="python")

    st.subheader("Lưu kết quả dự đoán – `regression_predictions.csv`")
    st.code("""
    df_save = pd.DataFrame([input_vehicle])
    df_save['gia_du_doan'] = price
    df_save.to_csv("regression_predictions.csv", index=False)
    """, language="python")

    st.write("---")

    # ============================================================
    # ANOMALY DETECTION
    # ============================================================
    st.header("5. Bài Toán 2 – Phát hiện Giá Bất Thường (Anomaly Detection)")

    st.subheader("Mục tiêu")
    st.markdown("""
    Xác định giá rao bán có:
    - **Bình thường (NORMAL)**
    - **Bất thường (ANOMALY)**  
    Dựa vào mô hình học không giám sát.
    """)

    st.subheader("💡 Mô hình tốt nhất")
    st.markdown("""
    - **Isolation Forest**
    - hoặc AutoEncoder Tree-Based
    """)

    st.subheader("Hàm kiểm tra giá bất thường")
    st.code("""
    def detect_price_anomaly(info, model_path, threshold=0.5):
        with open(model_path, "rb") as f:
            model = pickle.load(f)

        df = prepare_input(info, model.feature_names_in_)

        score = -model.decision_function(df)[0]
        label = "ANOMALY" if score > threshold else "NORMAL"

        return score, label
    """, language="python")

    st.subheader("📝 Ví dụ chạy anomaly detection")
    st.code("""
    input_vehicle = {
        'thuong_hieu': 'Honda',
        'dong_xe': 'Vision',
        'loai_xe': 'Xe tay ga',
        'dung_tich_xe': '50 - 100 cc',
        'so_km_da_di': 15000,
        'gia': 55_000_000
    }

    score, label = detect_price_anomaly(input_vehicle, "./Data/model_anomaly_best.pkl")
    print("Kết luận:", label)
    """, language="python")

    st.write("---")

    # ============================================================
    # MODEL EVALUATION
    # ============================================================
    st.header("5. Đánh giá mô hình")
    st.markdown("""
    ### **Regression**
    - RMSE  
    - MAE  
    - MAPE  
    - R²  

    ### **Anomaly Detection**
    - Precision / Recall anomaly  
    - ROC-AUC  
    - Biểu đồ phân phối anomaly score  
    """)

    st.write("---")

    # ============================================================
    # STREAMLIT UI
    # ============================================================
    st.header("6. Giao diện Streamlit")
    st.markdown("""
    Ứng dụng Streamlit bao gồm:

    - Form nhập thông tin xe → dự đoán giá  
    - Form nhập thông tin xe + giá → kiểm tra bất thường  
    - Cho phép tải xuống file CSV  
    - Hiển thị biểu đồ phân phối giá theo thị trường  
    """)

    st.write("---")

    # ============================================================
    # CONCLUSION
    # ============================================================
    st.header("🎯 7. Kết luận")
    st.markdown("""
    Dự án hoàn thành các mục tiêu đề ra:

    ### ✔ Dự đoán giá xe chính xác ~90%  
    Hỗ trợ người mua/bán xác định giá hợp lý.

    ### ✔ Phát hiện giá bất thường hiệu quả  
    Lọc tin rao sai lệch, phát hiện giá ảo, lừa đảo.
    """)
