#!/usr/local/bin/python3
from elasticsearch import Elasticsearch
from elasticsearch import client as client
import elasticsearch
from elasticsearch import helpers
import json
import os
import sys
import time
import subprocess
from itertools import islice

import logging
import logging.handlers
from random import randint
import requests
from vat import *




syscall = subprocess.run(["docker-machine","ip","lms"],stdout=subprocess.PIPE)
dockermachine_hostname = syscall.stdout.decode("utf-8").strip()
elasticsearch_port = "9251"



## initialize connection to elasticsearch:
es       = Elasticsearch(host=dockermachine_hostname,port=elasticsearch_port,timeout=30,max_retries=10,retry_on_timeout=True)
esclient = client.IndicesClient(es)
index    = 'vatvs'
doc_type = 'vatvs'
base_directory = '../../../variantTools/vat-vs/'
filename="chr22.vcf"
start_time = time.time()
## read in a data file
path_to_file = base_directory +"/" + filename 
f = open(path_to_file,'r')
data = f.read().split("\n")
f.close()

## last line of the file might be a ''
if data[-1] == '':
  del(data[-1])
## make an iterable to use the elasticsearch bulk helper 
##   see: http://elasticsearch-py.readthedocs.org/en/master/helpers.html
action = []  ## iterable to be used by the bulk helper
for line in data:
    if line.startswith("#"):
        continue
    data_list = line.split('\t')
    source={}
    source["chr"]=data_list[0]
    source["pos"]=data_list[1]
    source["ref"]=data_list[3]
    source["alt"]=data_list[4]
    source["variantID"]=data_list[2]
    action.append(source)

url = "http://"+dockermachine_hostname+":"+elasticsearch_port+"/vatvs/_search"
refgenome = CrrFile('/Users/jma7/Development/variantTools/vat-vs/build37.crr')

import threading


class myThread (threading.Thread):
    def __init__(self, threadID, name, url,action):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.url = url
        self.action = action
    def run(self):
        print ("Starting " + self.name)
        # runTest(self.url,self.action)
        runBatchTest(self.url,self.action)
        print ("Exiting " + self.name)


def iter_n(iterable, n):
    it = iter(iterable)
    while True:
        chunk = tuple(islice(it, n))
        if not chunk:
            return
        yield chunk



def runTest(url,action):
    numIDs=len(action)-1
    for upperRange in [10000]:
        idPositions=[randint(0,numIDs) for p in range (0,upperRange)]
        start_time=time.time()
        for idPos in idPositions:
            chr=action[idPos]["chr"]
            pos=action[idPos]["pos"]
            ref=action[idPos]["ref"]
            alt=action[idPos]["alt"]
            variant = [chr, pos, ref, alt]
            # modify variant directly if needed
            # result=normalize_variant(refgenome, variant, 0, 1, 2, 3)
            # variant1=variant
            # if (result!=""):
            #     print(variant1)
            #     print(variant)
            #     print(result)
            query = {}
            query["query"] = {} 
            query["query"]["bool"]={}
            query["query"]["bool"]["must"]=[]
            query["query"]["bool"]["must"].append({"term":{"variantID":action[idPos]["variantID"]}})
            # query["query"]["bool"]["must"].append({"term":{"chr":chr}})
            # query["query"]["bool"]["must"].append({"term":{"pos":pos}})
            # query["query"]["bool"]["must"].append({"term":{"ref":action[idPos]["ref"]}})
            # query["query"]["bool"]["must"].append({"term":{"alt":action[idPos]["alt"]}})
            query["size"]=10000
        # print(json.dumps(query))
            r = requests.post(url,data=json.dumps(query))
            print(json.loads(r.text))
        print(upperRange)
        print("--- %s seconds ---" % (time.time() - start_time))



def runBatchTest(url,action):
    numIDs=len(action)-1
    for upperRange in [10000]:
        idPositions=[randint(0,numIDs) for p in range (0,upperRange)]
        step=1000
        variantIDList=[]
        for idPos in idPositions:
            variantIDList.append(action[idPos]["variantID"])
            # modify variant directly if needed
            # result=normalize_variant(refgenome, variant, 0, 1, 2, 3)
            # variant1=variant
            # if (result!=""):
            #     print(variant1)
            #     print(variant)
            #     print(result)
        start_time=time.time()
        for batch in iter_n(variantIDList,step):
            query = {}
            query["query"] = {} 
            query["query"]["terms"]={"variantID":batch}
            query["size"]=step
        # print(json.dumps(query))
            r = requests.post(url,data=json.dumps(query))
          #  print(json.loads(r.text))
        print(upperRange)
        print("--- %s seconds ---" % (time.time() - start_time))


# Create new threads
thread1 = myThread(1, "Thread-1", url,action)
thread2 = myThread(2, "Thread-2", url,action)
thread3 = myThread(3, "Thread-3", url,action)
thread4 = myThread(4, "Thread-4", url,action)

# Start new Threads
thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()








