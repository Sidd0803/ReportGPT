import json 
import re
from langchain_community.document_loaders import WebBaseLoader

file_path = "../data/metadata.json"
#load data as a string
with open(file_path, 'r') as json_load:
    loaded_string = (json.load(json_load)) 

#convert to dictionary
res_dict = (json.loads(loaded_string))

docs = []
items = res_dict["items"]
count = 1
for item in items:
    md = {"source": item["publisher"], "time" : item["timestamp"]}
    url = item["newsUrl"]
    loader = WebBaseLoader(url)
    loader.requests_kwargs = {"verify":False}
    data = loader.load()
    text = data[0].page_content
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\t', '', text)
    doc = {"page_content" : text, "metadata" : md}
    docs.append(doc)
    print(count)
    count += 1


json_string = json.dumps(docs)
with open("../data/formatted_docs.json", "w") as json_file:
    json_file.write(json_string)
    

