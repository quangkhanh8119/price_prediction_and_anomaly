import streamlit as st
from ui.ui_components import UIComponents

st.set_page_config(page_title="Capstone Project – Giá Xe Máy", layout="wide")

def show():
    # Set page layout    
    UIComponents.set_page_layout(width=960, hide_branding=False)

    # Show logo
    UIComponents.show_logo_conditional('capstone_project2', width=960, centered=False)

    # ============================================================
    # TITLE
    # ============================================================
    # st.title("CAPSTONE PROJECT - Gợi ý xe máy tương đồng & Phân cụm thị trường")    
    UIComponents.centered_title("Capstone Project", "Gợi ý Xe Máy Tương Đồng & Phân Cụm Thị Trường")
    st.write("---")

    # ============================================================
    # INTRO
    # ============================================================
    st.header("1. Giới thiệu")
    st.markdown("""
    Bộ dự án gồm **2 bài toán chính**, được xây dựng trên dữ liệu xe máy cũ đăng bán tại TP.HCM (Chợ Tốt):

    ### 🔹 **Bài toán 1 – Content-based Recommendation**
      - Gợi ý *top N xe tương tự* dựa trên nội dung mô tả.  
      - Hỗ trợ cả:
        - Gợi ý dựa trên **một xe bất kỳ trong tập dữ liệu**
        - Gợi ý dựa trên **chuỗi mô tả người dùng nhập vào**

    ### 🔹 **Bài toán 2 – Phân cụm thị trường xe máy (Market Segmentation)**  
      - Phân nhóm xe theo đặc trưng kỹ thuật, danh mục và mô tả.
      - Giúp doanh nghiệp nhận diện phân khúc thị trường và hành vi người bán.

    """)

    st.write("---")

    # ============================================================
    # PROJECT STRUCTURE
    # ============================================================
    st.header("2. Cấu trúc dự án")
    st.code("""
    ├── data/
    │   ├── data_motobikes.xlsx
    │   ├── data_motobikes_cleaned.csv
    │
    ├── 1_Data_Cleaning_and_Tokenizer.ipynb
    ├── 2_Content-based_Recommender.ipynb
    ├── 3_Build_Models_Clustering_ML_PySpark.ipynb
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
    - Chuẩn hóa Unicode  
    - Loại bỏ ký tự đặc biệt  
    - Tokenize bằng **ViTokenizer**  
    - Loại stopwords tiếng Việt  
    - Tạo trường `content_wt` từ mô tả + tiêu đề + thương hiệu + dòng xe + loại xe

    ### ✔ Xử lý biến categorical
    - One-Hot Encoding  
    - PCA giảm chiều nếu cần

    ### ✔ Xử lý numeric
    - Chuẩn hóa giá trị số    
    - Loại bỏ dòng thiếu thông tin quan trọng


    ### ✔ Loại bỏ cột không cần thiết:
    - Cột: `id`, `href`
    """)

    st.write("---")

    # ============================================================
    # REGRESSION MODEL
    # ============================================================
    st.header("🏷️ 4. Bài Toán 1 – Gợi ý Xe Máy Tương Tự (Content-based Recommendation)")

    st.subheader("4.1 Mục tiêu")
    st.markdown("""
    Xây dựng hệ thống gợi ý xe dựa trên **nội dung mô tả** và **đặc trưng text**, bao gồm:

    - Gợi ý theo xe mẫu (id)
    - Gợi ý theo mô tả người dùng nhập vào
    - So sánh 2 mô hình TF-IDF (SkLearn Cosine Sim vs Gensim)
    """)

    st.subheader("💡 4.2 Phương pháp 1 – TF-IDF + Cosine Similarity")    
    st.markdown("Pipeline:")
    st.code("""
content_wt
→ TfidfVectorizer
→ TF-IDF Matrix
→ Cosine Similarity
→ Recommend Top-N Similar Items
    """, language="python")
    
    st.write("Hàm chính:")
    st.code("recommend_cosine_sim(id, top_n)", language="python")
    

    st.subheader("💡 4.3 Phương pháp 2 – Gensim TF-IDF + Similarity")
    st.markdown("Pipeline:")
    st.code("""
content_wt
→ Tokenize
→ BoW → Dictionary
→ Gensim TF-IDF
→ SparseMatrixSimilarity
→ Recommend Top-N Similar Items
    """, language="python")
    
    st.write("Hàm chính:")
    st.code("recommend_gensim(id, top_n)", language="python")
    
    st.subheader("4.4 Gợi ý từ mô tả người dùng nhập")
    st.markdown("""
    Hỗ trợ tìm kiếm như:
    - “Xe SH Việt Nam giá khoảng 65 triệu”
    - “Môto 150cc ít đi”
    - “Vision chính chủ giá rẻ”
    """)
    st.write("Hàm chính:")
    st.code("recommend_from_query('Xe SH, Việt Nam, Chính chủ, Màu Trắng, giá khoảng 65000000', top_n=5, sim_type)", language="python")
    st.markdown("""
    Với sim_type:
    - 0: dùng phương pháp TF-IDF - Cosine Sim
    - 1: dùng phương pháp Gensim - TF-IDF
    """)

    st.subheader("4.5 Trực quan hóa & Phân tích kết quả")
    st.markdown("""
    Text Analytics
    - WordCloud
    - Unigram / Bigram Frequency
    - Top-TFIDF words
    
    Similarity Analytics
    - Cosine similarity heatmap
    - Similarity histogram
    
    Model Insights
    - Overlap@5
    - Spearman correlation
    - Mean similarity (Cosine vs Gensim)
                """)
    
    st.subheader("4.6 Đánh giá mô hình")
    st.markdown("""
    Các metric sử dụng:     
    | Metric | Mô tả |
    |--------|-------|
    |- Overlap@K                   |Tỉ lệ gợi ý trùng nhau giữa 2 mô hình|
    |- Spearman Correlation        |Tương quan thứ hạng giữa 2 mô hình|
    |- Mean Similarity Comparison  |Trung bình độ tương đồng top-N|
    |- Std of Similarity Scores     |Độ lệch chuẩn độ tương đồng top-N|
    """)
    st.write("Hàm đánh giá:")
    st.code("""
eval_df = evaluate_models(df)
summarize_evaluation(eval_df)
    """, language="python")

    st.markdown("""
    ### 💡 **Mô hình tốt nhất**

    #### **Content-based Recommendation**

    Dựa trên quá trình thử nghiệm và đánh giá 2 hướng tiếp cận TF-IDF, mô hình mang lại hiệu quả tốt nhất:

    #### ⭐ **Best Model: TF-IDF (Sklearn) + Cosine Similarity**
    - Độ sắc nét phân biệt nội dung cao  
    - Tốc độ xử lý nhanh  
    - Phù hợp dữ liệu mô tả ngắn như xe máy trên Chợ Tốt  
    - Kết quả gợi ý sát nghĩa hơn so với Gensim TF-IDF  

    **→ Kết luận:** TF-IDF Sklearn là mô hình khuyến nghị chính cho hệ thống gợi ý.
    """)    

    st.write("---")

    # ============================================================
    # CLUSTERING MODEL
    # ============================================================
    st.header("🏷️ 5. Bài Toán 2 – Phân cụm thị trường xe máy")

    st.subheader("5.1 Mục tiêu")
    st.markdown("""
    - Phân nhóm xe theo đặc trưng kỹ thuật, danh mục, mô tả
    - Xây dựng phân khúc thị trường theo hành vi và đặc điểm
    """)

    st.subheader("5.1 Tiền xử lý đặc trưng cho phân cụm")
    st.markdown("""
    **Numeric Features**
    - giá
    - số km đã đi
    - năm đăng ký → Chuẩn hóa với StandardScaler

    **Categorical Features**
    - thương hiệu
    - dòng xe
    - loại xe → One-hot encoding → PCA giảm chiều (optional)
    
    **Text Features**
    - content_wt → TF-IDF → PCA để đưa vào mô hình clustering
    """
)
    st.write("Tạo ma trận cuối **X_final**")
    st.code("X_final = [Numeric + Category_PCA + Text_PCA]", language="python")

    st.subheader("5.2 Thuật toán phân cụm đã thử")
    st.markdown("""
    **ML truyền thống**
    - ***KMeans***
    - ***Gaussian Mixture Model (GMM)***
    - ***Agglomerative Clustering***
                
    **PySpark**
    - ***KMeans***
    - ***GMM***
    - ***Bisecting KMeans***
    """)

    st.subheader("5.3 Tự động chọn số cụm tối ưu")
    st.markdown("""
    Sử dụng:
    - ***Elbow method***
    - ***Silhouette score***
    Tự động đề xuất K tốt nhất.
    """)

    st.subheader("5.4 Trực quan hóa trong phân cụm & Insight mạnh")
    st.markdown("""
    - PCA scatter plot
    - t-SNE 2D
    - Heatmap đặc trưng theo cluster
    - Boxplot giá / km / năm theo cluster
    - WordCloud từng cluster (insight rất mạnh)
    """)

    st.subheader("5.5 Tự động mô tả cluster theo business format")
    st.write("Ví dụ:")
    st.code("""
    Cluster 0 – Phân khúc cao cấp
    - Giá trung bình: 75 triệu
    - Dòng xe: SH, Vespa
    - Km thấp, xe mới
    - Mô tả phổ biến: xe zin, chính chủ, ít đi
    """, language="python")
    st.write("Hoàn toàn tự động bằng code.")

    st.markdown("""
    ### 💡 **Mô hình tốt nhất**
    #### **Market Segmentation (Clustering)**

    Sau nhiều thử nghiệm (KMeans, GMM, Agglomerative, PySpark KMeans), mô hình mang lại kết quả ổn định nhất:

    #### ⭐ **Best Model: KMeans Clustering**
    - Phân tách nhóm rõ ràng khi dùng PCA 2D  
    - Hiệu quả tốt trên dữ liệu có chiều giảm (numeric + categorical PCA + TF-IDF PCA)  
    - Dễ giải thích (Interpretability tốt)  
    - Tối ưu bằng Silhouette Score và Elbow Method  

    **→ Kết luận:** KMeans là mô hình tối ưu cho bài toán phân cụm thị trường.    
    """)

    st.write("---")

    st.header("🎯 7. Kết Luận")
    st.markdown("""
    ### Bài toán 1 (Gợi ý xe)
    - TF-IDF Sklearn tạo phân biệt mạnh, hiệu quả gợi ý tốt hơn
    - Gensim TF-IDF ổn định & nhẹ hơn
    - Kết hợp mô tả + thương hiệu cho ra recommendation chất lượng
    
    ### Bài toán 2 (Phân cụm)
    Các cluster tạo insight rõ ràng về phân khúc xe:
    - Giá rẻ – Km cao
    - Xe phổ thông – trung cấp
    -Phân khúc cao cấp – ít km
    """)