import json 
import re
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma

file_path = "../data/metadata.json"
#load data as a string
with open(file_path, 'r') as json_load:
    loaded_string = (json.load(json_load)) 

# #convert to dictionary
res_dict = (json.loads(loaded_string))

# docs = []
urls = []
items = res_dict["items"]
# count = 1
for item in items:
    url = item["newsUrl"]
    urls.append(url)
    #metadata = {}

print("web loader")
loader = WebBaseLoader(urls[30:70])
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
all_splits = text_splitter.split_documents(docs)
#all_splits = docs

new_docs = []
print("format snippets")
for snippet in all_splits:
    text = snippet.page_content
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\t', '', text)
    snippet.page_content = text
    new_doc = {'page_content':snippet.page_content}
    if 'source' in snippet.metadata:
        new_doc['source'] = snippet.metadata['source']
    else:
        new_doc['source'] = "no source provided"
    if 'description' in snippet.metadata:
        new_doc['description'] = snippet.metadata['description']
    else:
        new_doc['description']= "no description provided"
    if 'title' in snippet.metadata:
         new_doc['title'] = snippet.metadata['title']
    else:
        new_doc['title']= "no title provided"
    snippet.metadata = {'source': new_doc['source'], 'title': new_doc['title'], 'description': new_doc['description']}
    new_docs.append(new_doc)
# print([new_doc['page_content'] for new_doc in new_docs])
json_string = json.dumps(new_docs)
with open("../data/formatted_docsv2.json", "w") as json_file:
    json_file.write(json_string)




###TESTING####
print("length of docs:", len(docs))
print("length of splits:", len(all_splits))
print("length of doc 1:", len(docs[0].page_content))
print("length of split 1:", len(all_splits[0].page_content))
print("metadata of splits:", all_splits[0].metadata, "\n", all_splits[1].metadata)

print("embedding function...")
# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
print("load... ")
# load it into Chroma 
db = Chroma.from_documents(all_splits, embedding_function, persist_directory="../vector_dbV2wChunking")


