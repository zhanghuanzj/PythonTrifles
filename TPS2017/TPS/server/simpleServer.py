# -*- coding: GBK -*-

import sys
sys.path.append('./common')

from network.simpleHost import SimpleHost
from dispatcher import Dispatcher

class SimpleServer(object):
	
	def __init__(self):
		super(SimpleServer, self).__init__()

		self.entities = {}
		self.host = SimpleHost()
		self.dispatcher = Dispatcher()

		return

	def generateEntityID(self):
		raise NotImplementedError

	def registerEntity(self, entity):
		eid = self.generateEntityID
		entity.id = eid

		self.entities[eid] = entity

		return

	def tick(self):
		self.host.process()

		for eid, entity in self.entities.iteritems():
			# Note: you can not delete entity in tick.
			# you may cache delete items and delete in next frame
			# or just use items.
			entity.tick()

		return



