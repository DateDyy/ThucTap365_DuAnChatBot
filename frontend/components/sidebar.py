import streamlit as st

class Sidebar:
    def __init__(self):
        with st.sidebar:
<<<<<<< Updated upstream
            self.setup_styles()
            st.title("🔮 ThucTap365 AI")
            
            # Logo with better spacing
            st.image("assets/logo.svg", width=180)
            st.markdown("---")
            
            # Info section with cards
            with st.expander("ℹ️ Thông tin Chatbot", expanded=True):
                st.markdown("""
                <div style="background-color: #f8f9fa; padding: 12px; border-radius: 8px;">
                    <p>Chatbot hỗ trợ giải đáp thắc mắc về:</p>
                    <ul>
                        <li>Lập trình web</li>
                        <li>Thuật toán</li>
                        <li>Cấu trúc dữ liệu</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Settings with better organization
            with st.expander("⚙️ Cài đặt"):
                st.slider("🎚️ Độ sáng tạo", 0.0, 1.0, 0.7, 0.1)
                st.checkbox("📝 Lưu lịch sử chat", True)
                
                if st.button("🗑️ Xóa lịch sử", type="secondary"):
                    st.session_state.messages = []
                    st.rerun()
            
            # Footer with better styling
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; color: #6c757d; font-size: 0.8rem;">
                <p>© 2025 ThucTap365</p>
                <p>Phiên bản 2.0.0</p>
            </div>
            """, unsafe_allow_html=True)
    
    def setup_styles(self):
        st.markdown("""
        <style>
            .sidebar .sidebar-content {
                background-color: #f8f9fa;
            }
            .stButton>button {
                border-radius: 8px;
            }
        </style>
        """, unsafe_allow_html=True)
=======
            st.title("ThucTap365 ChatBot")
            
            # Logo
            st.image("assets/logo.svg", width=200)
            
            st.markdown("---")
            
            # Thông tin về chatbot
            st.markdown("### Thông tin")
            st.markdown("""
            Chatbot này được phát triển để hỗ trợ trả lời các câu hỏi về lập trình web.
            
            Dữ liệu được xây dựng từ các tài liệu giáo trình và sách về lập trình web.
            """)
            
            st.markdown("---")
            
            # Các tùy chọn
            st.markdown("### Tùy chọn")
            
            # Nút xóa lịch sử chat
            if st.button("Xóa lịch sử chat"):
                st.session_state.messages = []
                st.rerun()
            
            # Các tùy chọn khác
            st.markdown("### Cài đặt")
            temperature = st.slider("Độ sáng tạo", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
            
            st.markdown("---")
            
            # Thông tin phiên bản
            st.markdown("### Phiên bản")
            st.markdown("v1.0.0")
            
            # Footer
            st.markdown("---")
            st.markdown("© 2025 ThucTap365")
>>>>>>> Stashed changes
