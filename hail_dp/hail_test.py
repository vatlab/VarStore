
# coding: utf-8

# In[1]:

from hail import *


# In[14]:

import requests


# In[2]:

hc = HailContext()


# In[3]:

vds = hc.read('/Users/jma7/Development/hail/test/firstchr22.vds')


# In[4]:

vds.count()


# In[50]:

vds.export_variants("/Users/jma7/Development/hail/test/variantcheck.tsv",'v,v.contig,v.start,v.ref,v.alt')


# In[51]:

originalIDs=[]
with open("/Users/jma7/Development/hail/test/variantChr22.tsv","r") as infile:
    for line in infile:
        cols=line.rstrip().split("\t")
        originalIDs.append([cols[0],cols[1],cols[2],cols[3],cols[4]])


# In[52]:
def iter_n(iterable, n):
    it = iter(iterable)
    while True:
        chunk = tuple(islice(it, n))
        if not chunk:
            return
        yield chunk

step=10000
with open("/Users/jma7/Development/hail/test/hgvsIDs_iter.tsv","w") as outfile:
    outfile.write("VariantID\thgvsID\n")
	for batch in iter_n(originalIDs,step):
		resVariants=requests.post("http://192.168.99.105/vatvs/variants/variantsID",json={"ids":batch})
		for id in resVariants.json():
        	outfile.write(id+"\n")    




resVariants=requests.post("http://192.168.99.103/vatvs/variants/variantsID",json={"ids":originalIDs})


# In[53]:

with open("/Users/jma7/Development/hail/test/hgvsIDs.tsv","w") as outfile:
    outfile.write("VariantID\thgvsID\n")
    for id in resVariants.json():
        outfile.write(id+"\n")


# In[85]:

vdsanno=vds.annotate_variants_table("/Users/jma7/Development/hail/test/hgvsIDs.tsv",root="va.vID",variant_expr="VariantID",config=TextTableConfig(impute=True))


# In[97]:

queryByID=vdsanno.filter_variants_expr('va.vID.hgvsID=="chr22:g.16050115G>A"')


# In[73]:

queryBySample=vdsanno.filter_samples_expr('s.id=="HG00096"')


# In[98]:

queryByID.export_genotypes("/Users/jma7/Development/hail/test/queryByID.tsv",'s,v')


# In[93]:

queryBySample.export_genotypes("/Users/jma7/Development/hail/test/queryBySample.tsv",'s,v')


# In[ ]:
vdsanno.query_genotypes('json(gs.filter(g=>va.vID.hgvsID=="chr22:g.16211244G>T").map(g=>{s:s.id,gt:g.gt,hgvsID:va.vID.hgvsID}).take(5))')

vds.filter_samples_expr('s=="HG00096"').query_genotypes('json(gs.map(g=>{gt:g.gt,hgvsID:va.vID.hgvsID}).take(5))')
vds.filter_variants_expr('va.vID.hgvsID=="chr22:g.16211244G>T"').query_genotypes('json(gs.map(g=>{s:s.id,gt:g.gt}).take(5))')
