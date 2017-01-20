import pysam
import glob
import os
import json


def filesInFolder(folder):
    return [os.path.basename(file) for file in glob.glob(folder+"*chr22*vcf.gz")]
    

def getHeader(folder,file):
    vcfin=pysam.VariantFile(folder+file)
    print (list((vcfin.header.contigs)))
    print (list((vcfin.header.alts)))
    print (list((vcfin.header.info)))
    print (list((vcfin.header.samples)))
    # for x in vcfin.header.records:
    #   print (x)
        

def getRowFromTabix(folder,file):
    tbx=pysam.TabixFile(folder+file)
    for row in tbx.fetch("19", 1900000, 2000000, parser=pysam.asVCF()):
        print (row.contig,row.pos,row.id,row.ref,row.alt,row.qual,len(row))

def getRowFromVCF(folder,file):
    vcfin=pysam.VariantFile(folder+file)
    info=list((vcfin.header.info))
    for row in vcfin.fetch():
        ids=row.id.split(";")
        ooarray=[]
        zoarray=[]
        ozarray=[]
        zzarray=[]
        mmarray=[]
        count=0
        if len(ids)>1:
            for idx,id in enumerate(ids):
                print (id,row.contig,row.pos,row.ref,row.alts[idx],row.info["AF"][idx])
                count=0
                ooarray=[]
                zoarray=[]
                ozarray=[]
                zzarray=[]
                mmarray=[]
                for sample in row.samples:
                    count=count+1
                    # print (sample,row.samples[sample].alleles)
                    for key,value in row.samples[sample].iteritems():
                        if (value[0]==value[1]==0):
                            zzarray.append(sample)      
                        elif (value[0]==value[1]==idx+1):
                            ooarray.append(sample)
                        elif (value[0]==0 and value[1]==idx+1):
                            zoarray.append(sample)
                        elif (value[0]==idx+1 and value[1]==0):
                            ozarray.append(sample)
                        elif (value[0]==idx+1 and value[1]>0):
                            mmarray.append(sample)
                print(len(zzarray),len(ooarray),len(zoarray),len(ozarray),len(mmarray))
        else:
            print (ids[0],row.contig,row.pos,row.ref,row.alts[0],row.info["AF"][0])
            for sample in row.samples:
                for key,value in row.samples[sample].iteritems():
                    print(key,value)
                    if (value[0]==value[1]==0):
                        zzarray.append(sample)      
                    elif (value[0]==value[1]==1):
                        ooarray.append(sample)
                    elif (value[0]==0):
                        zoarray.append(sample)
                    elif (value[0]==1):
                        ozarray.append(sample)
            print(len(zzarray),len(ooarray),len(zoarray),len(ozarray))
                    
            # for key in row.info:
            #     print(key,row.info[key])


def creatVCFdict(folder,file):
    vcfin=pysam.VariantFile(folder+file)
    info=list((vcfin.header.info))
    vcfDict={}
    count=0
    for row in vcfin.fetch():
        count=count+1
        print(count)
        if count>10000:
            break
        ids=row.id.split(";")
        if len(ids)>1:
            for idx,id in enumerate(ids):
                # print (id,row.contig,row.pos,row.ref,row.alts[idx],row.info["AF"][idx])
                vcfDict[id]={}
                vcfDict[id]["chr"]=row.contig
                vcfDict[id]["pos"]=row.pos
                vcfDict[id]["ref"]=row.ref
                vcfDict[id]["alt"]=row.alts[idx]
                vcfDict[id]["AF"]=row.info["AF"][idx]
                for sample in row.samples:
                    for key,value in row.samples[sample].iteritems():
                        if (value[0]==value[1]==0):
                            pass      
                        elif (value[0]==value[1]==idx+1):
                            vcfDict[id][sample]=value
                        elif (value[0]==0 and value[1]==idx+1):
                            vcfDict[id][sample]=value
                        elif (value[0]==idx+1 and value[1]==0):
                            vcfDict[id][sample]=value
                        elif (value[0]==idx+1 and value[1]>0):
                            vcfDict[id][sample]=value
                # print(len(zzarray),len(ooarray),len(zoarray),len(ozarray),len(mmarray))
        else:
            # print (ids[0],row.contig,row.pos,row.ref,row.alts[0],row.info["AF"][0])
            id=ids[0]
            vcfDict[id]={}
            vcfDict[id]["chr"]=row.contig
            vcfDict[id]["pos"]=row.pos
            vcfDict[id]["ref"]=row.ref
            vcfDict[id]["alt"]=row.alts[0]
            vcfDict[id]["AF"]=row.info["AF"][0]
            for sample in row.samples:
                for key,value in row.samples[sample].iteritems():
                    if (value[0]==value[1]==0):
                        pass
                    elif (value[0]==value[1]==1):
                        vcfDict[id][sample]=value
                    elif (value[0]==0):
                        vcfDict[id][sample]=value
                    elif (value[0]==1):
                        vcfDict[id][sample]=value
            # print(len(zzarray),len(ooarray),len(zoarray),len(ozarray))
    return vcfDict


