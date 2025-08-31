import json
import os
import hashlib
import secrets
from datetime import datetime, timedelta

# File lưu trữ thông tin người dùng
USER_DB_FILE = "users.json"
# File lưu trữ token đăng nhập
TOKEN_DB_FILE = "login_tokens.json"

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

def load_tokens():
    """Tải danh sách token đăng nhập từ file"""
    if os.path.exists(TOKEN_DB_FILE):
        try:
            with open(TOKEN_DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    else:
        return {}

def save_tokens(tokens):
    """Lưu danh sách token đăng nhập vào file"""
    with open(TOKEN_DB_FILE, "w") as f:
        json.dump(tokens, f)

def generate_login_token():
    """Tạo token đăng nhập ngẫu nhiên"""
    return secrets.token_urlsafe(32)

def create_login_token(email, remember_me=False):
    """Tạo token đăng nhập cho người dùng"""
    tokens = load_tokens()
    
    # Xóa token cũ của người dùng này nếu có
    tokens = {token: data for token, data in tokens.items() if data.get('email') != email}
    
    # Tạo token mới
    token = generate_login_token()
    expiry_days = 30 if remember_me else 1  # 30 ngày nếu remember me, 1 ngày nếu không
    expiry_date = datetime.now() + timedelta(days=expiry_days)
    
    tokens[token] = {
        'email': email,
        'created_at': datetime.now().isoformat(),
        'expires_at': expiry_date.isoformat()
    }
    
    save_tokens(tokens)
    return token

def validate_login_token(token):
    """Kiểm tra token đăng nhập có hợp lệ không"""
    tokens = load_tokens()
    
    if token not in tokens:
        return None
    
    token_data = tokens[token]
    
    # Kiểm tra token đã hết hạn chưa
    try:
        expires_at = datetime.fromisoformat(token_data['expires_at'])
        if datetime.now() > expires_at:
            # Xóa token hết hạn
            del tokens[token]
            save_tokens(tokens)
            return None
    except:
        return None
    
    return token_data['email']

def remove_login_token(token):
    """Xóa token đăng nhập"""
    tokens = load_tokens()
    if token in tokens:
        del tokens[token]
        save_tokens(tokens)

def cleanup_expired_tokens():
    """Dọn dẹp các token đã hết hạn"""
    tokens = load_tokens()
    current_time = datetime.now()
    
    expired_tokens = []
    for token, data in tokens.items():
        try:
            expires_at = datetime.fromisoformat(data['expires_at'])
            if current_time > expires_at:
                expired_tokens.append(token)
        except:
            expired_tokens.append(token)
    
    for token in expired_tokens:
        del tokens[token]
    
    if expired_tokens:
        save_tokens(tokens)

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

def login_user(email, password, remember_me=False):
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
    
    # Tạo token đăng nhập
    token = create_login_token(email, remember_me)
    
    return True, "Đăng nhập thành công!", token

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