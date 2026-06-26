from langchain_google_genai import ChatGoogleGenerativeAI
from src.controller.ai.open_ai_llm import get_sql_from_query
from src.helper.config import Settings


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=Settings().GOOGLE_API_KEY,
    temperature=0
)
