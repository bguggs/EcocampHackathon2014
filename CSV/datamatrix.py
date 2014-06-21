from get_data import *
#from clustering import *
#import linreg
#import copy
import numpy as np
#import statistics as stat
#import math
#import random
#import sys
#from kdtree import *

#file = raw_input('Input data file...')
#DATA_FILENAME = file
missing_data_token = "-1";

#To loop through, go CR not RC
class dataMatrix:
	#Initialize data-matrix from file. Properties are (header_list, dataset, num_cols, num_rows)
	def __init__(self, filename):
		self.header_list = get_headers(filename)
		self.num_cols = len(self.header_list)
		self.dataset = []
		l_of_d = get_data_list_of_dicts(filename)
		for i in range(0, self.num_cols):
			self.dataset.append(get_data_slice(self.header_list[i], l_of_d))
		self.num_rows = len(self.dataset[0])
		self.cleaningflags = np.zeros((self.num_cols, self.num_rows))

	def cutHeadersByXChars(self, charNum):
		for c in range (0, self.num_cols):
			new_header = self.header_list[c]
			self.header_list[c] = new_header[charNum:]

	def cutColFromEnd(self, col_num, charNum):
		for r in range(0, self.num_rows):
			new_dataset = self.dataset[col_num]
			self.dataset[col_num][r] = new_dataset[0:(len(new_dataset)-charNum)]

    #Remove a column from the dataset by column number
	def removeColumn(self, col_num):
		self.header_list.pop(col_num)
		self.dataset.pop(col_num)
		self.cleaningflags = np.delete(self.cleaningflags, col_num, 0)
		self.num_cols -= 1

	def removeRow(self, row_num):
		#print row_num
		#print self.num_rows
		for c in range(0,self.num_cols):
			#print c
			self.dataset[c].pop(row_num)
			#self.cleaningflags = np.delete(self.cleaningflags, row_num, 1)
		self.num_rows -= 1

	def getNumRows(self):
		len(self.dataset[0]);

	#Get the column number of a specific header name (helps remove column by name)
	def getColNum(self, header_name):
		return self.header_list.index(header_name)

	#Write the matrix to a csv. Filename is given by user.
	def writeFile(self):
		out_file = raw_input('Write full datafile where? ...')
		set_to_write = np.transpose(self.dataset)
		write_data(out_file, self.header_list, set_to_write)

	def writeToFile(self,filename):
		set_to_write = np.transpose(self.dataset)
		write_data(filename, self.header_list, set_to_write)

	def writeArray(self, array):
		out_file = raw_input('Write stdev with mean array where? ...')
		with open(out_file,'w') as f:
			f_csv = csv.writer(f)
			for i in range(len(array)):
				f_csv.writerow(array[i])

	def writeCleaningFlagFile(self):
		out_file = raw_input('Write flag file where? ...')
		set_to_write = np.transpose(self.cleaningflags)
		write_data(out_file, self.header_list, set_to_write)

	#find the correlation between two columns of the data matrix
	def findLinreg(self, col_num_one, col_num_two):
		A = np.vstack([self.dataset[col_num_one], np.ones(len(self.dataset[col_num_two]))]).T
		m, b = np.linalg.lstsq(A, self.dataset[col_num_two])[0]
		return m #, b

	#find all of the linregs. Returns a list of all comparisons in the form {Col1, Col2, Correl}
	def findAllLinregs(self):
		linreg_list = []
		for i in range(0,self.num_cols):
			for j in range(0, self.num_cols):
				if float(i) and float(j) and i != j:
					to_add = [self.header_list[i], self.header_list[j], self.findLinreg(i, j)]
					linreg_list.append(to_add)
					#print to_add
		return linreg_list



	#Removes any linregs that are correlated in a certain range
	def removeCorrelatedLinregs(self):
		correl_range = [.98,1.02]
		for i in xrange(self.num_cols):
			for j in range(self.num_cols):
				if i != j:
					if (-correl_range[0] > self.findLinreg(i,j) > -correl_range[1] or correl_range[0] < self.findLinreg(i,j) < correl_range[1]):
						if not (self.header_list[j] == "purity" or self.header_list[j] == "outcome"):
							print "x.removeColumn(x.getColNum(' ", self.header_list[j]
							self.removeColumn(j)
							return self.removeCorrelatedLinregs()
	#Prints all of the linregs between a certain correlation to the terminal in a user-friendly format
	def printLinregs(self):
		linreg_list = self.findAllLinregs()
		correl_range = [.9,1.1]
		for item in linreg_list:
			if (-correl_range[0] > item[2] > -correl_range[1] or correl_range[0] < item[2] < correl_range[1]):
				print "Correlation of " + item[0] + " and " + item[1] + " is " + str(item[2])[:5]

	#Returns a list of all of the correlations in a list (useful for min/max linreg)
	def allLinregs(self):
		just_correls = []
		linreg_list = self.findAllLinregs()
		for item in linreg_list:
			just_correls.append(item[2])
		return just_

	#Finds the mean value of a given column (helper for filling missing rows with mean)
	def meanCol(self,num_col):
		sum = 0
		counter = 0
		for i in self.dataset[num_col]:
			if i != missing_data_token:
				sum += float(i)
			else:
				counter+=1
		return sum/(self.num_rows-counter)

	#Find standard deviation of a given column
	def stdevCol(self, num_of_col):
		#find the variance
		mean = self.meanCol(num_of_col)
		squared_diffs = []
		#calculated all squared diffs
		for num in self.dataset[num_of_col]:
			try:
				squared_diffs.append((float(num)-mean)**2)
			except ValueError:
				print "problem with"
				print num
		#find the average of the squared_differences
		n = len(squared_diffs)
		sum_sdiffs = 0
		for item in squared_diffs:
			sum_sdiffs += item
		variance = sum_sdiffs/n
		return math.sqrt(variance)

	def createStdevArrayAllCols(self):
		stdev_arr = []
		#print self.num_cols
		for i in xrange(0, self.num_cols):
			stdev_arr.append(self.stdevCol(i))
		return stdev_arr

	def createMeanArrayAllCols(self):
		mean_arr = []
		for i in xrange(0, self.num_cols):
			mean_arr.append(self.meanCol(i))
		return mean_arr


	#Fills any missing data fields with the mean of its column. Missing data must be marked by a
	def fillMissingFieldsWithMean(self):
		counter = 0
		for i in xrange(0,self.num_cols):
			for j in xrange(0, self.num_rows):
				#if j == 0:
					#print "i, j: "
					#print i,j
					#print " " + self.dataset[i][j]
				if self.dataset[i][j] == "?" or self.dataset[i][j] == missing_data_token:
					counter += 1
					self.dataset[i][j] = self.meanCol(i)
					self.cleaningflags[i][j] = 1

	def is_number(self, s):
		try:
		    float(s)
		    return True
		except ValueError:
		    return False

	#convert yes/no to 1/0
	def convertYesNotoOneZero(self):
		counter = 0
		for i in xrange(0,self.num_cols):
			for j in xrange(0, self.num_rows):
				#if j == 0:
					#print "i, j: "
					#print i,j
					#print " " + self.dataset[i][j]
				if self.dataset[i][j] == "yes":
					counter += 1
					self.dataset[i][j] = 1
					self.cleaningflags[i][j] = 1
				elif self.dataset[i][j] == "no":
					counter += 1
					self.dataset[i][j] = 0
					self.cleaningflags[i][j] = 1
				elif self.dataset[i][j] == "?":
					counter += 1
					self.dataset[i][j] = 0
					self.cleaningflags[i][j] = 1

	#Remove non-numeric columns
	def removeStringCols(self):
		counter = 0
		for i in xrange(0,self.num_cols):
			for j in xrange(1, self.num_rows):
				if (self.is_number(self.dataset[i][j]) == False and not (self.dataset[i][j]) == "?"):
					print self.dataset[i][j]
					print "x.removeColumn(x.getColNum(': " + str(i)
					counter += 1
					self.removeColumn(i)
					return self.removeStringCols()


	def isMadeUp(self, row, col):
		self.cleaningflags

	def removeRandomCols(self, numEndingCols):
		while (self.num_cols > numEndingCols):
			delCol = random.randint(10,self.num_cols-3)
			self.removeColumn(delCol)

	def removeRandomRows(self, numEndingRows):
		while (self.num_rows > numEndingRows):
			#print "numrows"
			#print self.num_rows
			delRow = random.randint(0,self.num_rows-1)
			#print "delrow:"
			#print delRow
			self.removeRow(delRow)

	def addIds(self):
		id_list = []
		for i in range(0, self.num_rows):
			id_list.append(i)
		col_list = [id_list]
		for c in range(0, self.num_cols):
			col_list.append(self.dataset[c])
		self.dataset = col_list
		new_headers = ["id"]
		for item in self.header_list:
			new_headers.append(item)
		self.header_list = new_headers

	def removeColumn(self, col_num):
		self.header_list.pop(col_num)
		self.dataset.pop(col_num)
		self.cleaningflags = np.delete(self.cleaningflags, col_num, 0)
		self.num_cols -= 1

	def getOnlyCols(self, colarray):
		newDataset = []
		newHeaders = []
		for col in colarray:
			newHeaders.append(self.header_list[col])
			newDataset.append(self.dataset[col])

		#add purity and outcome
		newHeaders.append(self.header_list[self.num_cols-2])
		newDataset.append(self.dataset[self.num_cols-2])
		newHeaders.append(self.header_list[self.num_cols-1])
		newDataset.append(self.dataset[self.num_cols-1])
		self.dataset = newDataset
		self.header_list = newHeaders
		self.num_cols = len(self.header_list)
		self.num_rows = len(self.dataset[0])


	def createPointList(self):
		meanArr = self.createMeanArrayAllCols()
		statArr = self.createStdevArrayAllCols()
		pointList = []
		for r in range(0, self.num_rows):
			valuesArr = []
			for c in range(0,self.num_cols):
				valuesArr.append(float(self.dataset[c][r]))
			#print "ValuesArr: ", valuesArr
			pointList.append(Point(valuesArr, meanArr, statArr))
		return pointList

	#Prints the data matrix... poorly
	def __repr__(self):
		headers = ""
		data = ""
		for item in self.header_list:
			headers += item + ", "
		for item in self.dataset:
			data += str(item) + ", "
		return str(headers[:-1]) + "\n" + str(data[:-2])

