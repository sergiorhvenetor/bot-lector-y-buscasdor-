from fastapi import FastAPI, File, UploadFile, Form
from langchain_core.messages import HumanMessage
from typing import Optional
import shutil
import os

from app.agent.agent_basico import agent
from app.config.model import cohere
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Tavily API",
    description="API for Tavily, a platform for AI-powered chatbots.",
)

@app.post("/chat")
async def chat(question: str = Form(...), file: Optional[UploadFile] = File(None)):
    file_path = None
    if file:
        temp_dir = "temp_files"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        question_with_file = f"{question}\n\nHere is the path to the file you need to summarize: {file_path}"
        init_State = {"messages": [HumanMessage(content=question_with_file)]}
    else:
        init_State = {"messages": [HumanMessage(content=question)]}

    response = agent.invoke(init_State)

    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    return {"response": response["messages"][-1].content}
