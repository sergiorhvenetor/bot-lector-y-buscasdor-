
from langchain_cohere import ChatCohere
from app.config.env import COHERE_API_KEY, TAVILY_API_KEY
from tavily import TavilyClient



cohere = ChatCohere(
    cohere_api_key=COHERE_API_KEY

)


tavily = TavilyClient(
    api_key=TAVILY_API_KEY
)
