# os.chdir("/Users/jma7/Development/vat_data_provider/vat_dp/")
import vatlab_dp_utils
from random import randint
import time
from itertools import islice


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print ('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts))
        return result

    return timed

folder="/Users/jma7/Development/server/ga4gh-example-data/release/"
files=[]

files=vatlab_dp_utils.filesInFolder(folder)
# vatlab_dp_utils.getRowFromVCF(folder,files[0])
# vcfDict=vatlab_dp_utils.creatVCFdict(folder,files[0])


# keys=vcfDict.keys()
# for key in keys[:10]:
# 	print(vcfDict[key])


start=time.time()
vcfDict=vatlab_dp_utils.generateVCFinputAlt(folder,files[0])
end=time.time()
print(end-start)


# @timeit
# def checkCache():
#   count=0
#   while count<1000:
#       count=count+1
#       randID=ids[randint(0,len(ids))]
#       result=vcfDict[randID]

# checkCache()

# def iter_n(iterable, n):
#     it = iter(iterable)
#     while True:
#         chunk = tuple(islice(it, n))
#         if not chunk:
#             return
#         yield chunk


# @timeit
# def checkES():
#  	count=0
#  	selectedIDs=[]
#  	while count<1000:
#  		count=count+1
#  		randID=ids[randint(0,len(ids))]
#  		selectedIDs.append(randID)
#  	step=1000
#  	for batch in iter_n(selectedIDs,step):
#  		db.fetchByID(batch)

# checkES()

