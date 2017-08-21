import pysam
import glob
import os
import json
import myvariant
import requests

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
    output_variants=open("/Users/jma7/Development/vat_data_provider/es_dp/input_file/test_data_variants_noindex.txt","w")
    output_genotypes=open("/Users/jma7/Development/vat_data_provider/es_dp/input_file/test_data_genotypes_noindex.txt","w")
    count=0
    index="vatdp"
    doc_type_variants="dp_v"
    doc_type_genotypes="dp_g"
    print("Start")
    for row in vcfin.fetch():
        count=count+1
        if count>10000:
             break
        ids=row.id.split(";")
        if len(ids)>1:
            for idx,id in enumerate(ids):
                # print (id,row.contig,row.pos,row.ref,row.alts[idx],row.info["AF"][idx])
                source={}
                # source["variantID"]=id
                source["chr"]=row.contig
                source["pos"]=row.pos
                source["ref"]=row.ref
                source["alt"]=row.alts[idx]
                hgvsID=myvariant.format_hgvs(source["chr"],source["pos"],source["ref"],source["alt"])
                # res=requests.post("http://192.168.99.103/vatvs/variants/variantsID",json={"ids":[hgvsID]})
                # print(res.json())
                doc_id  = hgvsID
                source["variantID"]=hgvsID
                # action={"_index" : index, "_type" : doc_type_variants, "_id" : doc_id, "_source" : source}
                action={"_source" : source}
                output_variants.write(json.dumps(action)+"\n")

                source={}
                source["variantID"]=hgvsID
                source["Genotype"]={}
                for sample in row.samples:
                    for key,value in row.samples[sample].iteritems():
                        if (value[0]==value[1]==0):
                            continue
                        elif (value[0]==value[1]==idx+1):
                            source["Genotype"]={"SN":sample,"r":value[0],"a":value[1]}
                        elif (value[0]==0 and value[1]==idx+1):
                            source["Genotype"]={"SN":sample,"r":value[0],"a":value[1]}
                        elif (value[0]==idx+1 and value[1]==0):
                            source["Genotype"]={"SN":sample,"r":value[0],"a":value[1]}
                        elif (value[0]==idx+1 and value[1]>0):
                            source["Genotype"]={"SN":sample,"r":value[0],"a":value[1]}
                        # action={"_index" : index, "_type" : doc_type_genotypes, "_source" : source}
                        action={"_source" : source}
                        output_genotypes.write(json.dumps(action)+"\n")

             
        else:
            # print (ids[0],row.contig,row.pos,row.ref,row.alts[0],row.info["AF"][0])
            source={}
            id=ids[0]
            
            source["chr"]=row.contig
            source["pos"]=row.pos
            source["ref"]=row.ref
            source["alt"]=row.alts[0]
            hgvsID=myvariant.format_hgvs(source["chr"],source["pos"],source["ref"],source["alt"])
            source["variantID"]=hgvsID
            doc_id  = hgvsID+"va"
            # action={"_index" : index, "_type" : doc_type_variants, "_id" : doc_id, "_source" : source}
            action={"_source" : source}
            output_variants.write(json.dumps(action)+"\n")

            source={}
            source["variantID"]=hgvsID
            source["Genotype"]={}
            for sample in row.samples:
                for key,value in row.samples[sample].iteritems():
                    if (value[0]==value[1]==0):
                        continue
                    else:
                        source["Genotype"]={"SN":sample,"r":value[0],"a":value[1]}
                    doc_id  = hgvsID+"_"+sample+"_"+key
                    # action={"_index" : index, "_type" : doc_type_genotypes, "_source" : source}
                    action={"_source" : source}
                    output_genotypes.write(json.dumps(action)+"\n")
            
    output_variants.close()
    output_genotypes.close()


