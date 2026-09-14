from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model_name='openai/gpt-oss-20b'
)

prompt = PromptTemplate(
    template='Write a summary for the following text - \n {poem}',
    input_variables=['poem']
)

parser = StrOutputParser()

loader = TextLoader(r'D:\CodewithHarry\LLM\2\9.Loaders\cricket.txt',encoding='utf-8')

docs = loader.load()

print(type(docs))

print(len(docs))

print(docs[0].page_content)

print(docs[0].metadata)

chain = prompt | model | parser

print(chain.invoke({
    'poem': docs[0].page_content
}))