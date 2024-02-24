import http.client
import json 
import re
import time
# from langchain_community.document_loaders import WebBaseLoader #some bug
# from langchain.document_loaders import WebBaseLoader

conn = http.client.HTTPSConnection("google-news-api1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "0ab28348ecmshfe711b1979a2d49p1d92f5jsnc174b75b7c64",
    'X-RapidAPI-Host': "google-news-api1.p.rapidapi.com"
}

file_path = "sample_dict.json"
query = ""

query = input("What subject are you reporting on?\n")
time.sleep(2)
#connect to API
# conn.request("GET", "/search?language=en&q=Elon%20Musk", headers=headers)
# res = conn.getresponse()
# data = res.read() #json object
# res_string = data.decode("utf-8")

#store output in json
# with open(file_path, 'w') as json_file:
#     json.dump(res_string, json_file, indent=2) #store in json file

#load data as a string
with open(file_path, 'r') as json_load:
    loaded_string = (json.load(json_load)) #string that was dumped into json

#convert to dictionary
res_dict = (json.loads(loaded_string))
#print(res_dict)

#extract a certain type of value from dictionary
def extract_values(dictionary, searchterm):
    result = []
    for key, value in dictionary.items():
        if key == searchterm:
            result.append(value)
        elif isinstance(value, dict):
            result.extend(extract_values(value, searchterm))
        elif isinstance(value, list):
            for i in value:
                result.extend(extract_values(i, searchterm))
    return result

#can retrieve url/body using rapid api
print("\nScraping from relevant information sources via Google News API...\n")
time.sleep(2)
links = extract_values(res_dict, "link")
print(len(links), " articles were retrieved!\n")
for link in links:
    print(link)
bodies = extract_values(res_dict, "body")
article = bodies[17]
time.sleep(3)

#try loading content separately using webLoader
# loader = WebBaseLoader(links[9])
# docs = loader.load()
# print(type(docs[0].page_content))
# page_contents = docs[0].page_content
trimmed_article = " ".join(article.split())
re.sub(' +', ' ', article).strip()
print("\n\nDisplaying sample article that was retrieved...:\n")
time.sleep(2)
print(trimmed_article, '\n\n')

#store final output in a text file (eventually transition to a proper data store)
file_path = "demoarticle.txt"
with open(file_path, "w") as file:
    file.write(trimmed_article)

