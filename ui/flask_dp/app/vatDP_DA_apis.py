# import vatlab_dp_utils
from random import randint
import time
from itertools import islice
import main as dprun
import sys



def get_genotypes_by_variantIDs(ids):
    db=dprun.get_db()
    query={}
    query["query"]={}
    query["query"]["bool"]={}
    query["query"]["bool"]["must"]=[]
    query["query"]["bool"]["must"].append({"terms":{"variantID":ids}})
    query["size"]=10000
    result=db.runQuery_onGenotypes(query)
    genotypes={}
    for id in ids:
        genotypes[id]={}
    try:
        for genotype in result["hits"]["hits"]:
            sampleName=genotype["_source"]["Genotype"]["SN"]
            variantID=genotype["_source"]["variantID"]
            ref=genotype["_source"]["Genotype"]["r"]
            alt=genotype["_source"]["Genotype"]["a"]
            genotypes[variantID][sampleName]=str(ref)+"/"+str(alt)
    except:
          e = sys.exc_info()[0]
          print(e)
    return genotypes


def get_genotype_by_samplename(sample):
    db=dprun.get_db()
    query={}
    query["query"]={}
    query["query"]["nested"]={}
    query["query"]["nested"]["path"]="Genotype"
    query["query"]["nested"]["query"]={}
    query["query"]["nested"]["query"]["bool"]={}
    query["query"]["nested"]["query"]["bool"]["must"]=[]
    query["query"]["nested"]["query"]["bool"]["must"].append({"term":{"Genotype.SN":sample}})
    query["size"]=100000
    result=db.runQuery_onGenotypes(query)
    genotypes={}
    try:
        for genotype in result["hits"]["hits"]:
            variantID=genotype["_source"]["variantID"]
            ref=genotype["_source"]["Genotype"]["r"]
            alt=genotype["_source"]["Genotype"]["a"]
            genotypes[variantID]=str(ref)+"/"+str(alt)
    except:
          e = sys.exc_info()[0]
          print(e)
    return genotypes

def get_all_variantsID():
    db=dprun.get_db()
    query={}
    query["aggs"]={}
    query["aggs"]["ids"]={}
    query["aggs"]["ids"]["terms"]={"field":"variantID","size":0}
    result=db.runQuery_onVariants(query)
    ids=[]
    for id in result["aggregations"]["ids"]["buckets"]:
        ids.append(id["key"])
    return ids