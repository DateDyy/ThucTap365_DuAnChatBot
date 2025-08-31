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
    
    <!-- Persistent Login JavaScript -->
    <script>
    // Persistent Login JavaScript
    // Hỗ trợ lưu trữ token đăng nhập vào localStorage
    
    (function() {
        'use strict';
        
        // Kiểm tra xem có localStorage không
        function isLocalStorageAvailable() {
            try {
                const test = '__localStorage_test__';
                localStorage.setItem(test, test);
                localStorage.removeItem(test);
                return true;
            } catch (e) {
                return false;
            }
        }
        
        // Lưu token vào localStorage
        function saveTokenToLocalStorage(token) {
            if (isLocalStorageAvailable() && token) {
                try {
                    localStorage.setItem('chatbot_login_token', token);
                    localStorage.setItem('chatbot_login_time', Date.now().toString());
                    return true;
                } catch (e) {
                    console.error('Không thể lưu token vào localStorage:', e);
                    return false;
                }
            }
            return false;
        }
        
        // Đọc token từ localStorage
        function getTokenFromLocalStorage() {
            if (isLocalStorageAvailable()) {
                try {
                    const token = localStorage.getItem('chatbot_login_token');
                    const loginTime = localStorage.getItem('chatbot_login_time');
                    
                    if (token && loginTime) {
                        // Kiểm tra token có quá cũ không (30 ngày)
                        const now = Date.now();
                        const loginTimestamp = parseInt(loginTime);
                        const thirtyDays = 30 * 24 * 60 * 60 * 1000; // 30 ngày tính bằng milliseconds
                        
                        if (now - loginTimestamp < thirtyDays) {
                            return token;
                        } else {
                            // Token quá cũ, xóa đi
                            localStorage.removeItem('chatbot_login_token');
                            localStorage.removeItem('chatbot_login_time');
                        }
                    }
                } catch (e) {
                    console.error('Không thể đọc token từ localStorage:', e);
                }
            }
            return null;
        }
        
        // Xóa token khỏi localStorage
        function removeTokenFromLocalStorage() {
            if (isLocalStorageAvailable()) {
                try {
                    localStorage.removeItem('chatbot_login_token');
                    localStorage.removeItem('chatbot_login_time');
                    return true;
                } catch (e) {
                    console.error('Không thể xóa token khỏi localStorage:', e);
                    return false;
                }
            }
            return false;
        }
        
        // Kiểm tra token trong URL và lưu vào localStorage
        function checkAndSaveTokenFromURL() {
            const urlParams = new URLSearchParams(window.location.search);
            const token = urlParams.get('token');
            
            if (token) {
                saveTokenToLocalStorage(token);
                // Xóa token khỏi URL để bảo mật
                urlParams.delete('token');
                const newUrl = window.location.pathname + (urlParams.toString() ? '?' + urlParams.toString() : '');
                window.history.replaceState({}, document.title, newUrl);
            }
        }
        
        // Thêm token vào URL nếu cần
        function addTokenToURL() {
            const token = getTokenFromLocalStorage();
            if (token) {
                const urlParams = new URLSearchParams(window.location.search);
                if (!urlParams.has('token')) {
                    urlParams.set('token', token);
                    const newUrl = window.location.pathname + '?' + urlParams.toString();
                    window.history.replaceState({}, document.title, newUrl);
                }
            }
        }
        
        // Khởi tạo khi trang load
        function init() {
            // Kiểm tra và lưu token từ URL
            checkAndSaveTokenFromURL();
            
            // Thêm token vào URL nếu có trong localStorage
            addTokenToURL();
            
            // Lắng nghe sự kiện storage để đồng bộ giữa các tab
            if (isLocalStorageAvailable()) {
                window.addEventListener('storage', function(e) {
                    if (e.key === 'chatbot_login_token') {
                        if (e.newValue) {
                            // Token mới được lưu
                            addTokenToURL();
                        } else {
                            // Token bị xóa
                            const urlParams = new URLSearchParams(window.location.search);
                            urlParams.delete('token');
                            const newUrl = window.location.pathname + (urlParams.toString() ? '?' + urlParams.toString() : '');
                            window.history.replaceState({}, document.title, newUrl);
                        }
                    }
                });
            }
        }
        
        // Export functions để sử dụng từ Python
        window.PersistentLogin = {
            saveToken: saveTokenToLocalStorage,
            getToken: getTokenFromLocalStorage,
            removeToken: removeTokenFromLocalStorage,
            init: init
        };
        
        // Khởi tạo khi DOM ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
        
    })();
    </script>
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