#Main



#point = Point(0.1198,0.0010,0.6782,0.0061,-0.9410478216,-0.9631942510,0.1197,0.0011,-0.7811699664,-0.9288089971,-0.8118287703,-0.8386739881,90.0000,48.0000,1,2.0000,0,2,1,0,3,5.1000,16.0000,0,0,0,0,0,0,5.1000,5.2700,271.2600,271.2600,64.5200,220.2200,221.2000,271.2600,57.2000,7.0000,0.0001,4.1000,4.3300,0,0,0,0,0,0,4.1000,2.8800,221.2000,221.2000,51.0400,156.6700,0,0.0000,34.1400,5.0000,0,9.2000,20.3300,0,0,0,0,0,0,9.2000,8.1500,492.4600,492.4600,115.5600,376.8900,221.2000,271.2600,91.3400,12.0000,0.0001,20.9100,69.2800,1,1,1,1,1,1,20.9100,15.1776,60002.7120,60002.7120,3293.1008,34501.8674,0.0000,0.0000,1952.8080,35.0000,0.0000,12.6500,34.0700,34.0700,3.5600,6.6200,27.2400,3.3600,6.5800,13.3600,13.2500,211.8000,211.8000,211.8000,0,194.0400,17.7600,8.8800,0.0001,2.0000,12.6500,34.0700,34.0700,3.5600,6.6200,27.2400,3.3600,6.5800,13.3600,13.2500,211.8000,211.8000,211.8000,0,194.0400,17.7600,8.8800,0.0001,2.0000,12.6500,34.0700,34.0700,3.5600,6.6200,27.2400,3.3600,6.5800,13.3600,13.2500,211.8000,211.8000,211.8000,0,194.0400,17.7600,8.8800,0.0001,2.0000,12.6500,34.0700,34.0700,3.5600,6.6200,27.2400,3.3600,6.5800,13.3600,13.2500,211.8000,211.8000,211.8000,0.0000,194.0400,17.7600,8.8800,0.0001,2.0000,0.04086104666,4.97931167827,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,0.12627223511,0.09498066511,34.0859783449,34.0859783449,6.98846609951,26.2594070637,-0.5660221706,33.8131245166,11.462588296,0.49639082237,-0.5629028100,0.04086104666,4.97931167827,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,0.12627223511,0.09498066511,34.0859783449,34.0859783449,6.98846609951,26.2594070637,-0.5660221706,33.8131245166,11.462588296,0.49639082237,-0.5629028100,0.04086104666,4.97931167827,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,-0.8388759989,0.12627223511,0.09498066511,34.0859783449,34.0859783449,6.98846609951,26.2594070637,-0.5660221706,33.8131245166,11.462588296,0.49639082237,-0.5629028100,0.04086104666,4.97931167827,-0.6777519979,-0.6777519979,-0.6777519979,-0.6777519979,-0.6777519979,-0.6777519979,0.12627223511,0.09498066511,34.0859783449,34.0859783449,6.98846609951,26.2594070637,-0.5660221706,33.8131245166,11.462588296,0.49639082237,-0.5629028100,0.0196,0.0518,0.0000,0.0029,0.0000,0.0029,6.6875,17.6784,5.7278,0.0225,0.0518,0.0029,0,0,0,0,0,1,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,1,2)

