#!/usr/local/bin/python3

import logging
import logging.handlers
import sys
import subprocess
import requests 
import json



class esDatabase:
    
    def __init__(self):
        # syscall = subprocess.run(["docker-machine","ip","vat-dp"],stdout=subprocess.PIPE)
        # self.dockermachine_hostname = syscall.stdout.decode("utf-8").strip()
        self.dockermachine_hostname = "192.168.99.104"
        self.elasticsearch_port = "9253"
        self.index    = 'vatdp'
        self.doctype  = 'vatdp'


    def runQuery(self,query):   
        url = "http://"+self.dockermachine_hostname+":"+self.elasticsearch_port+"//"+self.index+"/"+self.doctype+"/_search"
        response = requests.post(url,data=json.dumps(query))
        return json.loads(response.text)


class esDatabaseAlt:
    
    def __init__(self):
        # syscall = subprocess.run(["docker-machine","ip","vat-dp"],stdout=subprocess.PIPE)
        # self.dockermachine_hostname = syscall.stdout.decode("utf-8").strip()
        self.dockermachine_hostname = "192.168.99.104"
        self.elasticsearch_port = "9253"
        self.index    = 'vatdpalt'
        self.doctype_variants  = 'vatdp_variants'
        self.doctype_genotypes = 'vatdp_genotypes'


    def runQuery_onVariants(self,query):   
        url = "http://"+self.dockermachine_hostname+":"+self.elasticsearch_port+"//"+self.index+"/"+self.doctype_variants+"/_search"
        response = requests.post(url,data=json.dumps(query))
        return json.loads(response.text)

    def runQuery_onGenotypes(self,query):   
        url = "http://"+self.dockermachine_hostname+":"+self.elasticsearch_port+"//"+self.index+"/"+self.doctype_genotypes+"/_search"
        response = requests.post(url,data=json.dumps(query))
        return json.loads(response.text)
