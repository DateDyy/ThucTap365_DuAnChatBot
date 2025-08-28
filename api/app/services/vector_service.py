import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Đường dẫn FAISS store (sau khi build bằng build_vector_store.py)
VECTOR_STORE_DIR = os.path.join("vector", "faiss_store")

# Khởi tạo mô hình embedding
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# --- Load FAISS store ---
def load_faiss_store(path: str = VECTOR_STORE_DIR):
    if not os.path.exists(path):
        raise FileNotFoundError(f"FAISS store không tồn tại tại: {path}")
    return FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)

db = load_faiss_store()

# --- Thêm tài liệu mới ---
def add_document(text: str, metadata: dict = None):
    """
    Thêm một document mới vào FAISS store và lưu lại.
    :param text: Nội dung văn bản
    :param metadata: Metadata kèm theo (dict)
    """
    global db
    db.add_texts([text], metadatas=[metadata] if metadata else None)
    db.save_local(VECTOR_STORE_DIR)
    print(f"Đã thêm document mới vào FAISS store ({VECTOR_STORE_DIR})")
