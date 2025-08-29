from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

from app.config.model import cohere

from langchain_tavily import TavilySearch

load_dotenv()
#create tools



search = TavilySearch(
    max_results=5,
    tavily_api_key="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"
)

agent = create_react_agent(
    model=cohere,
    tools=[search],
    prompt=" You are a helpful AI assistant. You can answer questions and perform searches using the Tavily search tool. If you don't know the answer, you can search for it. Use the tools provided to help answer the user's questions, your name is golotus-AI Your answers will be direct but formal."
)