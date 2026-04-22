from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from src.retriever import get_retriever
from src.hitl import escalate_to_human
from src.config import Config

# what saving data between steps looks like
class AgentState(TypedDict):
    query: str
    context: str
    response: str
    confidence: float
    escalated: bool

# expected output format from LLM
class ProcessedResponse(BaseModel):
    answer: str = Field(description="Answer the query based on context")
    confidence: float = Field(description="Confidence from 0 to 1")

def input_step(state):
    # just passes the query forward
    return {"query": state["query"]}

def retrieve_step(state):
    # searches database
    my_retriever = get_retriever()
    if my_retriever is None:
        return {"context": "error starting db"}
        
    docs = my_retriever.invoke(state["query"])
    merged_text = ""
    for doc in docs:
        merged_text += doc.page_content + "\n\n"
        
    if merged_text == "":
        return {"context": "no context found"}
        
    return {"context": merged_text}

def llm_step(state):
    # ask chatgpt the question
    try:
        my_llm = ChatOpenAI(model=Config.LLM_MODEL, temperature=0)
        structured_output = my_llm.with_structured_output(ProcessedResponse)
        
        prompt_text = "You are a support bot. Answer using only the context provided. also give a confidence score (0 to 1)."
        prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_text),
            ("human", "Context:\n{context}\n\nQuery:\n{query}")
        ])
        
        chain = prompt | structured_output
        result = chain.invoke({"context": state["context"], "query": state["query"]})
        
        return {"response": result.answer, "confidence": result.confidence}
    except Exception as e:
        print("error in llm step:", e)
        return {"response": "error connecting to AI", "confidence": 0.0}

def routing_logic(state):
    # decides which path to follow
    conf = state.get("confidence", 0.0)
    
    # if it's too low, escalate
    if conf < Config.CONFIDENCE_THRESHOLD:
        return "go_to_human"
    else:
        return "go_to_user"

def hitl_step(state):
    # escalate state function
    return escalate_to_human(state)

def final_output_step(state):
    # just do nothing, we are done
    return {"escalated": False}

def setup_graph():
    # build the actual logic tree
    graph = StateGraph(AgentState)
    
    # register all our functions as nodes
    graph.add_node("start_query", input_step)
    graph.add_node("search_db", retrieve_step)
    graph.add_node("ask_ai", llm_step)
    graph.add_node("human_handoff", hitl_step)
    graph.add_node("finish", final_output_step)
    
    # connect the nodes
    graph.set_entry_point("start_query")
    graph.add_edge("start_query", "search_db")
    graph.add_edge("search_db", "ask_ai")
    
    # add the if/else logic edge
    graph.add_conditional_edges(
        "ask_ai",
        routing_logic,
        {
            "go_to_human": "human_handoff",
            "go_to_user": "finish"
        }
    )
    
    graph.add_edge("human_handoff", END)
    graph.add_edge("finish", END)
    
    return graph.compile()