def generateVCFinput(folder,file):
    vcfin=pysam.VariantFile(folder+file)
    info=list((vcfin.header.info))
    output=open("/Users/jma7/Development/vat_data_provider/elasticsearch/input_file/test_data.txt","w")
    count=0
    index="vatdp"
    doc_type="vatdp"
    for row in vcfin.fetch():
        # count=count+1
        # if count>10000:
        #     break
        ids=row.id.split(";")
        if len(ids)>1:
            for idx,id in enumerate(ids):
                # print (id,row.contig,row.pos,row.ref,row.alts[idx],row.info["AF"][idx])
                source={}
                source["variantID"]=id
                source["chr"]=row.contig
                source["pos"]=row.pos
                source["ref"]=row.ref
                source["alt"]=row.alts[idx]
                source["AF"]=row.info["AF"][idx]
                source["Genotype"]=[]
                for sample in row.samples:
                    for key,value in row.samples[sample].iteritems():
                        if (value[0]==value[1]==0):
                            pass      
                        elif (value[0]==value[1]==idx+1):
                            source["Genotype"].append({"sampleName":sample,"forward":value[0],"reverse":value[1]})
                        elif (value[0]==0 and value[1]==idx+1):
                            source["Genotype"].append({"sampleName":sample,"forward":value[0],"reverse":value[1]})
                        elif (value[0]==idx+1 and value[1]==0):
                            source["Genotype"].append({"sampleName":sample,"forward":value[0],"reverse":value[1]})
                        elif (value[0]==idx+1 and value[1]>0):
                            source["Genotype"].append({"sampleName":sample,"forward":value[0],"reverse":value[1]})
                doc_id  = id
                action={"_index" : index, "_type" : doc_type, "_id" : doc_id, "_source" : source}
                output.write(json.dumps(action)+"\n")
                # print(len(zzarray),len(ooarray),len(zoarray),len(ozarray),len(mmarray))
        else:
            # print (ids[0],row.contig,row.pos,row.ref,row.alts[0],row.info["AF"][0])
            source={}
            id=ids[0]
            source["variantID"]=id
            source["chr"]=row.contig
            source["pos"]=row.pos
            source["ref"]=row.ref
            source["alt"]=row.alts[0]
            source["AF"]=row.info["AF"][0]
            source["Genotype"]=[]
            for sample in row.samples:
                for key,value in row.samples[sample].iteritems():
                    if (value[0]==value[1]==0):
                        pass
                    else:
                        source["Genotype"].append({"sampleName":sample,"forward":value[0],"reverse":value[1]})
            # print(len(zzarray),len(ooarray),len(zoarray),len(ozarray))
            doc_id  = id
            action={"_index" : index, "_type" : doc_type, "_id" : doc_id, "_source" : source}
            output.write(json.dumps(action)+"\n")
    output.close()





