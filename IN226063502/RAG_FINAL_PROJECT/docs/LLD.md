# LLD: Custom Bot Project Details

## 1. Module-Level Design
- **Document Processing Module & Chunking Module:** `document_loader.py` and `chunker.py` handles the PDF loading and splitting with `RecursiveCharacterTextSplitter`.
- **Embedding Module & Vector Storage Module:** `embeddings.py` and `vector_store.py` stores the text locally in `Chroma` without needing a cloud.
- **Retrieval Module & Query Processing Module:** `retriever.py` searches the db. `Ask_AI` in graph prompts the LLM.
- **Graph Execution Module:** `langgraph_workflow.py` main logic.
- **HITL Module:** `hitl.py` handles human escalation.

## 2. Data Structures
This is what a data chunk looks like when it's saved (Embedding structure):
```json
{
  "text": "Press power button to restart.",
  "metadata": {"source": "manual.pdf"},
  "embedding": [0.1, -0.4, 0.9]
}
```

This is how LangGraph remembers what happened during a chat (State Object / Query Schema):
```python
class AgentState(TypedDict):
    query: str        # what user said
    context: str      # what db found
    response: str     # what bot answers
    confidence: float # how sure bot is 
    escalated: bool   # true if passed to human
```

## 3. Workflow Design (LangGraph)
- **Nodes**: `start_query` (Input), `search_db` (Processing), `ask_ai` (Processing), `human_handoff` (Output), `finish` (Output).
- **Edges**: The flow goes from start -> db search -> ask AI.
- **State**: The `AgentState` object flows between all these nodes.

## 4. Conditional Routing Logic
The route decision is just a basic python function:
```python
def routing_logic(state):
    conf = state.get("confidence", 0.0)
    # Answer gen criteria -> conf > 0.5
    # Escalation criteria -> conf < 0.5 (low confidence, missing context, complex ask)
    if conf < 0.5:
        return "go_to_human"
    return "go_to_user"
```

## 5. HITL Design
- **When triggered:** If confidence is too low.
- **What happens:** We print out a ticket with the context and user query.
- **Integration:** Currently it just prints the JSON. In the future, a human replies via our helpdesk and we send a webhook back to the user app.

## 6. API / Interface Design
Input format (CLI): string arguments like `--ask "how to fix router"`
Output format: Just prints to console right now.
```text
User asked: how to fix router
Bot confidence was: 0.9
Was it escalated?: False
Reply: Hold the restart button.
```

## 7. Error Handling
- **Missing Data / No chunks found:** It returns `{"context": "no context found"}` and forces the LLM to give 0.0 confidence, triggering HITL.
- **LLM Failure:** I added a `try except` block so it defaults to 0.0 confidence and escalates to human instead of just crashing the whole backend.
