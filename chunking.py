from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os

#openai.api_key = os.environ.get("OPENAI_API_KEY")
embedding = OpenAIEmbeddings()

file_path =  "article.txt"
with open(file_path, "r") as file:
    article = file.read()
print("Contents of the file:\n",article)

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=450,
    chunk_overlap=0, 
    separators=["\n\n", "\n", ".", ""]
)

docs = r_splitter.split_text(article)
for doc in docs:
    print(len(doc), " characters")
    print(doc)

vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory=persist_directory
)

print(vectordb._collection.count())