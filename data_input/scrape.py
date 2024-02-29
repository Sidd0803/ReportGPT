import http.client
import json 
import re
import time

file_path = "../data/metadata.json"
conn = http.client.HTTPSConnection("google-news13.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "0ab28348ecmshfe711b1979a2d49p1d92f5jsnc174b75b7c64",
    'X-RapidAPI-Host': "google-news13.p.rapidapi.com"
}

conn.request("GET", "/search?keyword=Ukraine%20War%20articles%20after%3A2024-01-01", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
res_string = data.decode("utf-8")
print(res_string)

#store output in json
with open(file_path, 'w') as json_file:
    json.dump(res_string, json_file, indent=2) #store in json file
