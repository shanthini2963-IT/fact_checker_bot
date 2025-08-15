import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
    SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", None)
    DEFAULT_MODEL = "mixtral-8x7b-32768" 
    SEARCH_RESULTS_LIMIT = 5