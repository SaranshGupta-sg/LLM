from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

documents = [

    Document(
        page_content="LangChain helps developers build LLM applications easily."
    ),

    Document(
        page_content="Chroma is a vector database optimized for LLM-based search."
    ),

    Document(
        page_content="Embeddings convert text into high-dimensional vectors."
    ),

    Document(
        page_content="OpenAI provides powerful embedding models."
    )
]


vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    collection_name="my_collection"
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)


query = "What is Chroma used for?"


results = retriever.invoke(query)


for i, doc in enumerate(results):
    print(f"\n--- Retriever Result {i + 1} ---")
    print(doc.page_content)


results = vectorstore.similarity_search(
    query,
    k=2
)

print("DIRECT SIMILARITY SEARCH")

for i, doc in enumerate(results):
    print(f"\n--- Result {i + 1} ---")
    print(doc.page_content)