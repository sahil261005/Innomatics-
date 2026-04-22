# RAG Customer Support Bot
This is my internship project! It is a RAG-based AI support bot built with LangGraph and ChromaDB. It handles retrieving info from PDFs, and if it gets confused, it escalates to a human (HITL).

## 📂 Docs
You can read about how I designed this in the `docs/` folder:
- [High Level Design (HLD)](docs/HLD.md)
- [Low Level Design (LLD)](docs/LLD.md)
- [Technical Documentation](docs/TechnicalDocumentation.md)

## 🚀 How to run it
1. Install everything:
   ```bash
   pip install -r requirements.txt
   ```

2. Add your API key:
   Rename `.env.template` to `.env` and add your OpenAI key.

3. Load a manual/document:
   ```bash
   python -m src.main --add_file custom_manual.pdf
   ```

4. Ask a question:
   ```bash
   python -m src.main --ask "how do i reset the router?"
   ```