def generateVCFinputRow(folder,file):
    vcfin=pysam.VariantFile(folder+file)
    info=list((vcfin.header.info))
    output_genotypes=open("/Users/jma7/Development/vat_data_provider/es_dp/input_file/test_data_genotypes_row.txt","w")
    count=0
    index="vatdp"
    print("Start")
    for row in vcfin.fetch():
        count=count+1
        if count>10000:
             break
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
                hgvsID=myvariant.format_hgvs(source["chr"],source["pos"],source["ref"],source["alt"])
                # res=requests.post("http://192.168.99.103/vatvs/variants/variantsID",json={"ids":[hgvsID]})
                # print(res.json())
                doc_id  = hgvsID
                # source["variantID"]=hgvsID
                # action={"_index" : index, "_type" : doc_type_variants, "_id" : doc_id, "_source" : source}
                # action={"_source" : source}
                # output_variants.write(json.dumps(action)+"\n")


                source={}
                source["variantID"]=hgvsID
                source["Genotype"]=[]
                for sample in row.samples:
                    for key,value in row.samples[sample].iteritems():
                        if (value[0]==value[1]==0):
                            pass      
                        elif (value[0]==value[1]==idx+1):
                            source["Genotype"].append({"SN":sample,"r":value[0],"a":value[1]})
                        elif (value[0]==0 and value[1]==idx+1):
                            source["Genotype"].append({"SN":sample,"r":value[0],"a":value[1]})
                        elif (value[0]==idx+1 and value[1]==0):
                            source["Genotype"].append({"SN":sample,"r":value[0],"a":value[1]})
                        elif (value[0]==idx+1 and value[1]>0):
                            source["Genotype"].append({"SN":sample,"r":value[0],"a":value[1]})
                
                action={ "_source" : source}
                output_genotypes.write(json.dumps(action)+"\n")
             
        else:
            # print (ids[0],row.contig,row.pos,row.ref,row.alts[0],row.info["AF"][0])
            source={}
            id=ids[0]
            
            source["chr"]=row.contig
            source["pos"]=row.pos
            source["ref"]=row.ref
            source["alt"]=row.alts[0]
            hgvsID=myvariant.format_hgvs(source["chr"],source["pos"],source["ref"],source["alt"])
            # source["variantID"]=hgvsID
            # doc_id  = hgvsID+"va"
            # action={"_index" : index, "_type" : doc_type_variants, "_id" : doc_id, "_source" : source}
            # action={"_source" : source}
            # output_variants.write(json.dumps(action)+"\n")

            
            source={}
            source["variantID"]=hgvsID
            source["Genotype"]=[]
            for sample in row.samples:
                for key,value in row.samples[sample].iteritems():
                    if (value[0]==value[1]==0):
                        pass
                    else:
                        source["Genotype"].append({"SN":sample,"r":value[0],"a":value[1]})
            # print(len(zzarray),len(ooarray),len(zoarray),len(ozarray))
            action={ "_source" : source}
            output_genotypes.write(json.dumps(action)+"\n")
    output_genotypes.close()


def generateVCFinputCol(folder,file):
    vcfin=pysam.VariantFile(folder+file)
    info=list((vcfin.header.info))
    output_genotypes=open("/Users/jma7/Development/vat_data_provider/es_dp/input_file/test_data_genotypes_col.txt","w")
    count=0
    index="vatdp_col"
    print("Start")
    sampleDict={}
    for row in vcfin.fetch():
        count=count+1
        if count>10000:
             break
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
                hgvsID=myvariant.format_hgvs(source["chr"],source["pos"],source["ref"],source["alt"])
                # res=requests.post("http://192.168.99.103/vatvs/variants/variantsID",json={"ids":[hgvsID]})
                # print(res.json())
               
                for sample in row.samples:
                    if sample not in sampleDict:
                        sampleDict[sample]=[]
                    for key,value in row.samples[sample].iteritems():
                        if (value[0]==value[1]==0):
                            pass      
                        elif (value[0]==value[1]==idx+1):
                            sampleDict[sample].append({"va":hgvsID,"r":value[0],"a":value[1]})
                            # source["Genotype"].append({"va":hgvsID,"r":value[0],"a":value[1]})
                        elif (value[0]==0 and value[1]==idx+1):
                            sampleDict[sample].append({"va":hgvsID,"r":value[0],"a":value[1]})
                            # source["Genotype"].append({"va":hgvsID,"r":value[0],"a":value[1]})
                        elif (value[0]==idx+1 and value[1]==0):
                            sampleDict[sample].append({"va":hgvsID,"r":value[0],"a":value[1]})
                            # source["Genotype"].append({"va":hgvsID,"r":value[0],"a":value[1]})
                        elif (value[0]==idx+1 and value[1]>0):
                            sampleDict[sample].append({"va":hgvsID,"r":value[0],"a":value[1]})
                            # source["Genotype"].append({"va":hgvsID,"r":value[0],"a":value[1]})            
        else:
            source={}
            id=ids[0]
            source["chr"]=row.contig
            source["pos"]=row.pos
            source["ref"]=row.ref
            source["alt"]=row.alts[0]
            hgvsID=myvariant.format_hgvs(source["chr"],source["pos"],source["ref"],source["alt"])

            for sample in row.samples:
                if sample not in sampleDict:
                        sampleDict[sample]=[]
                for key,value in row.samples[sample].iteritems():
                    if (value[0]==value[1]==0):
                        pass
                    else:
                        sampleDict[sample].append({"va":hgvsID,"r":value[0],"a":value[1]})
    for key,value in sampleDict.items():
        source={}
        source["sampleName"]=key
        source["Genotype"]=value
        action={ "_source" : source}
        output_genotypes.write(json.dumps(action)+"\n")
    output_genotypes.close()




