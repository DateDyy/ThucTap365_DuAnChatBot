# Configuration settings for the chatbot application

# File paths
PDFS_PATH = 'pdfs/'
PDF_FILES = [
    'web_programming_1.pdf',
    'web_programming_2.pdf',
    'web_programming_3.pdf',
    'web_programming_4.pdf',
    'web_programming_5.pdf'
]

# Model parameters
MODEL_NAME = 'gpt-3.5-turbo'  # Example model name, adjust as necessary
MAX_TOKENS = 150  # Maximum tokens for response generation
TEMPERATURE = 0.7  # Sampling temperature for response variability

# Other constants
DEBUG_MODE = True  # Set to False in production
LOGGING_LEVEL = 'INFO'  # Logging level for the application