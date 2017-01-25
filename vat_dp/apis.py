import vatlab_dp_utils
from random import randint
import time
from itertools import islice



def get_variant_by_id(ids,db):
    query = {}
    query["query"] = {}
    query["query"]["bool"] = {}
    query["query"]["bool"]["must"]=[]
    query["query"]["bool"]["must"].append({"terms" : { "variantID" : [ids] }})
    query["size"]   = len(ids)
    result=db.runQuery(query)
    return result

def get_genotype_by_samplename(sample,db):
    query={}
    query["query"]={}
    query["query"]["nested"]={}
    query["query"]["nested"]["path"]="Genotype"
    query["query"]["nested"]["query"]={}
    query["query"]["nested"]["query"]["bool"]={}
    query["query"]["nested"]["query"]["bool"]["must"]=[]
    query["query"]["nested"]["query"]["bool"]["must"].append({"term":{"Genotype.sampleName":sample}})
    result=db.runQuery(query)
    return result

def get_all_variantsID(db):
    query={}
    query["aggs"]={}
    query["aggs"]["ids"]={}
    query["aggs"]["ids"]["terms"]={"field":"variantID","size":0}
    result=db.runQuery(query)
    ids=[]
    for id in result["aggregations"]["ids"]["buckets"]:
        ids.append(id["key"])
    return ids