from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model='sentence-transformers/all-MiniLM-L6-v2'
)

text = "Jaipur is a capital of Rajasthan"

documents = [
    "Tokyo is a capital of Japan",
    "Berlin is a capital of Germany",
    "Paris is a capital of France"
]

vector = embedding.embed_query(text)

vector1 = embedding.embed_query(documents)


print(str(vector))
print(str(vector1))

