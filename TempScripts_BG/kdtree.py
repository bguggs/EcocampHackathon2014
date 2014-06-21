from get_data import *
#from clustering import *
#from datamatrix import *
import math

class Node:
	def __init__ (self, point, dimension, parent):
		self.point = point
		self.left = None
		self.right = None
		self.parent = parent
		self.dimension = dimension
	
class KDTree:
	def __init__ (self, points):
		self.points = points
		self.root = self.makeKDTree(points, 0, None)
		
	def makeKDTree(self, pointList, splitIndex, parent):
		split_dimension = splitIndex % len(pointList)
		plen = len(pointList)
		if plen < 1:
			return None
		if plen == 1:
			return Node(pointList[0], split_dimension, parent)
		else:
			pointList = sorted(pointList, key=lambda point: point.values[split_dimension])
			median = int(plen/2)
			node = Node(pointList[median], split_dimension, parent)
			node.left = self.makeKDTree(pointList[0:median], splitIndex + 1, node)
			node.right = self.makeKDTree(pointList[median:], splitIndex + 1, node)
			return node

	def findNearestNeighborHelper(self, search_point, current_node, current_best_node):
		if current_node.point.distTo(search_point) < current_best_node.point.distTo(search_point):
			current_best_node = current_node
		
		if current_node.left == None and current_node.right == None:
			return current_best_node
		elif current_node.right == None:
			current_best_node = self.findNearestNeighborHelper(search_point, current_node.left, current_best_node)
		elif (current_node.left == None):
			current_best_node = self.findNearestNeighborHelper(search_point, current_node.right, current_best_node)
		else:
			splitdim = current_node.dimension % current_node.point.d
			if search_point.values[splitdim] < current_node.point.values[splitdim]:
				current_best_node = self.findNearestNeighborHelper(search_point, current_node.left, current_best_node)
			if (math.fabs(current_node.point.values[current_node.dimension] - search_point.values[current_node.dimension]) < search_point.distTo(current_best_node.point)):
				current_best_node = self.findNearestNeighborHelper(search_point, current_node.right, current_best_node)
			else:
				current_best_node = self.findNearestNeighborHelper(search_point, current_node.right, current_best_node)
				if math.fabs(current_node.point.values[splitdim] - search_point.values[splitdim]) < search_point.distTo(current_best_node.point):
					current_best_node = self.findNearestNeighborHelper(search_poitn, current_node.left, current_best_node)
		return current_best_node
	
	def findNearestNeighbor(self, querypoint):
		return self.findNearestNeighborHelper(querypoint, self.root, self.root)
	
	def removePoint(self, point):
		newList = []
		for item in self.points:
			if (not item.equals(point)):
				newList.append(item)
		return newList
		
	def findkNearestNeighbors(self, querypoint, k):
		return self.kNearestNeighborsHelper(self.points, k, querypoint, [])
			
	def kNearestNeighborsHelper(self,points, k, QP, neighborList):
		if k == 0:
			return neighborList
		else:
			tree = KDTree(points)
			NN = tree.findNearestNeighbor(QP)
			#print NN.point.values[0:3]
			neighborList.append(NN.point)
			return self.kNearestNeighborsHelper(tree.removePoint(NN.point), k-1, QP, neighborList)
			
"""
x = dataMatrix("filledNumericDataCleanwithTitleandId.csv")
point = Point([0.1198,0.0010,0.6782,0.0061,-0.9410478216,-0.9631942510,0.1197,0.0011,-0.7811699664,-0.9288089971,-0.8118287703,-0.8386739881,90.0000,48.0000,1,2.0000,0,2,1,0,3,5.1000,16.0000,0,0,0,0,0,0,5.1000,5.2700,271.2600,271.2600,64.5200,220.2200,221.2000,271.2600,57.2000,7.0000,0.0001,4.1000,4.3300,0,0,0,0,0,0,4.1000,2.8800,221.2000,221.2000,51.0400,156.6700,0,0.0000,34.1400,5.0000,0,9.2000,20.3300,0,0,0,0,0,0,9.2000,8.1500,492.4600,492.4600,115.5600,376.8900,221.2000,271.2600,91.3400,12.0000,0.0001,20.9100,69.2800,1,1,1,1,1,1,20.9100,15.1776,60002.7120,60002.7120,3293.1008,34501.8674,0.0000,0.0000,1952.8080,35.0000,0.0000,12.6500,34.0700,34.0700,3.5600,6.6200,27.2400,3.3600,6.5800,13.3600,13.2500,211.8000,211.8000,211.8000,0,194.0400,17.7600,8.8800,0.0001,2.0000,12.6500,34.0700,34.0700,3.5600,6.6200,27.2400,3.3600,6.5800,13.3600,13.2500,211.8000,211.8000,211.8000,0,194.0400,17.7600,8.8800,0.0001,2.0000,12.6500,34.0700,34.0700,3.5600,6.6200,27.2400,3.3600,6.5800,13.3600,13.2500,211.8000,211.8000,211.8000,0,194.0400,17.7600,8.8800,0.0001,2.0000,12.6500,34.0700,34.0700,3.5600,6.6200,27.2400,3.3600,6.5800,13.3600,13.2500,211.8000,211.8000,211.8000,0.0000,194.0400,17.7600,8.8800,0.0001,2.0000,0.04086104666,4.97931167827,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,0.12627223511,0.09498066511,34.0859783449,34.0859783449,6.98846609951,26.2594070637,-0.5660221706,33.8131245166,11.462588296,0.49639082237,-0.5629028100,0.04086104666,4.97931167827,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,0.12627223511,0.09498066511,34.0859783449,34.0859783449,6.98846609951,26.2594070637,-0.5660221706,33.8131245166,11.462588296,0.49639082237,-0.5629028100,0.04086104666,4.97931167827,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,0.12627223511,0.09498066511,34.0859783449,34.0859783449,6.98846609951,26.2594070637,-0.5660221706,33.8131245166,11.462588296,0.49639082237,-0.5629028100,0.04086104666,4.97931167827,-0.6777519979,-0.6777519979,-0.6777519979,-0.6777519979,-0.6777519979,-0.6777519979,0.12627223511,0.09498066511,34.0859783449,34.0859783449,6.98846609951,26.2594070637,-0.5660221706,33.8131245166,11.462588296,0.49639082237,-0.5629028100,0.0196,0.0518,0.0000,0.0029,0.0000,0.0029,6.6875,17.6784,5.7278,0.0225,0.0518,0.0029,0,0,0,0,0,1,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,1,2], x.createMeanArrayAllCols(), x.createStdevArrayAllCols())

tree = KDTree(x.createPointList())
nnors = tree.findkNearestNeighbors(point, 5)
for item in nnors:
	print item.values[0], item.outcome
 #nnors[0].values[0:3]
#for item in nnors:
	#print item.point.values[0:5]
	"""
			
