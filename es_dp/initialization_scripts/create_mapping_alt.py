#!/usr/local/bin/python3
from elasticsearch import Elasticsearch
from elasticsearch import client as client
import json
import logging
import logging.handlers
import sys
import subprocess

syscall = subprocess.run(["docker-machine","ip","vat-dp"],stdout=subprocess.PIPE)
dockermachine_hostname = syscall.stdout.decode("utf-8").strip()
elasticsearch_port = "9253"

es_logger = logging.getLogger('elasticsearch')
es_logger.setLevel(logging.ERROR)
es_logger_handler = logging.handlers.RotatingFileHandler("es.log")
es_logger.addHandler(es_logger_handler)

es_tracer = logging.getLogger('elasticsearch.trace')
es_tracer.setLevel(logging.ERROR)
es_tracer_handler = logging.handlers.RotatingFileHandler("es_tracer.log")
es_tracer.addHandler(es_tracer_handler)

## initialize connection to elasticsearch:
es       = Elasticsearch(host=dockermachine_hostname,port=elasticsearch_port)
esclient = client.IndicesClient(es)
index    = 'vatdp'

## delete index and start over:
try:
	esclient.delete(index=index)
except:
	pass

## settings to create the index:
create_body = {}
create_body["settings"] = { "number_of_shards":5, "number_of_replicas":1 }

esclient.create(index=index,body=create_body)

## mapping for 'vatdp' (calling all the documents 'vatdp' for the moment)
mapping = {}
mapping["dp_v"] = {}
mapping["dp_v"]["properties"] = {}
mapping["dp_v"]["properties"]["variantID"]  = { "type":"string", "index":"not_analyzed"}
mapping["dp_v"]["properties"]["chr"]   = { "type":"string" }
mapping["dp_v"]["properties"]["pos"]   = { "type":"integer"}
mapping["dp_v"]["properties"]["ref"]   = { "type":"string"}
mapping["dp_v"]["properties"]["alt"]   = { "type":"string"}


try:
	esclient.put_mapping(index=index,doc_type='dp_v',body=mapping["dp_v"])
except Exception as e:
	print ("Error in celllin document mapping")
	print (e)

mapping = {}
mapping["dp_g"] = {}
mapping["dp_g"]["properties"] = {}
mapping["dp_g"]["properties"]["variantID"]  = { "type":"string", "index":"not_analyzed"}
mapping["dp_g"]["properties"]["Genotype"]   = {}
mapping["dp_g"]["properties"]["Genotype"]["type"] = "nested"
mapping["dp_g"]["properties"]["Genotype"]["properties"] = {}
mapping["dp_g"]["properties"]["Genotype"]["properties"]["SN"] = {"type":"string", "index": "not_analyzed"}
mapping["dp_g"]["properties"]["Genotype"]["properties"]["F"] = {"type":"integer"}
mapping["dp_g"]["properties"]["Genotype"]["properties"]["R"] = {"type":"integer"}



try:
	esclient.put_mapping(index=index,doc_type='dp_g',body=mapping["dp_g"])
except Exception as e:
	print ("Error in celllin document mapping")
	print (e)



## verify the mapping is as we expect
current_mapping = esclient.get_mapping(index=index)
