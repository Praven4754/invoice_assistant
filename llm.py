from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from tools import tools

load_dotenv(override=True)
# groq_api_key = os.getenv('GROQ_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

llm = ChatOpenAI(
    model_name="gemini-1.5-flash",
    openai_api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

pro_llm = ChatOpenAI(
    model_name="gemini-2.0-flash",
    openai_api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm_with_tools = pro_llm.bind_tools(tools)