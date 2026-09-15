import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


video_id = "Gfr50f6ZBvo"

try:

    api = YouTubeTranscriptApi()

    transcript = api.fetch(
        video_id,
        languages=["en"]
    )

    transcript = " ".join(
        snippet.text
        for snippet in transcript
    )

    print("\nTranscript successfully loaded!")
    print("Transcript length:", len(transcript))

except TranscriptsDisabled:

    print("No captions available for this video.")
    exit()


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.create_documents(
    [transcript]
)

print("\nNumber of chunks:", len(chunks))


print("\nCreating embeddings...")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Creating FAISS vector store...")

vector_store = FAISS.from_documents(
    chunks,
    embedding_model
)

print("FAISS vector store created!")

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 4
    }
)


llm = ChatGroq(
    model_name="openai/gpt-oss-20b",
    temperature=0.2
)


prompt = PromptTemplate(
    template="""
You are a helpful assistant.

Answer ONLY from the provided YouTube transcript context.

If the context is insufficient, say:
"I don't know based on the provided transcript."

Context:
{context}

Question:
{question}
""",
    input_variables=[
        "context",
        "question"
    ]
)


def format_docs(retrieved_docs):

    context_text = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    return context_text


parallel_chain = RunnableParallel(
    {
        "context": retriever | RunnableLambda(format_docs),

        "question": RunnablePassthrough()
    }
)


parser = StrOutputParser()

main_chain = (
    parallel_chain | prompt | llm | parser
)


question = input("\nAsk something about the video: ")


answer = main_chain.invoke(question)

print("ANSWER")


print(answer)