#!/usr/local/bin/python3
from elasticsearch import Elasticsearch
from elasticsearch import client as client
import json
import logging
import logging.handlers
import sys
import subprocess
import requests 
import time

syscall = subprocess.run(["docker-machine","ip","lms"],stdout=subprocess.PIPE)
dockermachine_hostname = syscall.stdout.decode("utf-8").strip()
elasticsearch_port = "9250"


indexGenCode    = 'gencode'
indexVatvs ="vatvs"

query = {}
query["query"] = {}
query["query"]["term"] = {"chr":"22"}
query["size"]   = 5000

#query["query"]["term"] = {"CompoundOfficialName.raw":"STAUROSPORINE"}
#query["query"]["term"] = {"CompoundOfficialName.raw":"ESTRADIOL"}
#query["query"]["match"] = {"Other Names":"8 Cl Ad"}
#query["query"]["match"] = {"GCC Name":"Compound C"}
#query["fields"] = ["GCC Name","Other Names", "CompoundOfficialName"]


url = "http://"+dockermachine_hostname+":"+elasticsearch_port+"//"+indexGenCode+"/_search"
r = requests.post(url,data=json.dumps(query))
#print (json.dumps(r.json(),indent=4))
hits_list = r.json()["hits"]["hits"]
genes= []
for item in hits_list:
	document = item["_source"]
	genes.append(document)


url = "http://"+dockermachine_hostname+":"+elasticsearch_port+"//"+indexVatvs+"/_search"

start_time=time.time()
count=0
for gene in genes:
	start=gene["start"]
	end=gene["end"]
	query = {}
	query["query"] = {}	
	query["query"]["bool"]={}
	query["query"]["bool"]["must"]=[]
	query["query"]["bool"]["must"].append({"term":{"chr":22}})
	query["query"]["bool"]["must"].append({"range":{"pos":{"gte":start,"lte":end,"boost":2}}})
	query["size"]=10000
	# print(json.dumps(query))
	r = requests.post(url,data=json.dumps(query))
	# print(json.dumps(r.json(),indent=4))
	hits_list = r.json()["hits"]["hits"]
	count=count+len(hits_list)
print("--- %s seconds ---" % (time.time() - start_time))
print(count)