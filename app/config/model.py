from langchain_cohere import ChatCohere
from app.config.env import COHERE_API_KEY

cohere = ChatCohere(
    cohere_api_key=COHERE_API_KEY
)
