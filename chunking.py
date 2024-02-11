from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import Chroma
#from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
#from langchain.retrievers.self_query.base import SelfQueryRetriever
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

print('STEP 1: Splitting article into the following segments...','\n\n\n')
texts = r_splitter.split_text(article)
for i in range(len(texts)):
    text = texts[i]
    print(f"Segment {i}:")
    print(text)

# Embedding function
print('\n\n\n STEP 2: Initializing the model...')
#embedding_function = OpenAIEmbeddings()
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
#check model choice

query = "What companies are supporting the development of Starlab Space's forthcoming space station?"
print('\n\n\nSTEP 3: Answer the user\'s query!')
print('Sample User Query:', query)

### OpenAIEmbeddings ###
# vectordb = Chroma.from_texts(
#     texts=docs,
#     embedding=embedding_function,
#     persist_directory = "myvecdb"
# )
# print(vectordb._collection.count())

### - sentence transformer - ### 
vectordb = Chroma.from_texts(texts, embedding_function, persist_directory = "myvecdb")
print(vectordb._collection.count())
docs = vectordb.similarity_search(query)
print("Result: \n", docs[0].page_content)