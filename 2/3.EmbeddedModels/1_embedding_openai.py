from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions=32
)

documents = [
    "Tokyo is a capital of Japan",
    "Berlin is a capital of Germany",
    "Paris is a capital of France"
]

result = embedding.embed_query("How to learn Japanese")

result1 = embedding.embed_documents(documents)

print(str(result))
print(str(result1))
