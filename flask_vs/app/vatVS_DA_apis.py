# import vatlab_dp_utils
from random import randint
import time
from itertools import islice
import main as dprun
import sys
import main as vs_run


def get_variantIDs(ids):
    db=vs_run.get_db()
    query = {}
    query["query"] = {}
    query["query"]["bool"] = {}
    query["query"]["bool"]["must"]=[]
    query["query"]["bool"]["must"].append({"terms" : { "variantID" : ids }})
    query["size"]   = len(ids)
    result=db.runQuery(query)
    ids={}
    for variant in result["hits"]["hits"]:
        variantID=genotype["_source"]["varaintID"]
        rsID=genotype["_source"]["_id"]
        ids[variantID]=rsID
    return ids
