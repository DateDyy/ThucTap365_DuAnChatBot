from rag.retriever import Retriever
from rag.generator import Generator
import glob
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(__file__)) 
    pdf_dir = os.path.join(base_dir, "pdfs")
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))

    retriever = Retriever()
    retriever.load_pdfs(*pdf_files)

    print("Chatbot sẵn sàng hỗ trợ bạn với các câu hỏi về lập trình web!")

    while True:
        user_input = input("Bạn: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Chatbot: Tạm biệt!")
            break

        relevant_info = retriever.get_relevant_info(user_input)
        generator = Generator()
        response = generator.generate_response(relevant_info)

        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
