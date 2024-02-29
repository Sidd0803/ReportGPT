from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import Chroma
#from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain.retrievers.self_query.base import SelfQueryRetriever
import time
import os
#import getpass
#os.environ["OPENAI_API_KEY"] = "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"

file_path =  "article.txt"
with open(file_path, "r") as file:
    article = file.read()

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=450,
    chunk_overlap=0, 
    separators=["\n\n", "\n", ".", ""]
)
print('Loading ReportGPT...\n')
time.sleep(2)
print('Splitting text input into segments...','\n')
texts = r_splitter.split_text(article)
for i in range(len(texts)):
    text = texts[i]
    #print(f"Segment {i}:")
    #print(text)

# Embedding function
print('Initializing the model...\n')
#embedding_function = OpenAIEmbeddings()
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
#check model choice

flag = input("Type \'Y\' to ask me a question. Type \'n\' to exit.\n")
while flag == 'Y':
    query = input("What would you like to know?\n")
    #query = "What companies are supporting the development of Starlab Space's upcoming space station?"
    print(f'Answering the query: {query}')

    ### - sentence transformer - ### 
    vectordb = Chroma.from_texts(texts, embedding_function, persist_directory = "myvecdb")
    docs = vectordb.similarity_search(query)
    print("Result: \n", docs[0].page_content, '\n')
    flag = input("Type \'Y\' to ask me a question. Type \'n\' to exit.\n")