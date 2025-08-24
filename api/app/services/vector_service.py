import faiss
import json
import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS index + metadata
def load_faiss_index(index_path: str, metadata_path: str):
    index = faiss.read_index(index_path)
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return FAISS(embedding_model.embed_query, index, InMemoryDocstore({}), metadata)

db = load_faiss_index("vector/embeddings/faiss.index", "vector/embeddings/metadata.json")

# --- NEW: thêm tài liệu ---
def add_document(text: str, metadata: dict):
    vector = embedding_model.embed_query(text)
    db.index.add(np.array([vector], dtype=np.float32))
    db.docstore.add({len(db.docstore._dict): text})
    db.index.ntotal

    # Cập nhật metadata.json
    with open("vector/embeddings/metadata.json", "r", encoding="utf-8") as f:
        old_meta = json.load(f)
    old_meta[str(len(old_meta))] = metadata
    with open("vector/embeddings/metadata.json", "w", encoding="utf-8") as f:
        json.dump(old_meta, f, ensure_ascii=False, indent=2)

    # Ghi lại FAISS index
    faiss.write_index(db.index, "vector/embeddings/faiss.index")
