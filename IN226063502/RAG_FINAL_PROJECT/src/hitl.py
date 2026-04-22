import json

def escalate_to_human(state):
    # called when the bot doesnt know the answer and needs human help
    print("\n--- SENDING TO HUMAN AGENT... ---")
    
    ticket = {
        "status": "escalated required",
        "user_query": state.get("query"),
        "confidence_score": state.get("confidence", 0.0),
        "reason": "bot is not confident enough"
    }
    
    # just print it for now, later maybe connect to zendesk api
    print("Ticket Details:")
    print(json.dumps(ticket, indent=4))
    
    # updating state
    state["response"] = "Sorry, I'm not sure. I have escalated this to a real human to help you."
    state["escalated"] = True
    return dict(state)
