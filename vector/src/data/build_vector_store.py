import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
input_json = os.path.join(project_root, "processed", "data_combined.json")
output_vector = os.path.join(project_root, "vector", "faiss.index")
output_meta = os.path.join(project_root, "vector", "metadata.json")

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Đọc dữ liệu
with open(input_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Chunking: chia nhỏ văn bản (mỗi chunk ~200 từ)
def chunk_text(text, max_words=200):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

chunks = []
metadatas = []
for entry in data:
    for chunk in chunk_text(entry["text"]):
        if chunk.strip():
            chunks.append(chunk)  # chunk là chuỗi văn bản
            metadatas.append({
                "file": entry.get("file"),
                "page": entry.get("page")
            })  # metadata là dict, nhưng lưu riêng

# Embedding
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks, show_progress_bar=True)

# FAISS
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings))

# Lưu FAISS index và metadata
faiss.write_index(index, output_vector)
with open(output_meta, "w", encoding="utf-8") as f:
    json.dump(metadatas, f, ensure_ascii=False, indent=2)

print(f"Đã lưu {len(chunks)} chunk vào {output_vector} và {output_meta}")

# Đảm bảo chỉ lưu text vào FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# chunks: list các chuỗi văn bản
# metadatas: list các dict metadata
db = FAISS.from_texts(chunks, embedding_model, metadatas=metadatas)
output_dir = os.path.join(project_root, "vector", "faiss_store")
db.save_local(output_dir)