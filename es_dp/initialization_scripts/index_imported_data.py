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
import uuid

import logging
import logging.handlers


syscall = subprocess.run(["docker-machine","ip","vat-dp"],stdout=subprocess.PIPE)
elasticsearch_port = "9253"
dockermachine_hostname = syscall.stdout.decode("utf-8").strip()



es_logger = logging.getLogger('elasticsearch')
es_logger.setLevel(logging.ERROR)
es_logger_handler = logging.handlers.RotatingFileHandler("es.log")
es_logger.addHandler(es_logger_handler)

es_tracer = logging.getLogger('elasticsearch.trace')
es_tracer.setLevel(logging.ERROR)
es_tracer_handler = logging.handlers.RotatingFileHandler("es_tracer.log")
es_tracer.addHandler(es_tracer_handler)


## initialize connection to elasticsearch:
es       = Elasticsearch(host=dockermachine_hostname,port=elasticsearch_port,timeout=40,max_retries=10,retry_on_timeout=True)
esclient = client.IndicesClient(es)


filePath="/Users/jma7/Development/vat_data_provider/es_dp/input_file/test_data_variants.txt"
result = open(filePath,'r')

def bulkGenerator(result):
  for lineNum,item in enumerate(result):
      print(lineNum)
      yield json.loads(item)

start_time = time.time() 
bulk_index = elasticsearch.helpers.bulk(es,bulkGenerator(result),chunk_size=50000)
end_time = time.time()


# start_time = time.time() 
# for success,info in elasticsearch.helpers.parallel_bulk(es,bulkGenerator(pvalues,corrs,drugNamesP,drugNamesC),thread_count=4,chunk_size=50000):
#     if not success:
#       print("Fail")
# end_time = time.time()

print ("Time to load all files: " , str(end_time-start_time))





