from rag.retriever import Retriever
from rag.generator import Generator

def main():
    # Initialize the retriever and generator
    retriever = Retriever()
    generator = Generator()

    # Load PDF files
    retriever.load_pdfs('pdfs/web_programming_1.pdf', 'pdfs/web_programming_2.pdf', 
                        'pdfs/web_programming_3.pdf', 'pdfs/web_programming_4.pdf', 
                        'pdfs/web_programming_5.pdf')

    print("Chatbot is ready to assist you with web programming questions!")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Chatbot: Goodbye!")
            break
        
        # Retrieve relevant information based on user input
        relevant_info = retriever.get_relevant_info(user_input)
        
        # Generate a response based on the retrieved information
        response = generator.generate_response(relevant_info)
        
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()