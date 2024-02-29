from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
import json 
from langchain.text_splitter import RecursiveCharacterTextSplitter

with open("../data/formatted_docs.json", "r") as json_file:
    docs_dicts = json.load(json_file)

docs = []
#docs_dicts[0:5]
count = 1
for doc_dict in docs_dicts:
    doc = Document(page_content=doc_dict["page_content"],metadata=doc_dict["metadata"])
    docs.append(doc)
    print(count)
    count += 1

print("splitting...")
text_splitter = RecursiveCharacterTextSplitter(
 separators=["\n"], chunk_size=1000, chunk_overlap=0, keep_separator=False
)
chunks = text_splitter.split_documents(docs)

print("embedding function...")
# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

print("load...")
# load it into Chroma
db = Chroma.from_documents(chunks, embedding_function, persist_directory="../vector_db")