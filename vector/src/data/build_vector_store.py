import os
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
input_json = os.path.join(project_root, "processed", "data_combined.json")
output_dir = os.path.join(project_root, "vector", "faiss_store")

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Đọc dữ liệu
with open(input_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Chunking
def chunk_text(text, max_words=200):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

chunks = []
metadatas = []
for entry in data:
    for chunk in chunk_text(entry["text"]):
        if chunk.strip():
            chunks.append(chunk)
            metadatas.append({
                "file": entry.get("file"),
                "page": entry.get("page")
            })

db = FAISS.from_texts(chunks, embedding_model, metadatas=metadatas)
db.save_local(output_dir)

print(f"Đã lưu {len(chunks)} chunk vào {output_dir}")
