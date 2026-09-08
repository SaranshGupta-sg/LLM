from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

response = llm.invoke("Hello, explain LangChain in simple words")

print(response.content)