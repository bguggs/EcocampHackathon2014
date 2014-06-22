from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
#from sklearn.neighbors.kd_tree import KDTree
#from sklearn.neighbors import DistanceMetric
import numpy as np
import get_data2 as gd
import json

headers = gd.get_headers()
dicts = gd.get_data_list_of_dicts()

rows_lol = []
for i in range(len(gd.get_data_slice(headers[0], dicts))):
	rows_lol.append([])

print len(rows_lol)

for i in range(len(headers)):
	column = gd.get_data_slice(headers[i], dicts)

	for j in range(len(gd.get_data_slice(headers[0], dicts))):
		rows_lol[j].append(column[j])

print rows_lol[0]

#actually get similarities

def compare_rows(row1, row2):
	counter = 0
	for i in range(len(row1)):
		if row1[i] == row2[i]:
			counter +=1
	return counter
		
"""
similarities = []
for i in range(len(gd.get_data_slice(headers[0], dicts))):
	similarities.append([])

for i in range(len(rows_lol)):
	cur_row = rows_lol[i]
	for j in range(len(rows_lol)):
		if j != i:
			if compare_rows(cur_row, rows_lol[j]) >=:
				similarities[i].append(j)

print similarities
"""
			
X = np.array(rows_lol)			
nbrs = NearestNeighbors(n_neighbors = 10, algorithm ='kd_tree').fit(X)
distances, indices = nbrs.kneighbors(X)
a = indices
#print a

"right here"
a = a.tolist()

print a 
final = []
for each in a:
	final.append(each[2:])
print final


with open('hack_similar.json', 'w') as outfile:
	json.dump(final, outfile)

print headers
