from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path):
    # loads a pdf file so we can chunk it later
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        print(f"succesfully loaded {len(docs)} pages.")
        return docs
    except Exception as e:
        print(f"failed to load pdf: {e}")
        return None
