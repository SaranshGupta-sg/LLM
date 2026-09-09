from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

import os

load_dotenv()

cm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
    max_completion_tokens=100
)

response = cm.invoke("Hello, explain LangChain in simple words")

print(response.content)

# for temperature = 0 -> koi esa application banana ho jaha p same input k liye same output to waha p temperature ki value 0 k aas pass rakhni hai
# for temperature = 1.5 -> koi esa application banana ho jaha p same input k liye alag-alag output to waha p temperature ki value 1.5 k aas pass rakhni hai
