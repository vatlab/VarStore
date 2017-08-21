
from hail import *

import requests


hc = HailContext()

folderPath='/Users/jma7/Development/hail/test/firstchr22.vds'

vds = hc.read(folderPath)
vds.cache()

print(vds.count())