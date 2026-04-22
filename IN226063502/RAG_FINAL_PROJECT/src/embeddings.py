from langchain_openai import OpenAIEmbeddings
from src.config import Config

def get_embeddings_model():
    # this gets the openai embeddings to convert text to numbers
    if Config.OPENAI_API_KEY is None:
        print("warning: OPENAI_API_KEY is not set!")
        
    embeds = OpenAIEmbeddings(model=Config.EMBEDDING_MODEL)
    return embeds
