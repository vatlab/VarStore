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

# requestedURL="http://myvariant.info/v1/query?q=dbnsfp.polyphen2.hdiv.score:>0.99 AND chrom:1"
# requestedURL="http://myvariant.info/v1/variant/chr1:g.35367G>A?fields=cadd"
# res=requests.get(requestedURL)
# response = json.loads(res.text)
# print response


base_directory = '../../../variantTools/vat-vs/'
filename="chr22.vcf"

## read in a data file
path_to_file = base_directory +"/" + filename 
f = open(path_to_file,'r')
data = f.read().split("\n")
f.close()

## last line of the file might be a ''
if data[-1] == '':
	del(data[-1])

action = []  ## iterable to be used by the bulk helper

for line in data:
	if line.startswith("#"):
		continue
	data_list = line.split('\t')
	source={}
	source["chr"]=data_list[0]
	source["pos"]=data_list[1]
	source["ref"]=data_list[3]
	alt=data_list[4]
	for altone in alt.split(","):
		source["alt"]=altone
		source["variantID"]=data_list[2]
		action.append(source)


class myThread (threading.Thread):
    def __init__(self, threadID, name, action):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.action = action
    def run(self):
        print ("Starting " + self.name)
        runTest(self.action)
        print ("Exiting " + self.name)


def listGenerator():
	numIDs=len(action)-1
	for upperRange in [10000]:
		idPositions=[randint(0,numIDs) for p in range (0,upperRange)]
		for idPos in idPositions:
			chr=action[idPos]["chr"]
			pos=action[idPos]["pos"]
			ref=action[idPos]["ref"]
			alt=action[idPos]["alt"]
			yield myvariant.format_hgvs(chr,pos,ref,alt)

def runTest(action):
	results=[]
	start_time=time.time()
	response=mv.getvariants(listGenerator(), fields="dbsnp")
	results.append(response)
	# print(results)
	print("--- %s seconds ---" % (time.time() - start_time))

# Create new threads
thread1 = myThread(1, "Thread-1", action)
thread2 = myThread(2, "Thread-2", action)
thread3 = myThread(3, "Thread-3", action)
thread4 = myThread(4, "Thread-4", action)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()


# vars = ['chr1:g.866422C>T',
# 	'chr1:g.876664G>A',
# 	'chr1:g.69635G>C',
# 	'chr1:g.69869T>A',
# 	'chr1:g.881918G>A',
# 	'chr1:g.865625G>A']

# def listGenerator():
# 	for variant in vars:
# 		yield variant

# # response=mv.getvariants(listGenerator(), fields="cadd.phred")
# # print response


# response=myvariant.format_hgvs("1", 35366, "C", "T")
# print response