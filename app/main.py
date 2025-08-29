from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from app.agent.agent_basico import agent
from app.config.model import cohere
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(
    title="Tavily API",
    description="API for Tavily, a platform for AI-powered chatbots.",
)

class ChatSchema(BaseModel):
    question: str
    

@app.post("/chat")
async def chat(request: ChatSchema):
    init_State = {"messages": [HumanMessage(content=request.question)]}
    response = agent.invoke(init_State)
    return {"response": response["messages"][-1].content}