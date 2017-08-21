import datetime
import glob
import json
import os
import random
import re
import logging

from random import randint

import sys
import subprocess
import requests 

from flask import Flask,jsonify,request,g
import simplejson
from elasticsearch_database import esDatabase
import vatDP_DA_apis as apis



app = Flask(__name__)
# db=esDatabaseAlt()


def get_db():
    if not hasattr(g,"vatDPes"):
        g.vatDPes=esDatabase()
    return g.vatDPes


@app.route('/vatdp/variants/genotypes', methods=['POST'])
def get_genotypes_by_variantIDs():
    if not request.json:
        abort(400)
    ids=request.json.get('ids')
    result=apis.get_genotypes_by_variantIDs(ids)
    return jsonify(result)


@app.route('/vatdp/samples/genotypes/<string:sampleName>', methods=['GET'])
def get_genotypes_by_sampleName(sampleName):
    result=apis.get_genotype_by_samplename(sampleName)
    # print(result,files=sys.stderr)
    return jsonify(result)
    

@app.route('/vatdp/variants/<string:variantID>', methods=['GET'])
def get_meta_by_variantID(variantID):
    pass

@app.route('/vatdp/samples/<string:sampeName>', methods=['GET'])
def get_meta_by_sampleName(sampleName):
    pass



@app.route('/vatdp/variants', methods=['GET'])
def get_all_variantsID():
    result=apis.get_all_variantsID()
    # return simplejson.dumps(result)
    return jsonify(result)


@app.route('/vatdp/variants/search', methods=['POST'])
def search_variants():
    if not request.json:
        abort(400)
    ids=request.json.get('ids')
    result=apis.get_variant_by_id(ids)
    return jsonify(result)

@app.route("/")
def hello():
    return "Hello World from Flask"



if __name__ == '__main__':
    handler = logging.handlers.RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0',debug=True,port=80)
   








    



