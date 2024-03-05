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

loader = WebBaseLoader([urls[0], urls[1], urls[2]])
docs = loader.load()
print(docs[0].page_content)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)
print(all_splits[25].page_content , "/n/n/n/n")
for snippet in all_splits:
    text = snippet.page_content
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\t', '', text)
    snippet.page_content = text
#print(all_splits[25].page_content)
new_docs = [{'page_content':snippet.page_content,'source':snippet.metadata['source'],'title':snippet.metadata['title'],'description':snippet.metadata['description']} for snippet in all_splits]
#print([new_doc['page_content'] for new_doc in new_docs])
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


