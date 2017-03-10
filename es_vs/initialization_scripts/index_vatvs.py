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

import logging
import logging.handlers
import myvariant

#if len(sys.argv) != 3:
#	print "USAGE: "
#	print
#	print "./index_cellline_documents.py <host IP> <ES port>"
#	print "\nWhere: "
#	print "   <host IP>    : docker machine IP"
#	print "   <ES port>    : elasticsearch port exposed in docker-compose-up "
#	print "\nExample:"
#	print "   ./index_cellline_documents.py 192.168.99.100 9221"
#	sys.exit(0)

syscall = subprocess.run(["docker-machine","ip","default"],stdout=subprocess.PIPE)
dockermachine_hostname = syscall.stdout.decode("utf-8").strip()
elasticsearch_port = "9251"


es_logger = logging.getLogger('elasticsearch')
es_logger.setLevel(logging.ERROR)
es_logger_handler = logging.handlers.RotatingFileHandler("es.log")
es_logger.addHandler(es_logger_handler)

es_tracer = logging.getLogger('elasticsearch.trace')
es_tracer.setLevel(logging.ERROR)
es_tracer_handler = logging.handlers.RotatingFileHandler("es_tracer.log")
es_tracer.addHandler(es_tracer_handler)


## initialize connection to elasticsearch:
es       = Elasticsearch(host=dockermachine_hostname,port=elasticsearch_port,timeout=30,max_retries=10,retry_on_timeout=True)
esclient = client.IndicesClient(es)
index    = 'vatvs'
doc_type = 'vatvs'
base_directory = '/Users/jma7/Development/variantTools/vat-vs/'
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
    hgvsID=myvariant.format_hgvs(source["chr"],source["pos"],source["ref"],source["alt"])
    source["variantID"]=hgvsID
    doc_id=data_list[2]
    action.append({"_index" : index, "_type" : doc_type, "_id" : doc_id, "_source" : json.dumps(source)})

## do a bulk index of what we have
bulk_index = elasticsearch.helpers.bulk(es,action,chunk_size=20000)
end_time = time.time()
print ("Elapsed time to load " , filename , ": " , str(end_time-start_time))


