import streamlit as st
import json
import os
from datetime import datetime

# Cấu hình trang
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cấu hình CSS tùy chỉnh
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #e9ecef;
    }
    
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        text-align: right;
    }
    
    .ai-message {
        background-color: #e9ecef;
        color: #333;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        text-align: left;
    }
    
    .sidebar-header {
        font-size: 1.5rem;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    
    .profile-section {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .settings-section {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .file-upload {
        border: 2px dashed #007bff;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }
    
    .voice-button {
        background-color: #28a745;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        margin: 5px;
    }
    
    .voice-button:hover {
        background-color: #218838;
    }
    </style>
    """, unsafe_allow_html=True)

# Cấu hình màu sắc cho chat
CHAT_COLORS = {
    "Blue": "#007bff",
    "Green": "#28a745", 
    "Purple": "#6f42c1",
    "Orange": "#fd7e14",
    "Red": "#dc3545"
}

# Đường dẫn đến file cấu hình
CONFIG_FILE = "user_config.json"

# Hàm load cấu hình
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return {"chat_color": "Blue", "font_size": "Medium"}
    else:
        return {"chat_color": "Blue", "font_size": "Medium"}

# Hàm lưu cấu hình
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)