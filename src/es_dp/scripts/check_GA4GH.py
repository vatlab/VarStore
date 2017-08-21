
import requests
import json
from random import randint
import time
import threading
import traceback


import ga4gh.client as client
BASE_URL = "http://127.0.0.1:8000/"

DATASETS_SEARCH_URL = BASE_URL + "datasets/search"

headers = {'Content-type': 'application/json'}

c = client.HttpClient(BASE_URL)




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

response = c.search_datasets()

print(response)
datasets = []

for dataset in response:
    datasets.append(dataset)
    print(dataset)

variant_sets = []

for dataset in datasets:
    datasetId = dataset.id
    response = c.search_variant_sets(datasetId)
    for variant_set in response:
        variant_sets.append(variant_set)


variant_set = variant_sets[0]
variantSetId = variant_set.id
print variantSetId

counter = 0
for variant in c.search_variants(variant_set_id=variantSetId, reference_name="1", start=10176, end= 40176):
    if counter > 1:
        break
    counter += 1
    print "Variant id: {}...".format(variant.id)
    print "Variant Set Id: {}".format(variant.variant_set_id)
    print "Names: {}".format(variant.names)
    print "Reference Chromosome: {}".format(variant.reference_name)
    print "Start: {}, End: {}".format(variant.start, variant.end)
    print "Reference Bases: {}".format(variant.reference_bases)
    print "Alternate Bases: {}\n".format(variant.alternate_bases)
    single_variant = c.get_variant(variant_id=variant.id)



# class myThread (threading.Thread):
#     def __init__(self, threadID, name, action):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.action = action
#     def run(self):
#         print ("Starting " + self.name)
#         runTest(self.action)
#         print ("Exiting " + self.name)


# def listGenerator():
# 	numIDs=len(action)-1
# 	for upperRange in [10000]:
# 		idPositions=[randint(0,numIDs) for p in range (0,upperRange)]
# 		for idPos in idPositions:
# 			chr=action[idPos]["chr"]
# 			pos=action[idPos]["pos"]
# 			# print chr+" "+pos
# 			# ref=action[idPos]["ref"]
# 			# alt=action[idPos]["alt"]
# 			# vid=action[idPos]["variantID"]
# 			# response=c.get_variant(variant_id=vid)
# 			response=c.search_variants(variant_set_id=variantSetId, reference_name=chr, start=int(pos), end=int(pos)+1)
# 			counter=0
# 			for variant in response:
# 				counter=counter+1
# 			# print counter
# 				 # print "Names: {}".format(variant.names)

# 			yield response
# 			# yield myvariant.format_hgvs(chr,pos,ref,alt)

# def runTest(action):
# 	results=[]
# 	start_time=time.time()
# 	# response=mv.getvariants(listGenerator(), fields="dbsnp")
# 	# response=c.get_variant(variant_id=listGenerator())
# 	for response in listGenerator():
# 		results.append(response)
# 	# print(results)
# 	print("--- %s seconds ---" % (time.time() - start_time))

# # Create new threads
# thread1 = myThread(1, "Thread-1", action)
# thread2 = myThread(2, "Thread-2", action)
# thread3 = myThread(3, "Thread-3", action)
# thread4 = myThread(4, "Thread-4", action)

# # Start new Threads
# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()


