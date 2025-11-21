import streamlit as st
import pandas as pd
import numpy as np # Dùng để tạo data giả lập

from ui.ui_components import UIComponents

# Khởi tạo class
ui = UIComponents()

# Cấu hình page (Phải luôn nằm đầu tiên)
st.set_page_config(
    page_title="UI Components Demo",
    page_icon="🎨",
    layout="wide"
)

def show():
    """
    Hàm chính hiển thị demo các UI Components.
    """
    
    # ============================================================
    # 2. ĐIỀU HƯỚNG (NAVIGATION LOGIC)
    # ============================================================

    # Tạo Menu ở Sidebar
    with st.sidebar:
        st.title("Điều hướng")
        selected_page = st.radio(
            "Chọn trang:", 
            ["Trang Chủ", "UI Components Demo"]
        )

    # ============================================================
    # 3. ROUTING (GỌI HÀM TƯƠNG ỨNG)
    # ============================================================

    if selected_page == "Trang Chủ":
        home_page()
    elif selected_page == "UI Components Demo":
        show_ui_demo()
    
    # show_ui_demo()

# ============================================================
# 1. ĐỊNH NGHĨA CÁC TRANG (PAGES)
# ============================================================

def home_page():
    """Hàm hiển thị trang chủ giả lập"""
    ui.app_header(
        title="Trang Chủ",
        subtitle="Chào mừng đến với ứng dụng Streamlit",
        icon="🏠"
    )
    st.write("Hãy chọn **'UI Components Demo'** ở menu bên trái để xem thư viện UI.")
    
    # Demo thẻ card đơn giản
    ui.card(
        title="Bắt đầu", 
        content="Chọn menu bên trái để khám phá các component.", 
        color="#007bff", 
        icon="point_left"
    )

