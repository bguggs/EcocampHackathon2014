from clustering import *
from datamatrix import *
from get_data import *
import numpy as np
import math
from scipy import stats

def indexOfClosestCenter(point, centers):
	cc_index = 0
	for i in range(0,len(centers)):
		if (point.distTo(centers[i]) < point.distTo(centers[cc_index])):
			cc_index = i
	return cc_index
	
def indexOfMaxDistToCenter(points, centers):
	max_dist_index = 0
	max_dist = points[0].distTo(centers[indexOfClosestCenter(points[0],centers)])
	for i in range(0,len(points)):
		curr_dist = points[i].distTo(centers[indexOfClosestCenter(points[i],centers)])
		if (curr_dist > max_dist):
			max_dist_index = i
			max_dist = curr_dist
	return max_dist_index
	
def kcenters(points, k, centers):
	if (k == len(centers)):
		return makeClustering(centers,points)
	else:
		if (len(centers) == 0):
			centers.append(points[0])
			return kcenters(points,k,centers)
		else:
			centers.append(points[indexOfMaxDistToCenter(points,centers)])
			return kcenters(points,k,centers)

def calculateCentroid(points):
	centroid_values = []
	if (len(points) > 0):
		for d in range(0,points[0].d):
			sum_dimension = 0
			for p in range(0,len(points)):
				sum_dimension += points[p].values[d]
			mean_dimension = sum_dimension/len(points)
			centroid_values.append(mean_dimension)
		return centroid_values
	else:
		return 0
		
def kmeans(points, k):
	myCluster = kcenters(points, k, [])
	steady = False
	while (not steady):
		steady = True
		centroidList = []
		for i in range(0,len(myCluster.clusters)):
			old_center = Point(myCluster.clusters[i].center.values, myCluster.clusters[i].center.meanArr, myCluster.clusters[i].center.statArr)
			new_centroid = calculateCentroid(myCluster.clusters[i].points)
			new_center = Point(new_centroid, myCluster.clusters[i].center.meanArr, myCluster.clusters[i].center.statArr)
			if(not old_center.equals(new_center)):
				steady = False
			centroidList.append(new_center)
		all_points = myCluster.getAllPoints()
		myCluster = makeClustering(centroidList, all_points)
	return myCluster
	
def createProximityMatrix(clustering):
	points = clustering.getAllPoints()
	pmatrix = np.zeros((len(points),len(points)))
	for r in range(0,len(points)):
		for c in range(0,len(points)):
			if points[r].equals(points[c]):
				pmatrix[r][c] = 0.0
			elif (points[r].outcome == 4 and points[c].outcome == 4):
				pmatrix[r][c] = 1.0
			else:
				pmatrix[r][c] = -1.0
	return pmatrix
		
def createIncidenceMatrix(clustering):
	points = clustering.getAllPoints()
	imatrix = np.zeros((len(points),len(points)))
	for r in range(0,len(points)):
		for c in range(0,len(points)):
			if points[r].equals(points[c]):
				imatrix[r][c] = 0.0
			elif points[r].clusternum == points[c].clusternum:
				imatrix[r][c] = 1.0
			else:
				imatrix[r][c] = -1.0
	#imatrix.tofile("imatrixTest",";")
	return imatrix
				
def calcCorrelation(PM,IM):
	x = PM.flatten()
	y = IM.flatten()
	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	return r_value ** 2

def mypearsonr(x, y):
    """
    Calculates a Pearson correlation coefficient and the p-value for testing
    non-correlation.

    The Pearson correlation coefficient measures the linear relationship
    between two datasets. Strictly speaking, Pearson's correlation requires
    that each dataset be normally distributed. Like other correlation
    coefficients, this one varies between -1 and +1 with 0 implying no
    correlation. Correlations of -1 or +1 imply an exact linear
    relationship. Positive correlations imply that as x increases, so does
    y. Negative correlations imply that as x increases, y decreases.

    The p-value roughly indicates the probability of an uncorrelated system
    producing datasets that have a Pearson correlation at least as extreme
    as the one computed from these datasets. The p-values are not entirely
    reliable but are probably reasonable for datasets larger than 500 or so.

    Parameters
    ----------
    x : (N,) array_like
        Input
    y : (N,) array_like
        Input

    Returns
    -------
    (Pearson's correlation coefficient,
     2-tailed p-value)

    References
    ----------
    http://www.statsoft.com/textbook/glosp.html#Pearson%20Correlation

    """
    # x and y should have same length.
    x = np.asarray(x)
    #print x
    y = np.asarray(y)
    n = len(x)
    mx = x.mean()
    my = y.mean()
    xm, ym = x-mx, y-my
    r_num = np.add.reduce(xm * ym)
    r_den = np.sqrt(stats.ss(xm) * stats.ss(ym))
    r = r_num / r_den
    #r = max(min(r, 1.0), -1.0)
    df = n-2
    if abs(r.all()) == 1.0:
        prob = 0.0
    else:
        t_squared = r*r * (df / ((1.0 - r) * (1.0 + r)))
        prob = betai(0.5*df, 0.5, df / (df + t_squared))
    return r, prob

