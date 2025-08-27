import faiss
import json
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

# Khởi tạo mô hình embedding
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS index + metadata
from langchain.schema import Document

def load_faiss_index(index_path: str, metadata_path: str):
    # Đọc FAISS index
    index = faiss.read_index(index_path)

    # Đọc metadata (list)
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata_list = json.load(f)

    # Tạo danh sách Document (chỉ chứa metadata)
    documents = [
        Document(page_content="", metadata=item)
        for item in metadata_list
    ]

    # Khởi tạo FAISS từ index có sẵn
    return FAISS(
        embedding_model,
        index,
        InMemoryDocstore({str(i): doc for i, doc in enumerate(documents)}),
        {str(i): doc.metadata for i, doc in enumerate(documents)}
    )

db = load_faiss_index("vector/faiss.index", "vector/metadata.json")

# --- Thêm tài liệu mới ---
def add_document(text: str, metadata: dict):
    vector = embedding_model.embed_query(text)
    db.index.add(np.array([vector], dtype=np.float32))
    db.docstore.add({len(db.docstore._dict): text})

    # Cập nhật metadata.json
    with open("vector/metadata.json", "r", encoding="utf-8") as f:
        old_meta = json.load(f)
    old_meta[str(len(old_meta))] = metadata
    with open("vector/metadata.json", "w", encoding="utf-8") as f:
        json.dump(old_meta, f, ensure_ascii=False, indent=2)

    # Ghi lại FAISS index
    faiss.write_index(db.index, "vector/faiss.index")