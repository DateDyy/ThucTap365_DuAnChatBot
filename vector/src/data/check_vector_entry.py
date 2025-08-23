import os
import faiss
import json

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
faiss_index_path = os.path.join(project_root, "vector", "faiss.index")
metadata_path = os.path.join(project_root, "vector", "metadata.json")

# Đọc FAISS index
index = faiss.read_index(faiss_index_path)
num_vectors = index.ntotal

# Đọc metadata
with open(metadata_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)
num_metadata = len(metadata)

print(f"Số vector trong faiss.index: {num_vectors}")
print(f"Số entry trong metadata.json: {num_metadata}")

if num_vectors == num_metadata:
    print("✅ Số lượng vector và metadata trùng khớp.")
else:
    print("❌ Số lượng vector và metadata KHÔNG trùng khớp.")