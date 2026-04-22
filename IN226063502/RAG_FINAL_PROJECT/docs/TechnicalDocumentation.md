# Project Documentation

## 1. Introduction
- **What is RAG?** Retrieval-Augmented Generation. 
- **Why is it needed?** Regular LLMs hullucinate or make stuff up. Adding a RAG means we grab our company's real docs first, then say "only answer using this doc".
- **Use case:** Customer support bot that answers manual questions seamlessly.

## 2. System Architecture Explanation
The HLD breaks everything into ingestion (loading pdf, chunking, putting in chromadb) and retrieval (taking user text, finding similar text in database, and passing both to OpenAI). They interact through LangChain abstractions.

## 3. Design Decisions
- **Chunk size choice:** I realized if it's 200, a paragraph gets cut midway. If it's too big, it confuses the AI. 800 tokens is perfect.
- **Embedding strategy:** OpenAI small embeddings, because it captures the meaning of words better than just string matching.
- **Retrieval approach:** Grab top 3 matches using similarity search so we have enough context but dont overload the limit.
- **Prompt design logic:** "You are a support bot. Answer using only the context provided. also give a confidence score (0 to 1)."

## 4. Workflow Explanation
- **LangGraph usage:** Regular chain logic gets messy when you want to do IF/ELSE statements. LangGraph makes it a neat line of nodes.
- **Node responsibilities & State:** I have an input node, a retrieval node, and an ask_ai node. The state variable passes from one to the next holding the query and context. 

## 5. Conditional Logic
- **Intent detection:** I'm not doing a strict NLP classifier. I'm just letting GPT-4 process the context and assign a `confidence` float internally.
- **Routing decisions:** If confidence is under 0.5, we route to human.

## 6. HITL Implementation
HITL = Human in the loop. The role of human intervention is solving complex queries the bot fails at.
- **Benefits:** No hallucinations, better user experience and no wrong answers.
- **Limitations:** Need actual human agents on standby.

## 7. Challenges & Trade-offs
- **Retrieval accuracy vs speed:** Top 3 is fast. Top 10 is accurate but slow.
- **Chunk size vs context quality:** Smaller chunks = less irrelevant noise, but risk missing the main topic sentence.
- **Cost vs performance:** GPT-4 is smart but costs a few cents per query.

## 8. Testing Strategy
- I test by putting in simple questions: "how do i setup?" -> should pass.
- Complex/garbage questions: "adklfasdjf" -> should have low confidence and escalate.

## 9. Future Enhancements
- **Multi-document support:** Allow uploading images or word docs.
- **Feedback loop:** Thumbs up / down interface for the user.
- **Memory integration:** Remembering the previous chat messages.
- **Deployment:** Move it from CLI to a real web server like FastAPI.
