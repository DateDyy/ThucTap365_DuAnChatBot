# Thư mục vector - Lưu trữ và xử lý dữ liệu nhúng FAISS

Thư mục `vector` dùng để lưu trữ các file dữ liệu nhúng (embedding) và chỉ mục FAISS phục vụ cho việc tìm kiếm ngữ nghĩa nhanh trong dự án Chatbot RAG về Lập trình Web.

## Cấu trúc thư mục

```
vector/
├── faiss.index           # Chỉ mục FAISS chứa vector embedding của các đoạn văn bản
├── metadata.json         # Thông tin metadata (file, số trang) ứng với từng vector
├── requirements.txt      # Danh sách thư viện cần thiết để chạy các script trong vector
└── src/
    └── data/
        └── build_vector_store.py  # Script xử lý chunking, embedding và tạo FAISS index
```

## Chức năng các file

- **faiss.index**  
  Lưu trữ chỉ mục FAISS, giúp tìm kiếm nhanh các đoạn văn bản liên quan dựa trên vector embedding.

- **metadata.json**  
  Lưu thông tin về nguồn gốc của từng đoạn văn bản (tên file PDF, số trang), dùng để truy xuất lại nội dung gốc khi cần.

- **requirements.txt**  
  Liệt kê các thư viện Python cần thiết:  
  - `faiss-cpu`: Thư viện FAISS cho tìm kiếm vector.
  - `sentence-transformers`: Sinh embedding cho văn bản.
  - `numpy`: Xử lý mảng số.

- **src/data/build_vector_store.py**  
  Script thực hiện các bước:
  1. Đọc dữ liệu từ file JSON đã trích xuất.
  2. Chunking: Chia nhỏ văn bản thành các đoạn ngắn.
  3. Sinh embedding cho từng đoạn bằng mô hình `all-MiniLM-L6-v2`.
  4. Tạo chỉ mục FAISS và lưu metadata.

## Hướng dẫn sử dụng

1. Cài đặt các thư viện cần thiết:
   ```
   pip install -r vector/requirements.txt
   ```

2. Chạy script để tạo FAISS index:
   ```
   python vector/src/data/build_vector_store.py
   ```

Sau khi chạy xong, bạn sẽ có các file `faiss.index` và `metadata.json` sẵn sàng cho việc truy vấn ngữ nghĩa trong chatbot.

---
**Lưu ý:**  
- Đảm bảo file dữ liệu đầu vào (`processed/data_combined.json`) đã được tạo trước đó.
- Các file trong thư mục này chỉ phục vụ cho việc tìm kiếm và truy vấn nhanh, không chứa toàn bộ nội dung văn bản gốc.