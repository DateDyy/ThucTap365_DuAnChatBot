import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Xác định đường dẫn project và FAISS store
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
faiss_store_path = os.path.join(project_root, "vector", "faiss_store")

# Load embedding model (phải trùng với lúc build)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS store
db = FAISS.load_local(faiss_store_path, embedding_model, allow_dangerous_deserialization=True)

# Đếm số lượng vector
num_vectors = db.index.ntotal
num_metadata = len(db.docstore._dict)  # LangChain lưu metadata trong docstore

print(f"Số vector trong FAISS store: {num_vectors}")
print(f"Số metadata trong docstore: {num_metadata}")

if num_vectors == num_metadata:
    print("✅ Số lượng vector và metadata trùng khớp.")
else:
    print("❌ Số lượng vector và metadata KHÔNG trùng khớp.")
