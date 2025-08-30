class Generator:
    def __init__(self):
        pass

    def generate_response(self, retrieved_info):
        if not retrieved_info or retrieved_info.strip() == "":
            return "Xin lỗi, tôi không tìm thấy thông tin phù hợp với câu hỏi của bạn."

        response = f"Dựa trên tài liệu, tôi tìm thấy thông tin sau:\n{retrieved_info}"
        return response
