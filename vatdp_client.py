import requests

# Get genotypes by varaint ID
# res=requests.post("http://192.168.99.104/vatdp/variants/genotypes",json={"ids":["chr22:g.16211244G>T","chr22:g.16058883A>G"]})
# print(res.json())


## Get genotypes by sample Name
# res=requests.get("http://192.168.99.104/vatdp/samples/genotypes/HG00256")
# print(res.json())

## Get metadata by variantID
# res=requests.get("http://192.168.99.104/vatdp/variants/rs9628389")
# print(res.json())

# Get metadata by sample Name
#res=requests.get("http://192.168.99.104/vatdp/samples/HG01855")
#print(res.json())


# Get all varaints
res=requests.get("http://192.168.99.104/vatdp/variants")
resVariants=requests.post("http://192.168.99.103/vatvs/variants/variantsID",json={"ids":res.json()})
# resVariants=requests.post("http://192.168.99.103/vatvs/variants/variantsID",json={"ids":['chr22:g.16650580A>T', 'chr22:g.16650676A>C']})
print(resVariants.json())

# res=requests.post("http://192.168.99.104/vatdp/variants/search",json={"ids":["rs8136544","rs8135384"]})
# print(res.json())



