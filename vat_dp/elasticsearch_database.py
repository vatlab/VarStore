#!/usr/local/bin/python3

import logging
import logging.handlers
import sys
import subprocess
import requests 
import json



class esDatabase:
    
    def __init__(self):
        syscall = subprocess.run(["docker-machine","ip","default"],stdout=subprocess.PIPE)
        self.dockermachine_hostname = syscall.stdout.decode("utf-8").strip()
        self.elasticsearch_port = "9252"
        self.index    = 'vatdp'
        self.doctype  = 'vatdp'


    def runQuery(self,query):   
        url = "http://"+self.dockermachine_hostname+":"+self.elasticsearch_port+"//"+self.index+"/"+self.doctype+"/_search"
        response = requests.post(url,data=json.dumps(query))
        return json.loads(response.text)

