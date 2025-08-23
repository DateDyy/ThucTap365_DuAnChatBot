import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
input_json = os.path.join(project_root, "processed", "data_combined.json")
output_vector = os.path.join(project_root, "vector", "faiss.index")
output_meta = os.path.join(project_root, "vector", "metadata.json")

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
            chunks.append(chunk)
            metadatas.append({
                "file": entry.get("file"),
                "page": entry.get("page")
            })

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