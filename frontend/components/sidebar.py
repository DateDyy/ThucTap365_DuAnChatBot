import streamlit as st

class Sidebar:
    def __init__(self):
        with st.sidebar:
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