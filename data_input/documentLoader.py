from langchain_community.document_loaders import WebBaseLoader
import json
import requests
from bs4 import BeautifulSoup
import sys, os
import clean_data 
import re

with open("../data/URLS.json", 'r') as json_file:
    url_list = json.load(json_file)
    
texts = []
i = 1
for url in url_list:
    print(f"\n\n\n Article {i}")
    i += 1
    loader = WebBaseLoader(url)
    loader.requests_kwargs = {"verify":False}
    data = loader.load()
    text = data[0].page_content
    text = re.sub(r'\n', '', text)
    print(text)
    texts.append(text)

file_path = "../data/texts.json"
with open(file_path, 'w') as json_file:
    json.dump(texts, json_file)

# html_doc = requests.get(sample_url)
# soup = BeautifulSoup(html_doc.text, 'html.parser')
# print(soup)



