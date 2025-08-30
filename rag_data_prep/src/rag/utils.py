import re
import unicodedata
from typing import List

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'\s+', ' ', text)  
    return text.strip()

def format_response(response: str) -> str:
    if not isinstance(response, str):
        return ""
    return response.replace('\n', ' ').strip()

def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    if not isinstance(text, str):
        return []
    cleaned = re.sub(r'[^a-zA-Z0-9\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]', '', text.lower())
    return cleaned.split()[:max_keywords]

def calculate_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    if not set1 or not set2:
        return 0.0
    return len(set1 & set2) / float(len(set1 | set2))
