from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    r'D:\CodewithHarry\LLM\2\9.Loaders\dl-curriculum.pdf'
)

docs = loader.load()

print(len(docs))

print(docs[0].page_content)
print(docs[1].metadata)