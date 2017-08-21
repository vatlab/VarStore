from __future__ import print_function
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
import vatDP_HAIL_apis as apis
from hail_storage import hailStorage



app = Flask(__name__)
# db=esDatabaseAlt()


# def get_hail():
#      vatDPhail=hailStorage()
#      return vatDPhail

def get_hail():
    if not hasattr(g,"vatDPhail"):
        g.vatDPhail=hailStorage()
    return g.vatDPhail


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
    print(result,file=sys.stderr)
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
    return "Hello World from Flask!!"



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=80)
   








    



