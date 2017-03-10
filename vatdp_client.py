import requests
# res=requests.get("http://192.168.99.104/vatdp/variants/rs9628389")
# print(res.json())
# res=requests.get("http://192.168.99.104/")
# res=requests.get("http://192.168.99.104/vatdp/samples/genotypes/HG00256")
# print(res.json())
res=requests.post("http://192.168.99.104/vatdp/variants/genotypes",json={"ids":["chr22:g.16211244G>T","chr22:g.16058883A>G"]})
print(res.json())

# res=requests.post("http://192.168.99.104/vatdp/variants/search",json={"ids":["rs8136544","rs8135384"]})
# print(res.json())

#res=requests.get("http://localhost:5000/vatdp/samples/HG01855")
#print(res.json())

