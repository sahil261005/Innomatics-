import os
from dotenv import load_dotenv

# load the env file
load_dotenv()

# config variables that I use everywhere
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CHROMA_DB_DIR = "my_chroma_db"
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 200
    EMBEDDING_MODEL = "text-embedding-3-small"
    LLM_MODEL = "gpt-4-turbo-preview" # or gpt-3.5-turbo if it's too expensive
    CONFIDENCE_THRESHOLD = 0.5
    RETRIEVER_K = 3
