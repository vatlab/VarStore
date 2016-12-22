import myvariant
import requests
import json
from random import randint
import time
import threading

mv = myvariant.MyVariantInfo()
# res=mv.getvariant("chr7:g.140453134T>C", fields='cosmic,snpeff')
# res = mv.getvariant('chr6:g.26093141G>A', fields = ['clinvar.rcv.accession', 'exac.af', 'dbnsfp.sift.converted_rankscore'])
# print res

# requestedURL="http://myvariant.info/v1/query?q=_exists_%3Adbsnp%20AND%20dbsnp.vartype%3Aindel&fields=dbsnp.alt&fetch_all=TRUE"
# # requestedURL="http://myvariant.info/v1/variant/chr1:g.35367G>A?fields=cadd"
# res=requests.get(requestedURL)
# response = json.loads(res.text)
# sizeList=[len(elem["dbsnp"]["alt"]) for elem in response["hits"]]
# maxList=[]
# scroll_id=response["_scroll_id"]
# # print(sizeList)
# maxList.append(max(sizeList))
# count=0
# while (scroll_id!=""):

# 	requestedURL="http://myvariant.info/v1/query?scroll_id="+scroll_id
# 	res=requests.get(requestedURL)
# 	response = json.loads(res.text)
# 	sizeList=[len(elem["dbsnp"]["alt"]) for elem in response["hits"]]
# 	scroll_id=response["_scroll_id"]
# 	print(max(sizeList))
# 	maxList.append((max(sizeList)))
# 	count=count+1000
# print(max(maxList))


# requestedURL="http://myvariant.info/v1/query?q=_exists_%3Adbsnp%20AND%20dbsnp.vartype%3Aindel&fields=_id&fetch_all=TRUE"
# # requestedURL="http://myvariant.info/v1/variant/chr1:g.35367G>A?fields=cadd"
# res=requests.get(requestedURL)
# response = json.loads(res.text)
# #sizeList=[elem["_id"] for elem in response["hits"]]
# sizeList=[len(elem["_id"]) for elem in response["hits"] if "ins" in elem["_id"]]
# maxList=[]
# scroll_id=response["_scroll_id"]
# # print(sizeList)
# maxList.append(max(sizeList))
# count=0
# while (scroll_id!=""):
# 	requestedURL="http://myvariant.info/v1/query?scroll_id="+scroll_id
# 	res=requests.get(requestedURL)
# 	response = json.loads(res.text)
# 	sizeList=[elem["_id"] for elem in response["hits"] if "ins" in elem["_id"]]
# 	scroll_id=response["_scroll_id"]
# 	print(max(sizeList,key=len))
# 	# maxList.append((max(sizeList)))
# 	count=count+1000
# print(max(maxList))


requestedURL="http://myvariant.info/v1/query?q=chr1:1-1000000000&fields=_id&fetch_all=TRUE"
# requestedURL="http://myvariant.info/v1/variant/chr1:g.35367G>A?fields=cadd"
res=requests.get(requestedURL)
response = json.loads(res.text)
#sizeList=[elem["_id"] for elem in response["hits"]]
sizeList=[len(elem["_id"]) for elem in response["hits"] if "dup" in elem["_id"]]
print(sizeList)
scroll_id=response["_scroll_id"]
# print(sizeList)
count=0
while (scroll_id!=""):
	requestedURL="http://myvariant.info/v1/query?scroll_id="+scroll_id
	res=requests.get(requestedURL)
	response = json.loads(res.text)
	sizeList=[elem["_id"] for elem in response["hits"] if "dup" in elem["_id"]]
	scroll_id=response["_scroll_id"]
	print(sizeList)
	# maxList.append((max(sizeList)))
	count=count+1000
print(max(maxList))



