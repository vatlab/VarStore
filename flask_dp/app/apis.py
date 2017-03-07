# import vatlab_dp_utils
from random import randint
import time
from itertools import islice
import main as dprun



def get_variant_by_id(ids):
    db=dprun.get_db()
    query = {}
    query["query"] = {}
    query["query"]["bool"] = {}
    query["query"]["bool"]["must"]=[]
    query["query"]["bool"]["must"].append({"terms" : { "variantID" : [ids] }})
    query["size"]   = len(ids)
    result=db.runQuery_onVariants(query)
    return result

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
    result=db.runQuery_onGenotypes(query)
    return result

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