# High Level Design for Customer Support Bot

## 1. System Overview
**Problem:** Support teams get the same simple questions every day. 
**Scope:** This bot reads our manuals (PDF files), tries to find the answer using a database, and gives it to the user. If the AI is not sure, it won't lie. It just tells a real human support agent to take over.

## 2. Architecture Diagram (CLI/Backend)
I made a drawing of how the info moves around:

```text
 PDF file ---> [Split text] ---> [OpenAI Embed] ---> [Save to local ChromaDB]

 User asks question ---> [Database checks for related text] ---> [GPT-4 thinks]
 
 GPT-4 gives Answer AND a confidence score.
 
 IF confidence >= 0.5:
    Show answer to user
 ELSE:
    Bot says "im confused", sends log to Zendesk/Agent
```

## 3. Component Description
- **Document Loader**: Uses pypdf to read the text inside a file.
- **Chunking Strategy**: A text splitter that chops the whole file into 800 letter blocks.
- **Embedding Model**: OpenAI text-embedding-3-small.
- **Vector Store**: ChromaDB. It stores all the blocks for fast searching later.
- **Retriever**: Langchain retriever that pulls the top 3 best matching chunks.
- **LLM**: ChatGPT (gpt-4) reads the chunks we gave it and tries to answer the user.
- **Graph Workflow Engine**: LangGraph logic library that wires everything together.
- **Routing Layer**: An IF/ELSE logic node evaluating confidence score.
- **HITL Module**: This part is called when the bot is confused, it creates a JSON ticket.

## 4. Data Flow
How data moves from PDF --> Answer:
1. PDF gets loaded and split.
2. Embeddings are created and saved in ChromaDB.
3. User asks a query.
4. Database finds the 3 closest matches.
5. LangGraph passes chunks to LLM.
6. LLM answers. Router analyzes if answer is good. Output is printed to screen or routed to HITL.

## 5. Technology Choices
- **ChromaDB**: Coz it just runs locally as a folder (`chroma_db`) and i dont have to setup a aws server for it.
- **LangGraph**: It's better than standard if/else statements. It makes the flow look like a cool state machine.
- **LLM Choice**: OpenAI, because it is reliable at following instructions and giving proper json output without breaking.

## 6. Scalability Considerations
- **Handling large documents**: If the pdf is too big, chroma db might get slow on my laptop.
- **Increasing query load**: Currently it's a python script, but we can deploy via FastAPI.
- **Latency concerns**: OpenAI api is a bit slow (takes like 3 secs per answer) so maybe we need a loading spinner on the frontend later.
