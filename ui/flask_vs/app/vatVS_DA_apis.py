# import vatlab_dp_utils
from random import randint
import time
from itertools import islice
import main as dprun
import sys
import main as vs_run
import myvariant



# def iter_n(iterable, n):
#     it = iter(iterable)
#     while True:
#         chunk = tuple(islice(it, n))
#         if not chunk:
#             return
#         yield chunk

# def get_variantIDs(ids):
# 	try:
# 	    db=vs_run.get_db()
# 	    numIDs=len(ids)-1
# 	    resultIDs={}
# 	    step=1000
# 	    for batch in iter_n(ids,step):
# 	        query = {}
# 	        query["query"] = {} 
# 	        query["query"]["terms"]={"variantID":batch}
# 	        query["size"]=step
# 	        result=db.runQuery(query)
# 	        print(result,file=sys.stderr)
# 	        for variant in result["hits"]["hits"]:
# 	            variantID=variant["_source"]["variantID"]
# 	            rsID=variant["_id"]
# 	            resultIDs[variantID]=rsID
# 	except:
# 	      e = sys.exc_info()[0]
# 	      print(e)
# 	return resultIDs

def formatID(x):
	return x[0]+"\t"+myvariant.format_hgvs(x[1],x[2],x[3],x[4])


def get_variantIDs(ids):
	try:
	    resultIDs=list(map(lambda x:formatID(x),ids))
	except:
	      e = sys.exc_info()[0]
	      print(e)
	return resultIDs