import requests
import time

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print ('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts))
        return result

    return timed

# Get genotypes by varaint ID
@timeit
def get_genotypes_by_variantIDs():
	res=requests.post("http://192.168.99.104/vatdp/variants/genotypes",json={"ids":["chr22:g.16211244G>T","chr22:g.16058883A>G"]})
	print(res.json())

get_genotypes_by_variantIDs()


## Get genotypes by sample Name
# @timeit
# def get_genotypes_by_sampleName():
# 	res=requests.get("http://192.168.99.104/vatdp/samples/genotypes/HG00096")
# 	print(res.json())

# get_genotypes_by_sampleName()

## Get metadata by variantID
# res=requests.get("http://192.168.99.104/vatdp/variants/rs9628389")
# print(res.json())

# Get metadata by sample Name
#res=requests.get("http://192.168.99.104/vatdp/samples/HG01855")
#print(res.json())


# Get all varaints
# res=requests.get("http://192.168.99.104/vatdp/variants")
# resVariants=requests.post("http://192.168.99.103/vatvs/variants/variantsID",json={"ids":res.json()})
# resVariants=requests.post("http://192.168.99.103/vatvs/variants/variantsID",json={"ids":['chr22:g.16650580A>T', 'chr22:g.16650676A>C']})
# resVariants=requests.post("http://192.168.99.103/vatvs/variants/variantsID",json={"ids":[["22","16650580","A","T"], ["22","16650676","A","C"]]})
# print(resVariants.json())

# res=requests.post("http://192.168.99.104/vatdp/variants/search",json={"ids":["rs8136544","rs8135384"]})
# print(res.json())





