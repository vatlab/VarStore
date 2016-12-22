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
index    = 'gencode'
doc_type = 'gencode'
base_directory = '/Users/jma7/Development/variantTools'
filename="gencode.v19.annotation.gff3"
path_to_file = base_directory +"/" + filename 
start_time = time.time()
## read in a data file


with open(path_to_file) as f:
    GenCode=f.readlines()

action = []  ## iterable to be used by the bulk helper

fields=["Chromosome" 
        ,"Source"
        ,"Type"
        ,"Start"
        ,"End"
        ,"Score"
        ,"Strand"
        ,"Frame"
        ,"Group"]


Symbol=""
transcript_id=""
codingStart=""
codingEnd=""
for line in GenCode:
    if line.startswith("#"):
        continue
    line=line.rstrip()
    items=line.split("\t")
    if len(items) != len(fields):
        print ("wrong number of items.(got {}, expected {}").format(len(items),len(fields))
    type=""
    start=""
    end=""
    chr=""
    for ind,field in enumerate(fields):
        value=items[ind]
        if value == ".":
            continue
        if field == "Type":
            type=value
        if field=="Start":
            start=value
        if field=="End":
            end=value
        if field=="Chromosome":
            chr=value.replace("chr","")
        if field=="Group":
            cols=value.split(";")
            for col in cols:
                if col.startswith("gene_id="):
                    gene_id=col.replace("gene_id=","")
                if col.startswith("gene_name"):
                    Symbol=col.replace("gene_name=","")
            if type=="gene":
                source={}
                source["geneName"]=Symbol
                source["start"]=start
                source["end"]=end
                source["chr"]=chr
                doc_id=chr+start+end+Symbol
                action.append({"_index" : index, "_type" : doc_type, "_id" : doc_id, "_source" : json.dumps(source)})



## do a bulk index of what we have
bulk_index = elasticsearch.helpers.bulk(es,action,chunk_size=2000)
end_time = time.time()
print ("Elapsed time to load " , filename , ": " , str(end_time-start_time))