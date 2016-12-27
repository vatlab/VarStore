#!/usr/local/bin/python3
from elasticsearch import Elasticsearch
from elasticsearch import client as client
import json
import logging
import logging.handlers
import sys
import subprocess

syscall = subprocess.run(["docker-machine","ip","default"],stdout=subprocess.PIPE)
dockermachine_hostname = syscall.stdout.decode("utf-8").strip()
elasticsearch_port = "9252"

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
mapping["vatdp"] = {}
mapping["vatdp"]["properties"] = {}
mapping["vatdp"]["properties"]["variantID"]  = { "type":"string", "index":"not_analyzed"}
mapping["vatdp"]["properties"]["chr"]   = { "type":"string" }
mapping["vatdp"]["properties"]["pos"]   = { "type":"integer"}
mapping["vatdp"]["properties"]["ref"]   = { "type":"string"}
mapping["vatdp"]["properties"]["alt"]   = { "type":"string"}
mapping["vatdp"]["properties"]["VT"] = { "type":"string" }
mapping["vatdp"]["properties"]["AF"] = { "type":"double" }
mapping["vatdp"]["properties"]["DP"] = { "type":"integer" }
# mapping["vatdp"]["properties"]["info"]["properties"]["EAS_AF"]={ "type":"double" }
# mapping["vatdp"]["properties"]["info"]["properties"]["AMR_AF"]={ "type":"double" }
# mapping["vatdp"]["properties"]["info"]["properties"]["AFR_AF"]={ "type":"double" }
# mapping["vatdp"]["properties"]["info"]["properties"]["EUR_AF"]={ "type":"double" }
# mapping["vatdp"]["properties"]["info"]["properties"]["SAS_AF"]={ "type":"double" }
mapping["vatdp"]["properties"]["samples"]={"type":"string"}


try:
	esclient.put_mapping(index=index,doc_type='vatdp',body=mapping["vatdp"])
except Exception as e:
	print ("Error in celllin document mapping")
	print (e)



## verify the mapping is as we expect
current_mapping = esclient.get_mapping(index=index)
