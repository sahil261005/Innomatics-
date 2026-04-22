from langchain_community.vectorstores import Chroma
from src.embeddings import get_embeddings_model
from src.config import Config
import os

def create_vector_store(chunks):
    # saves chunks to the database folder
    embed_model = get_embeddings_model()
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embed_model,
        persist_directory=Config.CHROMA_DB_DIR
    )
    db.persist()
    print("saved into database")
    return db

def load_vector_store():
    # loads the database back from memory
    embed_model = get_embeddings_model()
    
    if os.path.exists(Config.CHROMA_DB_DIR) == False:
        print("no db found, maybe run ingest first")
        return None
        
    db = Chroma(
        persist_directory=Config.CHROMA_DB_DIR,
        embedding_function=embed_model
    )
    return db
