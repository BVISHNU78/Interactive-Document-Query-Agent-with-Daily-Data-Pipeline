from fastapi import FastAPI
from pydantic import BaseModel
from app import run_conversation

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat_with_agent(request: QueryRequest):
    response = await run_conversation(user_query=request.query)
    return {"response": response}