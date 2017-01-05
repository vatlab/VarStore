#!/usr/local/bin/python3
from elasticsearch import Elasticsearch
from elasticsearch import client as client
import json
import logging
import logging.handlers
import sys
import subprocess
import requests 


class esDatabase:
	
	def __init__(self):
		syscall = subprocess.run(["docker-machine","ip","default"],stdout=subprocess.PIPE)
		self.dockermachine_hostname = syscall.stdout.decode("utf-8").strip()
		self.elasticsearch_port = "9252"
		self.index    = 'vatdp'
		self.doctype  = 'vatdp'

	def fetchByID(self,ids):
		query = {}
		query["query"] = {}
		query["query"]["bool"] = {}
		query["query"]["bool"]["must"]=[]
		query["query"]["bool"]["must"].append({"terms" : { "variantID" : [ids] }})
		query["size"]   = len(ids)
		result=self.runQuery(query)
		return result

	def fetchGenotypeBySample(self,sample):
		query={}
		query["query"]={}
		query["query"]["nested"]={}
		query["query"]["nested"]["path"]="Genotype"
		query["query"]["nested"]["query"]={}
		query["query"]["nested"]["query"]["bool"]={}
		query["query"]["nested"]["query"]["bool"]["must"]=[]
		query["query"]["nested"]["query"]["bool"]["must"].append({"term":{"Genotype.sampleName":sample}})
		result=self.runQuery(query)
		return result

	def fetchAllID(self):
		query={}
		query["aggs"]={}
		query["aggs"]["ids"]={}
		query["aggs"]["ids"]["terms"]={"field":"variantID","size":0}
		result=self.runQuery(query)
		ids=[]
		for id in result["aggregations"]["ids"]["buckets"]:
			ids.append(id["key"])
		return ids

	def runQuery(self,query):	
		url = "http://"+self.dockermachine_hostname+":"+self.elasticsearch_port+"//"+self.index+"/"+self.doctype+"/_search"
		response = requests.post(url,data=json.dumps(query))
		return json.loads(response.text)