def show_ui_demo():
    """
    Hàm chính chứa toàn bộ logic demo UI cũ của bạn.
    Toàn bộ code hiển thị Tabs, Header, Footer được đưa vào đây.
    """
    
    # --- DEMO HEADER ---
    ui.app_header(
        title="UI Components Demo",
        subtitle="Thư viện các component UI cho Streamlit",
        icon="🎨"
    )

    # --- TABS ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Headers & Text",
        "🎯 Cards & Alerts", 
        "📊 Tables & Lists",
        "🏷️ Badges & Buttons",
        "📈 Progress & Steps"
    ])

    # --- TAB 1: HEADERS & TEXT ---
    with tab1:
        ui.section_header("Section Headers", "Các loại header cho từng section")
        
        st.subheader("1. Section Header")
        ui.section_header("Tiêu đề Section", "Mô tả ngắn về section này")
        
        st.code('ui.section_header("Tiêu đề Section", "Mô tả ngắn", color="#2b8acc")', language="python")
        
        ui.divider()
        
        st.subheader("2. Centered Title")
        ui.centered_title("Tiêu đề Căn Giữa", "Phụ đề bên dưới")
        
        st.code('ui.centered_title("Tiêu đề Căn Giữa", "Phụ đề bên dưới")', language="python")
        
        ui.divider()
        
        st.subheader("3. Highlight Text")
        ui.highlight_text("⚠️ Text này được highlight để thu hút sự chú ý!")
        
        st.code('ui.highlight_text("Text được highlight", bg_color="#fff3cd", text_color="#856404")', language="python")
        
        ui.divider()
        
        st.subheader("4. Colored Text")
        ui.colored_text("Text màu xanh", color="#007bff", size="20px", bold=True)
        ui.colored_text("Text màu đỏ in nghiêng", color="#dc3545", size="18px", italic=True)
        
        st.code('ui.colored_text("Text tùy chỉnh", color="#007bff", size="20px", bold=True, italic=False)', language="python")
        
        ui.divider()
        
        st.subheader("5. Gradient Text")
        ui.gradient_text("🌈 Text với Gradient")
        
        st.code('ui.gradient_text("Text Gradient", gradient="linear-gradient(90deg, #667eea 0%, #764ba2 100%)")', language="python")

        st.subheader("6. Centered Text Normal")
        ui.centered_text("Tiêu đề Căn Giữa", color="#1f77b4", size="30px")
        
        st.code('ui.centered_text("Tiêu đề Căn Giữa", color="#1f77b4", size="30px")', language="python")

    # --- TAB 2: CARDS & ALERTS ---
    with tab2:
        ui.section_header("Cards & Alerts", "Các loại thẻ và thông báo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("1. Alert Boxes")
            ui.alert_box("Thông tin quan trọng", alert_type="info", title="Info")
            ui.alert_box("Thành công!", alert_type="success", title="Success")
            ui.alert_box("Cảnh báo!", alert_type="warning", title="Warning")
            ui.alert_box("Lỗi xảy ra!", alert_type="error", title="Error")
            
            st.code('ui.alert_box("Message", alert_type="info", title="Title")', language="python")
        
        with col2:
            st.subheader("2. Info Box")
            ui.info_box(
                title="Lưu ý quan trọng",
                content="Đây là một box thông tin với icon và styling đẹp mắt.",
                icon="💡"
            )
            st.code('ui.info_box(title="Tiêu đề", content="Nội dung", icon="💡")', language="python")
        
        ui.divider()
        
        st.subheader("3. Cards")
        col1, col2, col3 = st.columns(3)
        with col1:
            ui.card(title="Card 1", content="Nội dung của card số 1", color="#007bff", icon="📊")
        with col2:
            ui.card(title="Card 2", content="Nội dung của card số 2", color="#28a745", icon="✅")
        with col3:
            ui.card(title="Card 3", content="Nội dung của card số 3", color="#dc3545", icon="🎯")
        
        st.code('ui.card(title="Card Title", content="Content", color="#007bff", icon="📊")', language="python")
        
        ui.divider()
        
        st.subheader("4. Metric Cards")
        col1, col2, col3, col4 = st.columns(4)
        with col1: ui.metric_card("Users", "1,234", "+12%", color="#007bff", icon="👥")
        with col2: ui.metric_card("Revenue", "$45.2K", "+8%", color="#28a745", icon="💰")
        with col3: ui.metric_card("Orders", "567", "+15%", color="#ffc107", icon="📦")
        with col4: ui.metric_card("Rating", "4.8/5", "+0.2", color="#dc3545", icon="⭐")
        
        st.code('ui.metric_card(label="Users", value="1,234", delta="+12%", color="#007bff", icon="👥")', language="python")

    # ============================================================
    # TAB 3: TABLES & LISTS
    # ============================================================
    with tab3:
        ui.section_header("Tables & Lists", "Bảng dữ liệu phân trang")

        st.subheader("1. Paginated Dataframe (30 rows)")

        # --- 1. TẠO DỮ LIỆU GIẢ LẬP (30 DÒNG) ---
        if 'df_data' not in st.session_state:
            # Tạo dataframe mẫu 30 dòng, 4 cột
            data = {
                'ID': range(1, 31),
                'Sản phẩm': [f'Sản phẩm {i}' for i in range(1, 31)],
                'Doanh số': np.random.randint(100, 1000, 30),
                'Trạng thái': np.random.choice(['Active', 'Inactive', 'Pending'], 30)
            }
            st.session_state.df_data = pd.DataFrame(data)

        df = st.session_state.df_data

        # --- 2. CẤU HÌNH PHÂN TRANG ---
        rows_per_page = 10
        total_rows = len(df)
        # Tính tổng số trang: (30-1)//10 + 1 = 3 trang
        total_pages = (total_rows - 1) // rows_per_page + 1

        # Khởi tạo trang hiện tại trong Session State nếu chưa có
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1

        # --- 3. XỬ LÝ LOGIC HIỂN THỊ NÚT ---
        # Tạo layout các cột cho nút bấm: [First] [1] [2] [3] [Last]
        # Số lượng cột = 2 (First/Last) + Số trang
        cols = st.columns(total_pages + 2)

        # Nút First (Về trang 1)
        if cols[0].button("⏮️ First", key="btn_first", disabled=(st.session_state.current_page == 1)):
            st.session_state.current_page = 1
            st.rerun()

        # Các nút số trang (1, 2, 3...)
        for i in range(total_pages):
            page_num = i + 1
            # Nếu là trang hiện tại thì dùng nút màu đậm (primary), còn lại màu nhạt (secondary)
            btn_type = "primary" if st.session_state.current_page == page_num else "secondary"
            
            if cols[i + 1].button(f"{page_num}", key=f"btn_page_{page_num}", type=btn_type):
                st.session_state.current_page = page_num
                st.rerun()

        # Nút Last (Về trang cuối)
        if cols[total_pages + 1].button("Last ⏭️", key="btn_last", disabled=(st.session_state.current_page == total_pages)):
            st.session_state.current_page = total_pages
            st.rerun()

        # --- 4. HIỂN THỊ BẢNG DỮ LIỆU ---
        # Tính toán chỉ số bắt đầu và kết thúc (Slicing)
        start_idx = (st.session_state.current_page - 1) * rows_per_page
        end_idx = start_idx + rows_per_page

        # Cắt dataframe
        sub_df = df.iloc[start_idx:end_idx]

        # Hiển thị thông tin trang
        st.markdown(f"**Đang hiển thị trang {st.session_state.current_page}/{total_pages}** (Dòng {start_idx + 1} đến {min(end_idx, total_rows)})")
        
        # Vẽ bảng
        st.dataframe(
            sub_df, 
            use_container_width=True,
            hide_index=True  # Ẩn cột index số 0, 1, 2... nếu muốn
        )

        ui.divider()
        
        # (Phần code cũ Styled Table & Definition List giữ lại ở dưới nếu cần...)
        st.subheader("2. Styled Table (Demo cũ)")
        ui.styled_table(
            headers=["Metric", "Value", "Description"],
            rows=[
                ["RMSE", "4.2%", "Root Mean Squared Error"],
                ["MAE", "2.8%", "Mean Absolute Error"]
            ],
            centered=True
        )

    # --- TAB 4: BADGES & BUTTONS ---
    with tab4:
        ui.section_header("Badges & Buttons", "Badge, tag và nút bấm")
        
        st.subheader("1. Single Badge")
        ui.badge("New", color="#28a745")
        ui.badge("Hot", color="#dc3545")
        ui.badge("Popular", color="#007bff")
        st.code('ui.badge("New", color="#28a745")', language="python")
        
        ui.divider()
        
        st.subheader("2. Multiple Tags")
        ui.tags(["Python", "Machine Learning", "Streamlit", "Data Science"], color="#6c757d")
        st.code('ui.tags(["Tag1", "Tag2"], color="#6c757d")', language="python")
        
        ui.divider()
        
        st.subheader("3. Custom Buttons")
        col1, col2, col3 = st.columns(3)
        with col1: ui.custom_button("Primary Button", "#", color="#007bff", centered=True)
        with col2: ui.custom_button("Success Button", "#", color="#28a745", centered=True)
        with col3: ui.custom_button("Danger Button", "#", color="#dc3545", centered=True)
        st.code('ui.custom_button("Text", "#", color="#007bff")', language="python")

    # --- TAB 5: PROGRESS & STEPS ---
    with tab5:
        ui.section_header("Progress & Steps", "Thanh tiến độ và các bước")
        
        st.subheader("1. Progress Bars")
        ui.progress_bar(75, 100, color="#007bff", label="Project Completion")
        ui.progress_bar(45, 100, color="#28a745", label="Tasks Done")
        ui.progress_bar(90, 100, color="#ffc107", label="Budget Used")
        st.code('ui.progress_bar(75, 100, color="#007bff")', language="python")
        
        ui.divider()
        
        st.subheader("2. Step Indicator")
        ui.step_indicator(steps=["Start", "Processing", "Review", "Complete"], current_step=2)
        st.code('ui.step_indicator(steps=["A", "B"], current_step=0)', language="python")
        
        ui.divider()
        
        st.subheader("3. Different Dividers")
        st.write("Solid Divider:")
        ui.divider(style="solid", color="#007bff")
        st.write("Dashed Divider:")
        ui.divider(style="dashed", color="#28a745")
        st.write("Dotted Divider:")
        ui.divider(style="dotted", color="#dc3545")
        st.write("Gradient Divider:")
        ui.gradient_divider()

    # --- FOOTER ---
    ui.footer(
        text="© 2025 Capstone Project. All rights reserved.",
        links={
            "GitHub": "https://github.com",
            "Documentation": "https://docs.streamlit.io",
            "Contact": "#"
        }
    )
    
    # --- QUICK REFERENCE (Chỉ hiện ở Sidebar khi đang ở trang này) ---
    with st.sidebar:
        st.markdown("---") # Kẻ ngang phân cách với menu
        st.markdown("### 📚 Quick Reference")
        st.code('''
# Headers
ui.app_header("T", "S")

# Alerts
ui.alert_box("Msg", "info")

# Cards
ui.card("T", "C")
        ''', language="python")

"""
# ============================================================
# 2. ĐIỀU HƯỚNG (NAVIGATION LOGIC)
# ============================================================

# Tạo Menu ở Sidebar
with st.sidebar:
    st.title("Điều hướng")
    selected_page = st.radio(
        "Chọn trang:", 
        ["Trang Chủ", "UI Components Demo"]
    )

# ============================================================
# 3. ROUTING (GỌI HÀM TƯƠNG ỨNG)
# ============================================================

if selected_page == "Trang Chủ":
    home_page()
elif selected_page == "UI Components Demo":
    show_ui_demo()
"""