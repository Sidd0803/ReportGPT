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

print("splitting...")
text_splitter = RecursiveCharacterTextSplitter(
 separators=["\n"], chunk_size=200, chunk_overlap=0, keep_separator=False, add_start_index=True
)
docs = []
#docs_dicts[0:5]
count = 1
for doc_dict in docs_dicts:
    doc = Document(page_content=doc_dict["page_content"],metadata=doc_dict["metadata"])
    docs.append(doc)
    print(count)
    count += 1
all_splits = text_splitter.split_documents(docs)

###TESTING####
print("length of docs:", len(docs))
print("length of splits:", len(all_splits))
print("length of doc 1:", len(docs[0].page_content))
print("length of split 1:", len(all_splits[0].page_content))
print(docs[0].type)

print("embedding function...(cancelled)")
# create the open-source embedding function
#embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


print("load... (cancelled)")
# load it into Chroma 
#db = Chroma.from_documents(chunks, embedding_function, persist_directory="../vector_db")