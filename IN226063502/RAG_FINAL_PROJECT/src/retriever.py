from src.vector_store import load_vector_store
from src.config import Config

def get_retriever():
    # returns the retriever so we can search the db
    db = load_vector_store()
    if db == None:
        print("error: db not loaded!")
        return None
        
    # k is how many results we want to get back
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": Config.RETRIEVER_K}
    )
    return retriever
