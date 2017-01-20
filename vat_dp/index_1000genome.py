import vatlab_dp_utils
from elasticsearch_utils import esDatabase
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

@timeit
def indexGenome(folder,files):
	vatlab_dp_utils.generateVCFinput(folder,files[0])

indexGenome(folder,files)