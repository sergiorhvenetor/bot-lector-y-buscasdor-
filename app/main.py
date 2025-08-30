from fastapi import FastAPI
from langchain_core.messages import HumanMessage
import shutil
import os
import base64
from app.schemas import UserChatMessage
from app.agent.agent_basico import agent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Tavily API",
    description="API for Tavily, a platform for AI-powered chatbots.",
)

@app.post("/chat")
async def chat(message: UserChatMessage):
    file_path = None
    text_content = ""

    for part in message.content:
        if part.type == "text":
            text_content = part.text
        elif part.type == "file":
            temp_dir = "temp_files"
            os.makedirs(temp_dir, exist_ok=True)

            # Extract file name from mime_type for simplicity, or generate one
            # This is a simplification. In a real app, you might want a better way to name files.
            file_extension = part.mime_type.split("/")[-1]
            file_name = f"uploaded_file.{file_extension}"
            file_path = os.path.join(temp_dir, file_name)

            file_data = base64.b64decode(part.data)

            with open(file_path, "wb") as buffer:
                buffer.write(file_data)

    if file_path:
        question_with_file = f"{text_content}\n\nHere is the path to the file you need to summarize: {file_path}"
        init_State = {"messages": [HumanMessage(content=question_with_file)]}
    else:
        init_State = {"messages": [HumanMessage(content=text_content)]}

    response = agent.invoke(init_State)

    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    return {"response": response["messages"][-1].content}
