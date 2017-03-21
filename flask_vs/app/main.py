import datetime
import glob
import json
import os
import random
import re
from random import randint

import sys
import subprocess
import requests 

from flask import Flask,jsonify,request,g
import simplejson
from elasticsearch_database import esDatabase
import vatVS_DA_apis as apis




app = Flask(__name__)
# db=esDatabaseAlt()

def get_db():
    if not hasattr(g,"vatVSes"):
        g.vatVSes=esDatabase()
    return g.vatVSes

@app.route('/vatvs/variants/list_fields',methods=['GET'])
def list_fields():
    pass


@app.route('/vatvs/variants/variantsID', methods=['POST'])
def get_variantIDs():
    if not request.json:
        abort(400)
    ids=request.json.get('ids')
    result=apis.get_variantIDs(ids)
    # print(result,file=sys.stderr)
    return jsonify(result)


# @app.route('/vatvs/variants/<string:chromosome>', methods=['GET'])
# def get_variants_by_chromosome_range(chr,range):
#     pass


# @app.route('/vatvs/variants/<string:field>', methods=['GET'])
# def get_variants_by_field_range(field,range):
#     pass


@app.route('/vatvs/variants/gene/<string:geneName>', methods=['GET'])
def get_variants_in_gene(geneName):
    pass


@app.route('/vatvs/variants/search', methods=['POST'])
def search_variants():
    pass


@app.route('/vatvs/annotation/gene/<string:geneName>', methods=['GET'])
def get_annotations_by_gene(geneName):
    pass


@app.route('/vatvs/annotation/variant/<string:variantID>', methods=['GET'])
def get_annotations_by_variantID(variantID):
    pass


@app.route('/vatvs/annotation/variant', methods=['POST'])
def get_annotations_by_variantIDs(variantIDs):
    pass


@app.route("/")
def hello():
    return "Hello World from Flask"



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=80)