import streamlit as st
from typing import List, Dict

class UIComponents:
    """Class chứa các component UI thông dụng cho Streamlit"""
    
    # ============================================================
    # HEADERS & TITLES
    # ============================================================
    
    @staticmethod
    def app_header(title: str, subtitle: str = "", icon: str = ""):
        """
        Header chính của app
        
        Args:
            title: Tiêu đề chính
            subtitle: Phụ đề
            icon: Icon emoji (optional)
        """
        st.markdown(
            f"""
            <div style="
                padding: 20px;
                border-radius: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                margin-bottom: 20px;
            ">
                <h1 style="margin: 0; font-size: 2.5em;">
                    {icon} {title}
                </h1>
                {f'<p style="font-size: 1.2em; margin-top: 10px; opacity: 0.9;">{subtitle}</p>' if subtitle else ''}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def section_header(title: str, subtitle: str = "", color: str = "#2b8acc"):
        """
        Header cho section/phần
        
        Args:
            title: Tiêu đề section
            subtitle: Mô tả ngắn
            color: Màu chủ đạo
        """
        st.markdown(
            f"""
            <div style="
                padding: 15px;
                border-left: 5px solid {color};
                background: #f8f9fa;
                border-radius: 8px;
                margin: 20px 0;
            ">
                <h2 style="color: {color}; margin: 0;">{title}</h2>
                {f'<p style="color: #555; margin-top: 5px; margin-bottom: 0;">{subtitle}</p>' if subtitle else ''}
            </div>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def section_title(title: str, subtitle: str = "", content: str = "", color: str = "#2b8acc"):
        """
        Header cho section/phần
        
        Args:
            title: Tiêu đề section
            subtitle: Mô tả ngắn
            color: Màu chủ đạo
        """
        st.markdown(
            f"""
            <div style="
                padding: 10px;
                border-left: 5px solid {color};
                background: #f8f9fa;
                border-radius: 6px;
                margin: 2px 0;
            ">
                <h3 style="color: {color}; margin: 0;">{title}</h3>
                {f'<h5 style="color: #555; margin-top: 5px; margin-bottom: 0;">{subtitle}</h5>' if subtitle else ''}
                {f'<p style="color: #555; margin-top: 5px; margin-bottom: 0;">{content}</p>' if content else ''}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def centered_title(title: str, subtitle: str = ""):
        """
        Tiêu đề căn giữa
        
        Args:
            title: Tiêu đề
            subtitle: Phụ đề
        """
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px;">
                <h1 style="color: #1f77b4; margin-bottom: 10px;">{title}</h1>
                {f'<h3 style="color: #666; font-weight: normal;">{subtitle}</h3>' if subtitle else ''}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def centered_title_normal(title: str, subtitle: str = ""):
        """
        Tiêu đề căn giữa
        
        Args:
            title: Tiêu đề
            subtitle: Phụ đề
        """
        st.markdown(
            f"""
            <div style="text-align: center; padding: 10px;">
                <h2 style="color: #1f77b4; margin-bottom: 6px;">{title}</h2>
                {f'<h4 style="color: #666; font-weight: normal;">{subtitle}</h4>' if subtitle else ''}
            </div>
            """,
            unsafe_allow_html=True
        )
   
    @staticmethod
    def centered_text(title: str, color: str = "#1f77b4", size: str = "16px"):
        """
        Tiêu đề căn giữa
        
        Args:
            title: Tiêu đề            
        """
        st.markdown(
            f"""
            <div style="text-align: center; padding: 3px;">
                <h1 style="color: {color}; font-size: {size}; margin-bottom: 0px;">{title}</h1>                
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # ============================================================
    # TEXT FORMATTING
    # ============================================================
    
    @staticmethod
    def highlight_text(text: str, bg_color: str = "#fff3cd", text_color: str = "#856404"):
        """
        Text được highlight
        
        Args:
            text: Nội dung text
            bg_color: Màu nền
            text_color: Màu chữ
        """
        st.markdown(
            f"""
            <div style="
                background-color: {bg_color};
                color: {text_color};
                padding: 15px;
                border-radius: 8px;
                border-left: 5px solid {text_color};
                margin: 10px 0;
            ">
                {text}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def colored_text(text: str, color: str = "#1f77b4", size: str = "16px", 
                     bold: bool = False, italic: bool = False):
        """
        Text với màu sắc tùy chỉnh
        
        Args:
            text: Nội dung
            color: Màu chữ
            size: Kích thước font
            bold: In đậm
            italic: In nghiêng
        """
        weight = "bold" if bold else "normal"
        style = "italic" if italic else "normal"
        
        st.markdown(
            f'<span style="color: {color}; font-size: {size}; font-weight: {weight}; font-style: {style};">{text}</span>',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def gradient_text(text: str, gradient: str = "linear-gradient(90deg, #667eea 0%, #764ba2 100%)"):
        """
        Text với gradient color
        
        Args:
            text: Nội dung
            gradient: CSS gradient
        """
        st.markdown(
            f"""
            <h2 style="
                background: {gradient};
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: bold;
            ">{text}</h2>
            """,
            unsafe_allow_html=True
        )
    
    # ============================================================
    # ALERTS & NOTIFICATIONS
    # ============================================================
    
    @staticmethod
    def alert_box(message: str, alert_type: str = "info", title: str = ""):
        """
        Alert box với các loại khác nhau
        
        Args:
            message: Nội dung thông báo
            alert_type: Loại alert (info, success, warning, error)
            title: Tiêu đề (optional)
        """
        colors = {
            "info": {"bg": "#d1ecf1", "border": "#0c5460", "text": "#0c5460", "icon": "ℹ️"},
            "success": {"bg": "#d4edda", "border": "#155724", "text": "#155724", "icon": "✅"},
            "warning": {"bg": "#fff3cd", "border": "#856404", "text": "#856404", "icon": "⚠️"},
            "error": {"bg": "#f8d7da", "border": "#721c24", "text": "#721c24", "icon": "❌"}
        }
        
        color = colors.get(alert_type, colors["info"])
        
        st.markdown(
            f"""
            <div style="
                background-color: {color['bg']};
                color: {color['text']};
                padding: 15px 20px;
                border-radius: 8px;
                border-left: 5px solid {color['border']};
                margin: 15px 0;
            ">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 24px;">{color['icon']}</span>
                    <div>
                        {f'<strong style="font-size: 18px;">{title}</strong><br>' if title else ''}
                        {message}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def info_box(title: str, content: str, icon: str = "💡"):
        """
        Box thông tin với icon
        
        Args:
            title: Tiêu đề
            content: Nội dung
            icon: Icon emoji
        """
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 20px;
                border-radius: 12px;
                margin: 15px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <h3 style="margin-top: 0; color: #2c3e50;">
                    {icon} {title}
                </h3>
                <p style="color: #34495e; margin-bottom: 0; line-height: 1.6;">
                    {content}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # ============================================================
    # CARDS & CONTAINERS
    # ============================================================
    
    @staticmethod
    def card(title: str, content: str, color: str = "#1f77b4", icon: str = ""):
        """
        Card component với header màu
        
        Args:
            title: Tiêu đề card
            content: Nội dung
            color: Màu header
            icon: Icon (optional)
        """
        st.markdown(
            f"""
            <div style="
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin: 15px 0;
            ">
                <div style="
                    background-color: {color};
                    color: white;
                    padding: 15px 20px;
                    font-size: 20px;
                    font-weight: bold;
                ">
                    {icon} {title}
                </div>
                <div style="
                    background-color: white;
                    padding: 20px;
                    color: #333;
                    line-height: 1.6;
                ">
                    {content}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def metric_card(label: str, value: str, delta: str = "", 
                   color: str = "#1f77b4", icon: str = ""):
        """
        Card hiển thị metric
        
        Args:
            label: Nhãn
            value: Giá trị
            delta: Thay đổi
            color: Màu chủ đạo
            icon: Icon
        """
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {color}15 0%, {color}30 100%);
                padding: 20px;
                border-radius: 12px;
                border: 2px solid {color};
                text-align: center;
                margin: 10px 0;
            ">
                <div style="color: #666; font-size: 14px; margin-bottom: 5px;">
                    {icon} {label}
                </div>
                <div style="
                    color: {color};
                    font-size: 36px;
                    font-weight: bold;
                    margin: 10px 0;
                ">
                    {value}
                </div>
                {f'<div style="color: #28a745; font-size: 16px;">{delta}</div>' if delta else ''}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # ============================================================
    # TABLES
    # ============================================================
    
    @staticmethod
    def styled_table(headers: List[str], rows: List[List[str]], 
                    centered: bool = False):
        """
        Bảng với styling
        
        Args:
            headers: Danh sách header
            rows: Danh sách rows (list of lists)
            centered: Căn giữa nội dung
        """
        align = "center" if centered else "left"
        
        header_html = "".join([f"<th>{h}</th>" for h in headers])
        rows_html = ""
        for row in rows:
            row_html = "".join([f"<td>{cell}</td>" for cell in row])
            rows_html += f"<tr>{row_html}</tr>"
        
        st.markdown(
            f"""
            <style>
            .custom-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
            }}
            .custom-table th {{
                background-color: #2b8acc;
                color: white;
                padding: 15px;
                text-align: {align};
                font-weight: bold;
            }}
            .custom-table td {{
                padding: 12px 15px;
                text-align: {align};
                border-bottom: 1px solid #ddd;
            }}
            .custom-table tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}
            .custom-table tr:hover {{
                background-color: #e9ecef;
            }}
            </style>
            
            <table class="custom-table">
                <thead>
                    <tr>{header_html}</tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def styled_table_small(headers: List[str], rows: List[List[str]], 
                    centered: bool = False):
        """
        Bảng với styling
        
        Args:
            headers: Danh sách header
            rows: Danh sách rows (list of lists)
            centered: Căn giữa nội dung
        """
        align = "center" if centered else "left"
        
        header_html = "".join([f"<th>{h}</th>" for h in headers])
        rows_html = ""
        for row in rows:
            row_html = "".join([f"<td>{cell}</td>" for cell in row])
            rows_html += f"<tr>{row_html}</tr>"
        
        st.markdown(
            f"""
            <style>
            .custom-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
            }}
            .custom-table th {{
                background-color: #2b8acc;
                color: white;
                padding: 6px;
                text-align: {align};
                font-weight: bold;
            }}
            .custom-table td {{
                padding: 7px 15px;
                text-align: {align};
                border-bottom: 1px solid #ddd;
            }}
            .custom-table tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}
            .custom-table tr:hover {{
                background-color: #e9ecef;
            }}
            </style>
            
            <table class="custom-table">
                <thead>
                    <tr>{header_html}</tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def definition_list(items: Dict[str, str]):
        """
        Danh sách định nghĩa (key: value)
        
        Args:
            items: Dictionary với key-value pairs
        """
        rows_html = ""
        for key, value in items.items():
            rows_html += f"""
                <tr>
                    <td style="font-weight: bold; color: #2b8acc; width: 30%;">{key}</td>
                    <td style="color: #555;">{value}</td>
                </tr>
            """
        
        st.markdown(
            f"""
            <table style="
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            ">
                {rows_html}
            </table>
            """,
            unsafe_allow_html=True
        )
    
    # ============================================================
    # BADGES & TAGS
    # ============================================================
    
    @staticmethod
    def badge(text: str, color: str = "#007bff", bg_color: str = None):
        """
        Badge/tag nhỏ
        
        Args:
            text: Nội dung badge
            color: Màu chữ
            bg_color: Màu nền (nếu None sẽ dùng màu mờ của color)
        """
        if bg_color is None:
            bg_color = f"{color}20"
        
        st.markdown(
            f"""
            <span style="
                background-color: {bg_color};
                color: {color};
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 500;
                display: inline-block;
                margin: 3px;
            ">{text}</span>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def tags(tags_list: List[str], color: str = "#6c757d"):
        """
        Hiển thị nhiều tags
        
        Args:
            tags_list: Danh sách các tag
            color: Màu chủ đạo
        """
        tags_html = ""
        for tag in tags_list:
            tags_html += f"""
                <span style="
                    background-color: {color}20;
                    color: {color};
                    padding: 6px 14px;
                    border-radius: 20px;
                    font-size: 14px;
                    display: inline-block;
                    margin: 5px;
                    border: 1px solid {color};
                ">{tag}</span>
            """
        
        st.markdown(
            f'<div style="margin: 15px 0;">{tags_html}</div>',
            unsafe_allow_html=True
        )
    
    # ============================================================
    # BUTTONS & LINKS
    # ============================================================
    
    @staticmethod
    def custom_button(text: str, url: str, color: str = "#007bff", 
                     centered: bool = False):
        """
        Button/link tùy chỉnh
        
        Args:
            text: Text trên button
            url: Link URL
            color: Màu button
            centered: Căn giữa
        """
        align = "center" if centered else "left"
        
        st.markdown(
            f"""
            <div style="text-align: {align}; margin: 20px 0;">
                <a href="{url}" target="_blank" style="
                    background-color: {color};
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 8px;
                    display: inline-block;
                    font-weight: bold;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    transition: all 0.3s ease;
                ">
                    {text}
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # ============================================================
    # DIVIDERS
    # ============================================================
    
    @staticmethod
    def divider(style: str = "solid", color: str = "#ddd", margin: str = "20px"):
        """
        Đường phân cách tùy chỉnh
        
        Args:
            style: solid, dashed, dotted
            color: Màu đường kẻ
            margin: Khoảng cách trên/dưới
        """
        st.markdown(
            f"""
            <hr style="
                border: none;
                border-top: 2px {style} {color};
                margin: {margin} 0;
            ">
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def gradient_divider():
        """Đường phân cách gradient"""
        st.markdown(
            """
            <div style="
                height: 3px;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                margin: 20px 0;
                border-radius: 2px;
            "></div>
            """,
            unsafe_allow_html=True
        )
    
    # ============================================================
    # PROGRESS & STEPS
    # ============================================================
    
    @staticmethod
    def progress_bar(value: int, max_value: int = 100, 
                    color: str = "#28a745", label: str = ""):
        """
        Progress bar tùy chỉnh
        
        Args:
            value: Giá trị hiện tại
            max_value: Giá trị tối đa
            color: Màu thanh progress
            label: Nhãn hiển thị
        """
        percentage = (value / max_value) * 100
        
        st.markdown(
            f"""
            <div style="margin: 15px 0;">
                {f'<div style="color: #666; margin-bottom: 5px;">{label}</div>' if label else ''}
                <div style="
                    background-color: #e9ecef;
                    border-radius: 10px;
                    overflow: hidden;
                    height: 25px;
                ">
                    <div style="
                        background-color: {color};
                        width: {percentage}%;
                        height: 100%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-weight: bold;
                        font-size: 12px;
                        transition: width 0.3s ease;
                    ">
                        {value}/{max_value}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def step_indicator(steps: List[str], current_step: int):
        """
        Hiển thị các bước
        
        Args:
            steps: Danh sách tên các bước
            current_step: Bước hiện tại (bắt đầu từ 0)
        """
        steps_html = ""
        for i, step in enumerate(steps):
            is_active = i == current_step
            is_completed = i < current_step
            
            if is_completed:
                color = "#28a745"
                icon = "✓"
            elif is_active:
                color = "#007bff"
                icon = str(i + 1)
            else:
                color = "#ccc"
                icon = str(i + 1)
            
            steps_html += f"""
                <div style="flex: 1; text-align: center;">
                    <div style="
                        width: 40px;
                        height: 40px;
                        background-color: {color};
                        color: white;
                        border-radius: 50%;
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: bold;
                        margin-bottom: 10px;
                    ">
                        {icon}
                    </div>
                    <div style="
                        color: {color};
                        font-size: 14px;
                        font-weight: {'bold' if is_active else 'normal'};
                    ">
                        {step}
                    </div>
                </div>
            """
            
            if i < len(steps) - 1:
                connector_color = "#28a745" if is_completed else "#ccc"
                steps_html += f"""
                    <div style="
                        flex: 0.5;
                        height: 2px;
                        background-color: {connector_color};
                        align-self: center;
                        margin-bottom: 35px;
                    "></div>
                """
        
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: start;
                margin: 30px 0;
            ">
                {steps_html}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # ============================================================
    # CODE DISPLAY
    # ============================================================
    
    @staticmethod
    def code_block(code: str, language: str = "python", title: str = ""):
        """
        Code block với tiêu đề
        
        Args:
            code: Nội dung code
            language: Ngôn ngữ lập trình
            title: Tiêu đề code block
        """
        if title:
            st.markdown(
                f"""
                <div style="
                    background-color: #2d2d2d;
                    color: white;
                    padding: 10px 15px;
                    border-radius: 8px 8px 0 0;
                    font-weight: bold;
                ">
                    📄 {title}
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.code(code, language=language)
    
    # ============================================================
    # FOOTER
    # ============================================================
    
    @staticmethod
    def footer(text: str, links: Dict[str, str] = None):
        """
        Footer cho app
        
        Args:
            text: Text footer
            links: Dictionary với {text: url}
        """
        links_html = ""
        if links:
            for text, url in links.items():
                links_html += f'<a href="{url}" style="color: white; margin: 0 10px;">{text}</a>'
        
        st.markdown(
            f"""
            <div style="
                background-color: #2c3e50;
                color: white;
                padding: 30px;
                text-align: center;
                margin-top: 50px;
                border-radius: 10px;
            ">
                <p style="margin: 0; font-size: 16px;">{text}</p>
                {f'<div style="margin-top: 15px;">{links_html}</div>' if links_html else ''}
            </div>
            """,
            unsafe_allow_html=True
        )

    # ============================================================
    # PAGE LAYOUT
    # ============================================================
    @staticmethod
    def show_logo_conditional(page_name: str, width: int = 960, centered: bool = True):
        """
        Hiển thị logo có điều kiện
        
        Args:
            page_name: Tên trang hiện tại ('home', 'gioithieu', etc.)
            width: Chiều rộng logo
            centered: Căn giữa
        """
        import os
        from pathlib import Path
        
        # Danh sách trang được hiển thị logo
        pages_with_logo = ['home', 'gioithieu', 'capstone_project1', 'capstone_project2']
        
        # Kiểm tra trang có trong danh sách không
        if page_name.lower() not in pages_with_logo:
            return
        
        # Kiểm tra file logo có tồn tại không
        if not os.path.exists("./assets/logo.jpg"):
            st.warning("⚠️ Logo không tìm thấy!")
            return
        
        # Hiển thị logo
        if centered:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("./assets/logo.jpg", width=width)            
        else:
            st.image("./assets/logo.jpg", width=width)
    
    # Page style: set fixed width and centered
    @staticmethod
    def set_page_width_centered(width: int = 960):
        """
        Set width cố định và căn giữa cho toàn bộ page
        
        Args:
            width: Chiều rộng mong muốn (pixels)
        """
        st.markdown(
            f"""
            <style>
            /* Main content container */
            .main .block-container {{
                max-width: {width}px;
                padding-left: 2rem;
                padding-right: 2rem;
                margin: 0 auto;
            }}
            
            /* Full width container khi cần */
            .full-width {{
                max-width: 100% !important;
            }}
            
            /* Đảm bảo sidebar không ảnh hưởng */
            section[data-testid="stSidebar"] {{
                width: 300px !important;
            }}
            
            /* Header căn giữa */
            header {{
                background-color: transparent !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def set_page_layout(width: int = 960, hide_branding: bool = True):
        """
        Set page layout với width cố định và căn giữa
        
        Args:
            width: Chiều rộng mong muốn (pixels)
            hide_branding: Ẩn Streamlit branding
        """
        branding_css = """
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        """ if hide_branding else ""
                
        st.markdown(
            """
            <style>
            /* Tìm class chứa nội dung chính của Streamlit (thường là block-container) */
            .block-container {
                max-width: 960px; /* Cố định chiều rộng tối đa */
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 2rem;
                padding-bottom: 2rem;
                margin: 0 auto; /* Căn giữa khối div */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def set_page_layout_wide(width: int = 1200, hide_branding: bool = True):
        """
        Set page layout với width cố định và căn giữa
        
        Args:
            width: Chiều rộng mong muốn (pixels)
            hide_branding: Ẩn Streamlit branding
        """
        branding_css = """
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        """ if hide_branding else ""
                
        st.markdown(
            """
            <style>
            /* Tìm class chứa nội dung chính của Streamlit (thường là block-container) */
            .block-container {
                max-width: 1200px; /* Cố định chiều rộng tối đa */
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 2rem;
                padding-bottom: 2rem;
                margin: 0 auto; /* Căn giữa khối div */
            }
            </style>
            """,
            unsafe_allow_html=True
        )