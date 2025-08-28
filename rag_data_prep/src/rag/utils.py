import re
import unicodedata
from typing import List

def clean_text(text: str) -> str:
    """
    Làm sạch và tiền xử lý văn bản.
    - Loại bỏ khoảng trắng dư thừa
    - Chuẩn hóa Unicode (NFKC)
    - Xóa ký tự không cần thiết
    """
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'\s+', ' ', text)  # thay nhiều khoảng trắng bằng 1
    return text.strip()

def format_response(response: str) -> str:
    """
    Định dạng phản hồi của chatbot để dễ đọc hơn.
    - Xóa khoảng trắng thừa
    - Thay dấu xuống dòng bằng khoảng trắng
    """
    if not isinstance(response, str):
        return ""
    return response.replace('\n', ' ').strip()

def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """
    Trích xuất từ khóa cơ bản từ văn bản.
    - Loại bỏ ký tự đặc biệt
    - Chuyển về chữ thường
    - Cắt thành từ và lấy số lượng giới hạn
    """
    if not isinstance(text, str):
        return []
    cleaned = re.sub(r'[^a-zA-Z0-9\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]', '', text.lower())
    return cleaned.split()[:max_keywords]

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Tính độ tương đồng Jaccard giữa hai văn bản (dạng đơn giản).
    - Trả về giá trị từ 0.0 (không giống) đến 1.0 (giống hoàn toàn)
    """
    if not text1 or not text2:
        return 0.0
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    if not set1 or not set2:
        return 0.0
    return len(set1 & set2) / float(len(set1 | set2))
