import os
from data.process_pdf import extract_text_from_pdf

class Retriever:
    def __init__(self):
        """
        Khởi tạo Retriever mà không cần truyền trước danh sách PDF.
        """
        self.documents = []

    def load_pdfs(self, *pdf_paths):
        """
        Tải nhiều tệp PDF vào bộ nhớ.
        :param pdf_paths: Danh sách đường dẫn PDF
        """
        for pdf_path in pdf_paths:
            if os.path.exists(pdf_path):
                pages = extract_text_from_pdf(pdf_path)
                # Gộp text từ các trang
                combined_text = "\n".join([page["text"] for page in pages if page["text"]])
                if combined_text.strip():
                    self.documents.append({
                        "path": pdf_path,
                        "content": combined_text
                    })
                else:
                    print(f"⚠️ Tệp {pdf_path} không có nội dung văn bản.")
            else:
                print(f"⚠️ Không tìm thấy tệp: {pdf_path}")

    def get_relevant_info(self, query):
        """
        Truy xuất thông tin liên quan dựa trên từ khóa.
        :param query: Chuỗi truy vấn từ người dùng
        :return: Chuỗi văn bản chứa thông tin liên quan
        """
        if not self.documents:
            return "Chưa có dữ liệu PDF nào được tải vào hệ thống."

        query_lower = query.lower()
        relevant_docs = []

        for doc in self.documents:
            if query_lower in doc["content"].lower():
                relevant_docs.append(f"Tài liệu: {doc['path']}\n{doc['content'][:500]}...")

        if not relevant_docs:
            return "Không tìm thấy thông tin phù hợp trong tài liệu."

        return "\n\n".join(relevant_docs)