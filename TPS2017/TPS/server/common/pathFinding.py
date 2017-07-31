# -*- coding: GBK -*-
import heapq
import math
import time
import sys
FLAG = 0
XINDEX = 1
ZINDEX = 3
PRECISION = 1e-6
CLOSEDISTANCE = 0.2
A = 1
B = 2
C = 3
class Vertex(object):
	def __init__(self, index, cost):
		super(Vertex, self).__init__()
		self.index = index
		self.cost = cost
		self.father = None

	def __le__(self, other): 
		return self.cost <= other.cost

	def __hash__(self):  
		return hash(str(self.index) ) 
  
	def __eq__(self, other):  
		if self.index == other.index :  
			return True  
		return False  

class PathFinding(object):
	def __init__(self):
		super(PathFinding, self).__init__()
		self.gameMap = {}
		self.triangle = {}
		self.vertex = {}
		self.vertexIndex = {}
		self.dest = 1 	#[-5.333332, -23.66667]
		self.vcost = {}
		self.next = {}
		#self.stat = 34	#[5.0, 24.0]

	def generateIndex(self, x, y, index):
		for k,v in self.vertex.items():
			if math.fabs(v[0]-x) < PRECISION and math.fabs(v[1]-y) < PRECISION:#already exist vertex
				return k
		return index

	def getIndex(self, index):
		while index != self.vertexIndex[index]:
			index = self.vertexIndex[index]
		return index

	def readMap(self, filePath):#read map data
		mapFile = open(filePath)
		try:
			mapLines = mapFile.readlines()
			index = 1
			tindex = 1
			for line in mapLines:
				values = line.split()
				if values[FLAG] == 'v':
					trueIndex = self.generateIndex(float(values[XINDEX]), float(values[ZINDEX]), index)
					if trueIndex == index:
						self.vertex[index] = [float(values[XINDEX]),float(values[ZINDEX])]
					self.vertexIndex[index] = trueIndex
					index = index + 1
				elif values[FLAG] == 'f':
					indexs = [self.getIndex(int(values[A])), self.getIndex(int(values[B])), self.getIndex(int(values[C]))]
					self.triangle[tindex] = indexs
					tindex = tindex + 1
					for i,v in enumerate(indexs):
						if v in self.gameMap:#already exist
							self.gameMap[v].add(indexs[(i+1)%3])
						else:
							self.gameMap[v] = set([indexs[(i+1)%3]])
						self.gameMap[v].add(indexs[(i+2)%3])
			#path cost record
			for v in self.vertex:
				self.path(v)
		except Exception as e:
			raise e
		finally:
			mapFile.close()

	def printMap(self):
		for i,v in self.vertex.items():
				print i,":",v
		for k,v in self.gameMap.items():
			print k,":",v

	def distance(self, x1, y1, x2, y2):
		return math.pow(y1 - y2 , 2) + math.pow(x1 - x2 , 2)

	def moveCost(self, cur, next, dest = 1):
		dist = self.distance(self.vertex[next][0],self.vertex[next][1],self.vertex[cur][0],self.vertex[cur][1]) 
		total = dist + self.distance(self.vertex[next][0], self.vertex[next][1], self.vertex[dest][0], self.vertex[dest][1])
		return total

	def path(self, stat = 34, dest = 1):#A star pathing
		openList = []
		heapq.heappush(openList, Vertex(stat, 0))
		closed = set()
		while openList[0].index != dest:
			isRemove = False
	 		cur = heapq.heappop(openList)
	 		closed.add(cur.index)
	 		for neighbor in self.gameMap[cur.index]:
	 			if neighbor in closed:
	 				continue
	 			cost = cur.cost + self.moveCost(cur.index, neighbor, dest)
	 			newVertex = Vertex(neighbor, cost)
	 			if newVertex in openList :
	 				for oldV in openList:
	 					if oldV == newVertex and oldV.cost > newVertex.cost:
	 						openList.remove(oldV)
	 						isRemove = True
	 						break
	 			if (not newVertex in openList) and (not newVertex in closed):
	 				if isRemove:
	 					heapq.heapify(openList)
	 				heapq.heappush(openList, newVertex)
	 				newVertex.father = cur
	 	destVertex = openList[0]
	 	self.vcost[stat] = destVertex.cost
	 	father = None
	 	while not destVertex is None:
	 		father = destVertex.index
	 		destVertex = destVertex.father
	 	return self.vertex[father]

	def pathByPosition(self, x, z, dest = 1):
		result = 0
		cost = sys.maxint
		for tri in self.triangle.values():#Find close point
			#print tri
			if self.isInTriangle(tri[0], tri[1], tri[2], x, z):
				for i in tri:
					if self.vcost[i] < cost:
						result = i
						cost = self.vcost[i]
		if result == 0:
			dist = 0
			closeVertex = -1
			for k,v in self.vertex.items():
				d = self.distance(x, z, v[0], v[1])
				if closeVertex == -1:
					closeVertex = k
					dist = d
				else:
					if d < dist:
						dist = d
						closeVertex = k
			return self.path(closeVertex)
		return self.vertex[result]
		
		# #print "close:",closeVertex
		# self.path(closeVertex)

	def isInTriangle(self, a, b, c, x, z):
		va = self.vertex[a]
		vb = self.vertex[b]
		vc = self.vertex[c]
		v0x = vc[0] - va[0]
		v0z = vc[1] - va[1]
		v1x = vb[0] - va[0]
		v1z = vb[1] - va[1]
		v2x = x - va[0]
		v2z = z - va[1]
		dot00 = v0x*v0x + v0z*v0z
		dot01 = v0x*v1x + v0z*v1z
		dot02 = v0x*v2x + v0z*v2z
		dot11 = v1x*v1x + v1z*v1z
		dot12 = v2x*v1x + v2z*v1z
		inverDeno = 1/(dot00 * dot11 - dot01 * dot01)
		u = (dot11 * dot02 - dot01 * dot12) * inverDeno
		#print "U:",u
		if u < -PRECISION or u > 1:
			return False 
		v = (dot00 * dot12 - dot01 * dot02) * inverDeno
		#print "V:",v
		if v < -PRECISION or v > 1:
			return False 
		return u + v <= 1 
	
	def isArriveDest(self, x, z):
		if self.distance(x, z, self.vertex[self.dest][0], self.vertex[self.dest][1]) < CLOSEDISTANCE:
			return True
		return False

