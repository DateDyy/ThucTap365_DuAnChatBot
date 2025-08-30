# Chatbot RAG Cho lập trình Web

Dự án này nhằm mục tiêu nâng cao trải nghiệm học tập cho người dùng quan tâm đến lập trình web bằng cách cung cấp một chatbot tương tác và giàu thông tin.

# Thư mục `rag_data_prep` - Xử lý dữ liệu cho Chatbot RAG

Thư mục `rag_data_prep` chứa mã nguồn và tài liệu liên quan đến việc xử lý dữ liệu, chuẩn bị dữ liệu để sử dụng trong hệ thống Chatbot RAG hỗ trợ sinh viên học lập trình web.

---

## Cấu trúc thư mục

```
rag_data_prep/
├── README_data.md          # Tài liệu hướng dẫn cho thư mục rag_data_prep
├── requirements.txt        # Danh sách thư viện cần thiết để xử lý dữ liệu
├── src/
│   ├── main.py             # File chính khởi động quy trình xử lý dữ liệu
│   ├── data/
│   │   ├── process_pdf.py  # Xử lý trích xuất văn bản từ file PDF
│   │   ├── label_data.py   # Gán nhãn dữ liệu dựa trên nội dung
│   └── rag/
│       ├── retriever.py    # Truy vấn thông tin liên quan từ dữ liệu
│       ├── generator.py    # Sinh câu trả lời dựa trên thông tin truy vấn
├── pdfs/                   # Thư mục chứa các file PDF đầu vào
├── processed/              # Thư mục chứa dữ liệu đã xử lý
```

---

## Chức năng các file và thư mục

### **1. README_data.md**
- Tài liệu hướng dẫn sử dụng, cấu trúc và chức năng các file trong thư mục `rag_data_prep`.

### **2. requirements.txt**
- Danh sách các thư viện Python cần thiết để xử lý dữ liệu:
  - `Flask`: Framework web (nếu cần tích hợp).
  - `transformers`: Xử lý mô hình ngôn ngữ lớn.
  - `torch`: Thư viện học sâu.
  - `PyPDF2`: Xử lý file PDF.
  - `nltk`: Xử lý ngôn ngữ tự nhiên.
  - `numpy`, `pandas`: Xử lý dữ liệu.

### **3. src/main.py**
- File khởi động quy trình xử lý dữ liệu và tương tác với người dùng.
- **Chức năng**:
  - Tải dữ liệu từ các file PDF.
  - Tương tác với người dùng để trả lời câu hỏi dựa trên dữ liệu đã xử lý.

### **4. src/data/process_pdf.py**
- **Mục đích**: Trích xuất văn bản từ các file PDF.
- **Chức năng**:
  - Đọc nội dung từng trang của file PDF.
  - Lưu dữ liệu đã trích xuất vào file JSON và TXT.
- **Cách sử dụng**:
  - Chạy lệnh:
    ```bash
    python src/data/process_pdf.py
    ```
  - Dữ liệu sẽ được lưu vào thư mục `processed`.

### **5. src/data/label_data.py**
- **Mục đích**: Gán nhãn dữ liệu dựa trên nội dung.
- **Chức năng**:
  - Gán nhãn chủ đề (HTML, PHP, Django, v.v.) cho từng đoạn văn bản.
  - Làm sạch văn bản để loại bỏ các ký tự không cần thiết.
- **Cách sử dụng**:
  - Chạy lệnh:
    ```bash
    python src/data/label_data.py
    ```
  - Dữ liệu đã gán nhãn sẽ được lưu vào file JSON trong thư mục `processed`.

### **6. src/rag/retriever.py**
- **Mục đích**: Truy vấn thông tin liên quan từ dữ liệu đã xử lý.
- **Chức năng**:
  - Tìm kiếm thông tin phù hợp với câu hỏi của người dùng.

### **7. src/rag/generator.py**
- **Mục đích**: Sinh câu trả lời dựa trên thông tin truy vấn.
- **Chức năng**:
  - Tạo phản hồi tự nhiên và dễ hiểu dựa trên thông tin đã tìm kiếm.

---

## Hướng dẫn sử dụng

### **1. Cài đặt các thư viện cần thiết**
- Tạo môi trường ảo:
  ```bash
  python -m venv venv
  ```
- Kích hoạt môi trường ảo:
  - **Windows**:
    ```bash
    venv\Scripts\activate
    ```
  - **Linux/macOS**:
    ```bash
    source venv/bin/activate
    ```
- Cài đặt các thư viện:
  ```bash
  pip install -r rag_data_prep/requirements.txt
  ```

---

### **2. Xử lý dữ liệu từ file PDF**
- Đảm bảo các file PDF được lưu trong thư mục `pdfs`.
- Chạy lệnh sau để trích xuất văn bản từ các file PDF:
  ```bash
  python src/data/process_pdf.py
  ```
- Dữ liệu đã trích xuất sẽ được lưu vào thư mục `processed`.

---

### **3. Gán nhãn dữ liệu**
- Chạy lệnh sau để gán nhãn chủ đề cho dữ liệu:
  ```bash
  python src/data/label_data.py
  ```
- Dữ liệu đã gán nhãn sẽ được lưu vào file JSON trong thư mục `processed`.

---

### **4. Tương tác với Chatbot**
- Chạy lệnh sau để khởi động chatbot:
  ```bash
  python src/main.py
  ```
- Nhập câu hỏi của bạn và nhận phản hồi từ chatbot.

---

### **5. Lưu ý**
- Đảm bảo các file PDF đầu vào được lưu trong thư mục `pdfs`.
- Kiểm tra thư mục `processed` để xác nhận dữ liệu đã được xử lý thành công.