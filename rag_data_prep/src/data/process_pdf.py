import fitz  
import json
import os

def extract_text_from_pdf(pdf_path):
    text_per_page = []
    with fitz.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf, start=1):
            text = page.get_text("text") or ""  
            text_per_page.append({
                "page": page_num,
                "text": text
            })
    return text_per_page

def process_all_pdfs(pdf_directory,
                     output_json=os.path.join("processed", "data_combined.json"),
                     output_txt=os.path.join("processed", "data_combined.txt")):
    all_data = []

    processed_dir = os.path.dirname(output_json)
    if processed_dir and not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            pages = extract_text_from_pdf(pdf_path)
            for page in pages:
                all_data.append({
                    "file": filename,
                    "page": page["page"],
                    "text": page["text"].strip()
                })

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    with open(output_txt, "w", encoding="utf-8") as f:
        for entry in all_data:
            f.write(entry["text"] + "\n\n")

    print(f"Trích xuất xong {len(all_data)} trang từ {pdf_directory}")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    pdf_folder = os.path.join(project_root, "pdfs")
    print("Đang lấy PDF từ:", pdf_folder)
    process_all_pdfs(pdf_folder)
    print("Xử lý hoàn tất. Dữ liệu đã được lưu vào:", os.path.join(project_root, "processed"))
