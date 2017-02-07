import datetime
import glob
import json
import os
import random
import re
import pysam
from random import randint

import sys
import subprocess
import requests 

from flask import Flask,jsonify,request
import simplejson
from elasticsearch_database import esDatabase,esDatabaseAlt
import apis



app = Flask(__name__)
db=esDatabaseAlt()



@app.route('/vatdp/variants', methods=['GET'])
def get_all_variantsID():
    result=apis.get_all_variantsID(db)
    # return simplejson.dumps(result)
    return jsonify(result)


@app.route('/vatdp/samples/<string:sampleName>', methods=['GET'])
def get_genotype_by_samplename(sampleName):
    result=apis.get_genotype_by_samplename(sampleName,db)
    return jsonify(result)


@app.route('/vatdp/variants/<string:variantID>', methods=['GET'])
def get_variant_by_id(variantID):
    result=apis.get_variant_by_id([variantID],db)
    return jsonify(result)


@app.route('/vatdp/variants/search', methods=['POST'])
def search_variants():
    if not request.json:
        abort(400)
    ids=request.json.get('ids')
    result=apis.get_variant_by_id(ids,db)
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)
   






class Variant:
    """
        variantID: ID of the variant
        chr(string): The chromosome on which variant is located.
        pos(int): The position of variant on the chromosome.
        ref(string): The reference base of the variant.
        alt(string): The alternate base of the varaint.
        genotypes(list<Genotype>): An array of genotypes 

    """
    def __init__(self,variantID,chr,pos,ref,alt,genotypes):
        self.variantID=variantID
        self.chr=chr
        self.pos=pos
        self.ref=ref
        self.alt=alt
        self.genotypes=genotypes

class Genotype:
    """
        sampleName(string): The name of the sample
        variantID(string): The ID of the variant
    """
    def __init__(self,sampleName,variantID):
        self.sampleName=sampleName
        self.variantID=varaintID

class Sample:
    """
        sampleName(string): The name of the sample
        datasetname(string): The name of the dataset that sample is in, (e.g 1000 genome)
        metaData(map<string,string>): The meta data of the sample
    """
    def __init__(self,sampleName,datasetName,metaData):
        self.sampleName=sampleName
        self.datasetName=datasetName
        self.metaData=metaData

class Dataset:
    """
        datasetName(string): The name of the dataset
        metaData(map<string,string>): The metadata of the dataset
        samples(list<string>): The samples in this dataset 

    """
    def __init__(self,datasetName,samples):
        self.datasetName=datasetName
        self.metaData=metaData
        self.samples=samples








    



