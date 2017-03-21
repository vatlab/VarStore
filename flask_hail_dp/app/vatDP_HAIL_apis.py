# import vatlab_dp_utils
from __future__ import print_function
from random import randint
import time
from itertools import islice
import main as dprun
import sys
from hail import *
import json




def get_genotypes_by_variantIDs(ids):
    hail=dprun.get_hail()
    genotypes={}
    idString=""
    for id in ids:
        genotypes[id]={}
        idString=idString+'va.vID.hgvsID=="'+id+'" ||'
    idString=idString[:-3]
    print(idString,file=sys.stderr)
    result=hail.vds.query_genotypes('json(gs.filter(g=>'+idString+').map(g=>{s:s.id,gt:g.gt,hgvsID:va.vID.hgvsID}).collect())')
    result=json.loads(result)
    for genotype in result:
        sampleID=genotype["s"]
        variantID=genotype["hgvsID"]
        if genotype["gt"]==2:
            ref=1
            alt=1
        elif genotype["gt"]==1:
            ref=0
            alt=1
        elif genotype["gt"]==0:
            ref=0
            alt=0
        genotypes[variantID][sampleID]=str(ref)+"/"+str(alt)
    hail.stopHail()
    return genotypes


def get_genotype_by_samplename(sample):
    hail=dprun.get_hail()
    result=hail.vds.query_genotypes('json(gs.filter(g=>s.id=="'+sample+'").map(g=>{gt:g.gt,hgvsID:va.vID.hgvsID}).collect())')
    result=json.loads(result)
    genotypes={}
    # print(result,file=sys.stderr)
    ref=0
    alt=0
    for genotype in result:
        variantID=genotype["hgvsID"]
        if genotype["gt"]==2:
            ref=1
            alt=1
        elif genotype["gt"]==1:
            ref=0
            alt=1
        elif genotype["gt"]==0:
            ref=0
            alt=0
        genotypes[variantID]=str(ref)+"/"+str(alt)
    hail.stopHail()
    return genotypes

def get_all_variantsID():
    pass