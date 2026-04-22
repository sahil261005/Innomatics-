import os
import argparse
from src.document_loader import load_pdf
from src.chunker import split_documents
from src.vector_store import create_vector_store
from src.langgraph_workflow import setup_graph
from src.config import Config

def add_document(pdf_path):
    print("starting to process file:", pdf_path)
    docs = load_pdf(pdf_path)
    if docs:
        chunks = split_documents(docs)
        create_vector_store(chunks)
        print("all done processing pdf!")
        
def ask_question(query):
    # runs the bot
    print("asking question:", query)
    app = setup_graph()
    
    start_state = {
        "query": query,
        "context": "",
        "response": "",
        "confidence": 0.0,
        "escalated": False
    }
    
    # run langgraph
    result = app.invoke(start_state)
    
    print("\n--- RESULTS ---")
    print(f"User asked: {query}")
    print(f"Bot confidence was: {result.get('confidence', 0.0)}")
    print(f"Was it escalated?: {result.get('escalated', False)}")
    print(f"Reply: {result.get('response', '')}")
    print("---------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Customer support bot project")
    parser.add_argument("--add_file", help="Path to pdf to learn from")
    parser.add_argument("--ask", help="Query you want to ask")
    
    args = parser.parse_args()
    
    if args.add_file:
        add_document(args.add_file)
        
    elif args.ask:
        if not os.path.exists(Config.CHROMA_DB_DIR):
            print("warning! u need to run --add_file first so there is a database!")
        ask_question(args.ask)
        
    else:
        print("how to use this:")
        print("python -m src.main --add_file book.pdf")
        print("python -m src.main --ask 'how do i restart router?'")
