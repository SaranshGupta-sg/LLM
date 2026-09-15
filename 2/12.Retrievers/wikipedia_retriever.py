from langchain_community.retrievers import WikipediaRetriever


# Create Wikipedia Retriever
retriever = WikipediaRetriever(
    top_k_results=2,
    lang="en"
)


# Query
query = "the geopolitical history of India and Pakistan from the perspective of a Chinese"


# Retrieve relevant Wikipedia documents
docs = retriever.invoke(query)


# Print results
for i, doc in enumerate(docs):

    print(f"\n--- Result {i + 1} ---")

    print("Content:")
    print(doc.page_content[:1000])

    print("\nMetadata:")
    print(doc.metadata)