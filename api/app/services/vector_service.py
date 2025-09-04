import os
from langchain_community.vectorstores import FAISS

VECTOR_STORE_DIR = os.path.join("vector", "faiss_store")

# Biến toàn cục để lưu trữ mô hình nhúng
embedding_model = None

def get_embedding_model():
    """Khởi tạo mô hình nhúng với lazy loading."""
    global embedding_model
    if embedding_model is None:
        from langchain_huggingface import HuggingFaceEmbeddings
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedding_model

def load_faiss_store(path: str = VECTOR_STORE_DIR):
    """Tải FAISS store từ đường dẫn."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"FAISS store không tồn tại tại: {path}")
    return FAISS.load_local(path, get_embedding_model(), allow_dangerous_deserialization=True)

db = load_faiss_store()

def add_document(text: str, metadata: dict = None):
    """Thêm tài liệu mới vào FAISS store."""
    global db
    db.add_texts([text], metadatas=[metadata] if metadata else None)
    db.save_local(VECTOR_STORE_DIR)
    print(f"Đã thêm document mới vào FAISS store ({VECTOR_STORE_DIR})")
