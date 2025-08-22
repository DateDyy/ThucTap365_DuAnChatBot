import json
import os
import re

def clean_text(text):
    # Gộp nhiều xuống dòng thành 2 (giữ đoạn văn)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Xóa khoảng trắng đầu cuối mỗi dòng
    text = "\n".join(line.strip() for line in text.splitlines())
    # Xóa số trang (dòng chỉ chứa số hoặc số cuối dòng)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n\d+\s*$', '', text)
    # Chuẩn hóa bullet: thay các ký tự bullet phổ biến thành "-"
    text = re.sub(r'^[•●▪▶\-–—]+', '- ', text, flags=re.MULTILINE)
    # Xóa các bullet lặp lại đầu dòng
    text = re.sub(r'^(\- ){2,}', '- ', text, flags=re.MULTILINE)
    # Xóa khoảng trắng thừa, xuống dòng lặp
    text = re.sub(r"\n+", "\n", text)
    return text.strip()

def guess_label_topic(text):
    # Đơn giản: tìm từ khóa chủ đề phổ biến
    topics = {
        "HTML": ["HTML", "siêu văn bản", "Hypertext Markup Language"],
        "PHP": ["PHP", "Hypertext Preprocessor"],
        "ASP.NET": ["ASP.NET", "ASP", "Active Server Pages"],
        "Django": ["Django", "Python"],
        "JavaScript": ["JavaScript", "JS"],
        "SQL": ["SQL", "cơ sở dữ liệu", "MySQL", "PostgreSQL"],
        "Web": ["Web", "website", "lập trình web", "web chuyên sâu"],
    }
    for topic, keywords in topics.items():
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
                return topic
    return "Khác"

def label_data(input_json, output_json):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    labeled = []
    for entry in data:
        text = entry.get("text", "")
        labeled.append({
            "file": entry.get("file", ""),
            "page": entry.get("page", ""),
            "text": text,
            "label_topic": guess_label_topic(text)
            # Không xác định label_chapter nữa
        })
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(labeled, f, ensure_ascii=False, indent=2)
    print(f"Đã gán nhãn {len(labeled)} mục vào {output_json}")

def clean_labeled_json(input_json, output_json):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in data:
        entry["text"] = clean_text(entry["text"])
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Đã làm sạch text cho {len(data)} mục vào {output_json}")

if __name__ == "__main__":
    # Đường dẫn đúng tới file processed
    input_json = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "processed", "data_combined.json")
    output_json = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "processed", "data_labeled.json")
    # Nếu file không tồn tại, thử đường dẫn tuyệt đối
    if not os.path.exists(input_json):
        input_json = r"d:\DAKHMT\ThucTap365_DuAnChatBot\processed\data_combined.json"
        output_json = r"d:\DAKHMT\ThucTap365_DuAnChatBot\processed\data_labeled.json"
    label_data(input_json, output_json)
    clean_labeled_json(output_json, output_json)