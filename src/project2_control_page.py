import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import re

from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

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
        group_xe_theo_dac_diem2()
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

def get_recommendations(df, id, cosine_sim, top_n=3):
    # Trả về top_n xe tương tự dựa trên Cosine Similarity của TF-IDF
    if id not in df['id'].values:
        print(f"Không tìm thấy xe có id '{id}' trong cơ sở dữ liệu.")
        return pd.DataFrame() # Return an empty DataFrame if no match

    idx = df.index[df['id'] == id][0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]

    indices = [i[0] for i in sim_scores]

    result = df.iloc[indices][['id','tieu_de','mo_ta_chi_tiet','thuong_hieu','dong_xe','gia','so_km_da_di','nam_dang_ky']].copy()
    result['similarity'] = [round(i[1], 3) for i in sim_scores]
    return result

# Hiển thị đề xuất ra bảng
def display_recommended_bikes(recommended_bikes, cols=5):
    col1, col2, col3 = st.columns(3)
    for i in range(0, len(recommended_bikes), cols):
        cols = st.columns(cols)
        for j, col in enumerate(cols):
            if i + j < len(recommended_bikes):
                bike = recommended_bikes.iloc[i + j]
                with col:
                    bike_description = bike['mo_ta_chi_tiet']
                    truncated_description = ' '.join(bike_description.split()[:100]) + '...'
                    ui.card(
                        title=f"Xe Máy {i + j + 1}", 
                        content=f"<b>{bike['tieu_de']}</b><br><i>{truncated_description}</i>", 
                        color="#3874b4", icon="🎯")

