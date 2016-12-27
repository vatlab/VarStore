import pysam
import glob
import os

folder="/Users/jma7/Development/server/ga4gh-example-data/release/"
files=[]


def filesInFolder(folder):
    return [os.path.basename(file) for file in glob.glob(folder+"*22*vcf.gz")]
    

def getHeader(file):
    vcfin=pysam.VariantFile(folder+file)
    print (list((vcfin.header.contigs)))
    print (list((vcfin.header.alts)))
    print (list((vcfin.header.info)))
    print (list((vcfin.header.samples)))
    # for x in vcfin.header.records:
    #   print (x)
        

def getRowFromTabix(file):
    tbx=pysam.TabixFile(folder+file)
    for row in tbx.fetch("19", 1900000, 2000000, parser=pysam.asVCF()):
        print (row.contig,row.pos,row.id,row.ref,row.alt,row.qual,len(row))

def getRowFromVCF(file):
    vcfin=pysam.VariantFile(folder+file)
    info=list((vcfin.header.info))
    for row in vcfin.fetch():
        ids=row.id.split(";")
        if len(ids)>1:
            for idx,id in enumerate(ids):
                print (id,row.contig,row.pos,row.ref,row.alts[idx],row.info["AF"][idx])
                for sample in row.samples:
                    print (sample,row.samples[sample].alleles)
                    for key,value in row.samples[sample].iteritems():
                        print(key,value)
            # for key in row.info:
            #     print(key,row.info[key])
        # if len(row.ref)>5:
        #     for sample in row.samples:
        #          print (sample,row.samples[sample].alleles)
        #          for key,value in row.samples[sample].iteritems():
        #              print(key,value)



files=filesInFolder(folder)
# getHeader(files[0])
getRowFromVCF(files[0])





# vcfin=pysam.VariantFile(folder+"ALL.chr19.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz")
# print(vcfin.header)

