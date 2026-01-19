from fastapi import FastAPI
from backend.retrieval.search import retrieve_context

app = FastAPI()

@app.get("/chat")
def chat(query: str):
    answer = retrieve_context(query)
    return {"answer": answer}
