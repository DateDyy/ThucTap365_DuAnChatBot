import json
import os
import hashlib
from datetime import datetime

# File lưu trữ thông tin người dùng
USER_DB_FILE = "users.json"

def hash_password(password):
    """Mã hóa mật khẩu bằng SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Tải danh sách người dùng từ file"""
    if os.path.exists(USER_DB_FILE):
        try:
            with open(USER_DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    else:
        return {}

def save_users(users):
    """Lưu danh sách người dùng vào file"""
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f)

def register_user(email, password, name):
    """Đăng ký người dùng mới"""
    users = load_users()
    
    # Kiểm tra email đã tồn tại chưa
    if email in users:
        return False, "Email đã được sử dụng!"
    
    # Thêm người dùng mới
    users[email] = {
        "password": hash_password(password),
        "name": name,
        "created_at": datetime.now().isoformat(),
        "last_login": None
    }
    
    save_users(users)
    return True, "Đăng ký thành công!"

def login_user(email, password):
    """Đăng nhập người dùng"""
    users = load_users()
    
    # Kiểm tra email tồn tại
    if email not in users:
        return False, "Email hoặc mật khẩu không đúng!"
    
    # Kiểm tra mật khẩu
    if users[email]["password"] != hash_password(password):
        return False, "Email hoặc mật khẩu không đúng!"
    
    # Cập nhật thời gian đăng nhập
    users[email]["last_login"] = datetime.now().isoformat()
    save_users(users)
    
    return True, "Đăng nhập thành công!"

def get_user_info(email):
    """Lấy thông tin người dùng"""
    users = load_users()
    
    if email in users:
        user_info = users[email].copy()
        # Xóa thông tin nhạy cảm
        if "password" in user_info:
            del user_info["password"]
        return user_info
    
    return None

def update_user_info(email, name=None):
    """Cập nhật thông tin người dùng"""
    users = load_users()
    
    if email in users:
        if name:
            users[email]["name"] = name
        
        save_users(users)
        return True, "Cập nhật thông tin thành công!"
    
    return False, "Không tìm thấy người dùng!"