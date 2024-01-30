import http.client

conn = http.client.HTTPSConnection("google-news-api1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "0ab28348ecmshfe711b1979a2d49p1d92f5jsnc174b75b7c64",
    'X-RapidAPI-Host': "google-news-api1.p.rapidapi.com"
}

query = "Delhi%20riots"

conn.request("GET", "/search?language=en&q=Elon%20Musk", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))