#!/usr/local/bin/python3
import pickle
GenCodePath="/Users/jma7/Development/variantTools/gencode.v19.annotation.gff3"

with open(GenCodePath) as f:
    GenCode=f.readlines()
    
genCodeDict={}
fields=["Chromosome" 
        ,"Source"
        ,"Type"
        ,"Start"
        ,"End"
        ,"Score"
        ,"Strand"
        ,"Frame"
        ,"Group"]

mainhash={}
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
    for index,field in enumerate(fields):
        value=items[index]
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
                codingStart=start
                codingEnd=end
                genCodeDict[Symbol]={}
                genCodeDict[Symbol]["CodingStart"]=codingStart
                genCodeDict[Symbol]["CodingEnd"]=codingEnd
                genCodeDict[Symbol]["Chromosome"]=chr


with open("/Users/jma7/Development/variantTools/genCode19.pickle","wb") as handle:
    pickle.dump(genCodeDict,handle)
