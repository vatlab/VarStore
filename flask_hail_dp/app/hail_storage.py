from hail import *


class hailStorage:
	def __init__(self):
		folderPath='/usr/work/chr22.vds'
		self.hc=HailContext()
		self.vds=self.hc.read(folderPath)

	def stopHail(self):
		self.hc.stop()
