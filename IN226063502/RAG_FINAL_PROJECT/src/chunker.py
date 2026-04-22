from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config import Config

def split_documents(docs):
    # we need to split the text into chunks so it fits into the prompt
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(docs)
    print(f"made {len(chunks)} chunks out of the text")
    return chunks
