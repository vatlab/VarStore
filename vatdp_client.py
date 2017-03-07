import requests
# res=requests.get("http://localhost:5000/vatdp/variants/rs9628389")
# print(res.json())

res=requests.post("http://192.168.99.104/vatdp/variants/search",json={"ids":["rs8136544","rs8135384"]})
print(res.json())

#res=requests.get("http://localhost:5000/vatdp/samples/HG01855")
#print(res.json())

