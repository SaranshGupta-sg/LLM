from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

cm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
    max_completion_tokens=100
)

response = cm.invoke("Hello, explain LangChain in simple words")

print(response.content)