import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
faiss_store_path = os.path.join(project_root, "vector", "faiss_store")

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = FAISS.load_local(faiss_store_path, embedding_model, allow_dangerous_deserialization=True)

num_vectors = db.index.ntotal
num_metadata = len(db.docstore._dict) 

print(f"Số vector trong FAISS store: {num_vectors}")
print(f"Số metadata trong docstore: {num_metadata}")

if num_vectors == num_metadata:
    print("✅ Số lượng vector và metadata trùng khớp.")
else:
    print("❌ Số lượng vector và metadata KHÔNG trùng khớp.")