# PREPROCESS TEXT (same as training)
def clean_text_vn(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|href\S+", " ", text)
    text = re.sub(r"[^0-9a-zA-ZÀ-ỹ\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Hàm load mô hình và dữ liệu đã lưu
def load_models():
    df = pd.read_csv("./data/data_motobikes_cleaned_content_wt.csv")   # UPDATE path if needed

    with open("./models/tfidf_vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)

    with open("./models/tfidf_matrix.pkl", "rb") as f:
        tfidf_matrix = pickle.load(f)

    with open("./models/cosine_sim.pkl", "rb") as f:
        cosine_sim = pickle.load(f)

    return df, vectorizer, tfidf_matrix, cosine_sim

# Hàm đề xuất xe tương đồng với "Nội dung nhập vào"
def recommend_from_query(query_text, df, vectorizer, tfidf_matrix, top_n=5):

    clean_query = clean_text_vn(query_text)

    q_vec = vectorizer.transform([clean_query])
    sim_scores = cosine_similarity(q_vec, tfidf_matrix).flatten()

    top_idx = sim_scores.argsort()[::-1][:top_n]

    result = df.iloc[top_idx][[
        'id', 'tieu_de', 'thuong_hieu', 'dong_xe', 'gia',
        'so_km_da_di', 'nam_dang_ky', 'xuat_xu'
    ]].copy()

    result["similarity"] = sim_scores[top_idx].round(4)

    return result.reset_index(drop=True)

# ============================================================
# 3. CÁC HÀM XỬ LÝ THEO LỰA CHỌN Ở MENU
# ============================================================

def de_xuat_theo_id():
    ui.centered_text("Đề xuất [n] xe máy theo ID", color="#1f77b4", size="36px")
    # ui.colored_text("Đề xuất [n] xe máy theo ID", color="#1f77b4", size="32px", bold=True, italic=False)

    # Đọc dữ liệu từ file data_motobikes_cleaned.csv        
    df_bikes = load_data("./data/data_motobikes_cleaned.csv")   

    # Lấy 10 mẫu xe máy
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
        "Hãy chọn xe máy bạn quan tâm:",
        options=bike_options,
        format_func=lambda x: x[0]  # Hiển thị tên xe máy
    )
    # Display the selected bike
    # st.write("Bạn đã chọn:", selected_bike)

    # Cập nhật session_state dựa trên lựa chọn hiện tại
    st.session_state.selected_bike_id = selected_bike[1]

    # Open and load file to cosine_sim_new
    with open('./models/cosine_sim.pkl', 'rb') as f:
        cosine_sim_new = pickle.load(f)

    if st.session_state.selected_bike_id:
        # ui.badge("bike_ID: " + str(st.session_state.selected_bike_id), color="#007bff")
        # st.write("bike_ID: ", st.session_state.selected_bike_id)
        # Hiển thị thông tin xe máy được chọn
        selected_bike = df_bikes[df_bikes['id'] == st.session_state.selected_bike_id]

        if not selected_bike.empty:
            bike_description = selected_bike['mo_ta_chi_tiet'].values[0]
            # truncated_description = ' '.join(bike_description.split()[:100]) + '...'

            # ui.colored_text("Xe máy được chọn", color="#1f77b4", size="32px", bold=True, italic=False)
            ui.section_title("Xe máy được chọn " + f"(ID: {str(st.session_state.selected_bike_id)})", selected_bike['tieu_de'].values[0], "Thông tin: " + bike_description)           
                        
            st.write("---")
            ui.colored_text("🔍 Các xe máy khác bạn cũng có thể quan tâm:", color="#ce7018", size="28px", bold=True, italic=False)            

            recommendations = get_recommendations(df_bikes, st.session_state.selected_bike_id, cosine_sim=cosine_sim_new, top_n=3) 
            display_recommended_bikes(recommendations, cols=3)
        else:
            st.write(f"Không tìm thấy xe máy với ID: {st.session_state.selected_bike_id}")

    def de_xuat_theo_query():    
        st.subheader("Đề xuất n xe máy theo yêu cầu người dùng nhập")

    def group_xe_theo_dac_diem():    
        st.subheader("Nhóm các xe máy theo đặc điểm chung")


def de_xuat_theo_query():    
    ui.centered_text("Gợi ý xe dựa trên mô tả", color="#1f77b4", size="36px")
    st.write("Nhập mô tả xe bạn muốn tìm, hệ thống sẽ gợi ý những xe phù hợp nhất.")

    # Load model & data
    df, vectorizer, tfidf_matrix, cosine_sim = load_models()

    # Input box
    query = st.text_input(
        "Nhập mô tả xe:",
        placeholder="Ví dụ: xe SH Việt Nam giá khoảng 65000000",
        value="xe SH Việt Nam giá khoảng 65000000",
    )

    # Top-N slider
    top_n = st.slider("Số lượng gợi ý muốn xem:", 3, 10, 5)

    # Button
    if st.button("🔍 Gợi ý ngay"):
        if query.strip() == "":
            st.warning("⚠ Vui lòng nhập mô tả trước khi tìm kiếm.")
        else:
            st.write("### 📌 Kết quả gợi ý:")
            result = recommend_from_query(query, df, vectorizer, tfidf_matrix, top_n)

            # Format clickable link
            def linkify(url):
                return f"[Mở tin đăng]({url})"

            st.dataframe(result[[
                "id", "tieu_de", "thuong_hieu", "dong_xe", "gia",
                "similarity"
            ]])

def group_xe_theo_dac_diem():
    ui.centered_text("Nhóm các xe máy theo đặc điểm kỹ thuật chung", color="#1f77b4", size="36px")    
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    

    # =====================================================
    # STREAMLIT UI – PCA CLUSTER DEMO
    # =====================================================

    ui.colored_text("PCA Scatter Plot – Demo Cluster (K=4)", color="#111111", size="32px", bold=True)        
    st.write("Trực quan hóa phân cụm xe theo đặc điểm kỹ thuật (Demo K=4).")

    # ============================
    # STEP 1 — Upload File
    # ============================
    """
    uploaded_file = st.file_uploader(
        "Upload file data_motobikes_cleaned.csv",
        type=["csv"]
    )

    if uploaded_file is None:
        st.warning("⚠ Vui lòng upload file CSV để tiếp tục.")
        st.stop()
    """
    
    uploaded_file = "./data/data_motobikes_cleaned_content_wt.csv"
    # Load dataframe
    df = pd.read_csv(uploaded_file)
    # st.success("📁 File đã được tải lên thành công!")

    # ============================
    # STEP 2 — Select numeric features
    # ============================
    st.subheader("🧮 Chọn các thuộc tính numeric để phân cụm")

    num_cols_default = ["gia", "so_km_da_di", "nam_dang_ky"]
    num_cols = st.multiselect(
        "Chọn cột numeric:",
        options=df.columns.tolist(),
        default=num_cols_default
    )

    if len(num_cols) < 2:
        st.error("⚠ Cần chọn ít nhất 2 cột numeric!")
        st.stop()

    X = df[num_cols].fillna(0)

    # ============================
    # STEP 3 — Normalize
    # ============================
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ============================
    # STEP 4 — KMeans (Demo K=4)
    # ============================
    k = 4
    kmeans = KMeans(n_clusters=k, random_state=42)
    df["cluster_demo"] = kmeans.fit_predict(X_scaled)

    # ============================
    # STEP 5 — PCA Projection
    # ============================
    pca = PCA(n_components=2, random_state=42)
    pca_comp = pca.fit_transform(X_scaled)
    df["pca1"] = pca_comp[:, 0]
    df["pca2"] = pca_comp[:, 1]

    # ============================
    # STEP 6 — Scatter Plot PCA
    # ============================
    st.subheader("📈 PCA Scatter Plot Visualization")

    fig, ax = plt.subplots(figsize=(10, 7))
    colors = ["red", "green", "blue", "purple"]

    for cluster_id, color in zip(sorted(df["cluster_demo"].unique()), colors):
        subset = df[df["cluster_demo"] == cluster_id]
        ax.scatter(subset["pca1"], subset["pca2"], 
                s=25, alpha=0.7, label=f"Cluster {cluster_id}", color=color)

    ax.set_title("PCA Scatter Plot – Demo Market Segmentation (K=4)", fontsize=14)
    ax.set_xlabel("PCA Component 1")
    ax.set_ylabel("PCA Component 2")
    ax.legend()
    ax.grid(alpha=0.2)

    st.pyplot(fig)

    # ============================
    # STEP 7 — Cluster Statistics
    # ============================
    st.subheader("📊 Thống kê theo cụm")

    cluster_summary = df.groupby("cluster_demo")[num_cols].mean().round(2)
    st.dataframe(cluster_summary)

    # ============================
    # STEP 8 — Sample of each cluster
    # ============================
    st.subheader("📌 Ví dụ một vài xe trong từng cụm")

    for c in sorted(df["cluster_demo"].unique()):
        st.markdown(f"### 🔹 Cluster {c}")
        st.dataframe(df[df["cluster_demo"] == c].head(5)[["tieu_de", "thuong_hieu", "dong_xe", "gia"]])

def group_xe_theo_dac_diem2():
    import streamlit as st
    import pandas as pd
    import numpy as np
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    import matplotlib.pyplot as plt
    import seaborn as sns

    st.set_page_config(page_title="t-SNE Cluster Visualization", layout="wide")

    st.title("🔍 t-SNE Visualization for Motorbike Clustering")
    
    uploaded_file = "./data/data_motobikes_cleaned_content_wt.csv"
    df = pd.read_csv(uploaded_file)    
    st.write(df.head())

    # ==============================
    # 2. Select numeric features
    # ==============================
    st.subheader("⚙️ Select numeric features for visualization")

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    selected_features = st.multiselect(
        "Chọn các cột để chạy PCA + t-SNE:",
        numeric_cols,
        default=numeric_cols[:6]  # chọn một số cột đầu tiên làm mặc định
    )

    cluster_col = st.selectbox(
        "Chọn cột cluster để phân màu:",
        df.columns,
        index=list(df.columns).index("cluster") if "cluster" in df.columns else 0
    )

    if st.button("🚀 Run PCA + t-SNE"):
        if len(selected_features) < 2:
            st.error("⚠️ Cần chọn ít nhất 2 đặc trưng!")
            st.stop()

        X = df[selected_features].fillna(0).values

        # ==============================
        # 3. PCA reduction (50D)
        # ==============================
        st.write("🔄 Running PCA...")
        pca = PCA(n_components=min(50, X.shape[1]), random_state=42)
        X_pca = pca.fit_transform(X)

        # ==============================
        # 4. t-SNE Reduction
        # ==============================
        perplexity = st.slider("Perplexity", 5, 50, 30)

        st.write("🎨 Running t-SNE (this may take a moment)...")
        tsne = TSNE(
            n_components=2,
            perplexity=perplexity,
            learning_rate="auto",
            init="pca",
            random_state=42
        )

        X_tsne = tsne.fit_transform(X_pca)

        tsne_df = pd.DataFrame({
            "tsne_1": X_tsne[:, 0],
            "tsne_2": X_tsne[:, 1],
            "cluster": df[cluster_col].astype(str)
        })

        # ==============================
        # 5. Plot t-SNE
        # ==============================
        st.subheader("📌 t-SNE Scatter Plot")

        plt.figure(figsize=(10, 7))
        sns.scatterplot(
            data=tsne_df,
            x="tsne_1",
            y="tsne_2",
            hue="cluster",
            palette="tab10",
            s=20,
            alpha=0.8
        )
        plt.title("t-SNE Visualization of Motorbike Clusters")
        plt.xlabel("t-SNE 1")
        plt.ylabel("t-SNE 2")
        plt.legend(title="Cluster")

        st.pyplot(plt)

        # ==============================
        # 6. Show cluster distribution
        # ==============================
        st.subheader("📊 Cluster Distribution")
        st.bar_chart(tsne_df["cluster"].value_counts())