print "starting"
x = dataMatrix("temp.csv")
x.cutHeadersByXChars(12)
x.cutColFromEnd(1, 16)
print "doneCutting"
#tree = KDTree(x.getAllPoints)
#print "valueArr:"
#print tree.findNearestNeighbor(point).valuesArr[0:10]

#print x.dataset[x.getColNum('origintime')]
#x.addIds()
#x.writeToFile("filledNumericDataCleanwithTitleandId.csv")
#x.convertYesNotoOneZero()
#x.removeStringCols()
#print "Removed columns containing strings"
#x.fillMissingFieldsWithMean()
#print "filled missing data rows with the mean"
#x.removeColumn(x.getColNum('LemasSwFTPerPop'))

#print "removing correlated linregs"
#x.removeCorrelatedLinregs()
#print "removed correlated linregs"
#print "attempting to create array of stdevs and means"
#arr_file = [x.createStdevArrayAllCols(), x.createMeanArrayAllCols()]
#x.writeArray(arr_file)


#print x.cleaningflags

#x.printLinregs()
#print "Removing Correlated Linregs... Please go get some water while you wait"
#x.removeCorrelatedLinregs()
#x.writeCleaningFlagFile()
#x.writeFile()
#x.getOnlyCols([1,3,5])
print "writing..."
x.writeFile()


# make doctest work:
def _test():
    import doctest
    result = doctest.testmod()
    if result[0] == 0:
        print "Wahoo! Passed all", result[1], __file__.split('/')[-1], "tests!"
    else:
       print "Rats!"
