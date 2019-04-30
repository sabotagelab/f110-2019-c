#!/usr/bin/env python

import time
import rospy
from sklearn.cluster import DBSCAN
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan
import numpy as np
from numpy import inf
from numpy import NaN as nan
import math
import tf
import tf2_ros
import tf2_geometry_msgs

x = 0
y = 0

def dbscan(data):
	#4 6
	results = DBSCAN(eps=4, min_samples=8, algorithm='brute').fit(data)
	labels = results.labels_
	numClusters = len(set(labels)) - (1 if -1 in labels else 0)
	print("Num clusters: %d" % numClusters )
	print(labels)
	pickGap(results, data)

def pickGap(results, data):
	# calculate gap between each cluster
	clusters = []

	clusterCount = 0
	first = None

	# find start and end of each cluster
	labels = results.labels_
	pointData = [None] * 5
	average = 0
	averageCount = 1

	for x in range (0, len(labels) - 1):
		if (labels[x] != clusterCount and labels[x] != -1):
			print("LAST: %d" % x)
			pointData[0] = first
			pointData[1] = data[first][1]
			pointData[2] = x - 1
			pointData[3] = data[x][1]
			pointData[4] = average / averageCount
			clusters.append(pointData)
			clusterCount += 1
			pointData = [None] * 5
			first = None
			average = 0
			averageCount = 0
		elif labels[x] == clusterCount and first == None:
			first = x
			print("FIRST: %d" % first)
		
		average += data[x][1]
		averageCount += 1
	print(clusters)
	gaps = []

	# put only far range clusters in gaps
	for cluster in clusters:
		if cluster[4] > 4:
			gaps.append(cluster)

	# find widest gap
	max_width = 0
	max_gap = None
	for x in range(0, len(gaps)):
		if (gaps[x][2] - gaps[x][0] > max_width):
			max_gap = x

	target_gap = gaps[max_gap]
	print(target_gap)
	center = (target_gap[2] + target_gap[0]) / 2
	center_of_gap = [data[center][0], data[center][1]]
	print(center_of_gap)
	polarToCartesian(center_of_gap)

def polarToCartesian(middleGap):
	global x
	global y 

	x = middleGap[1] * math.cos(0.004363 * middleGap[0])
	y = middleGap[1] * math.sin(0.004363 * middleGap[0])
	print("X: ")
	print(x)
	print("Y: ")
	print(y)

 
def callback(data):
	# create numpy array from data
	# format: [ range , intensity ]
	dataArray = np.empty((513,2), dtype='float')
	numEntries = len(data.ranges)
	#numInt = len(data.intensities)
	print(numEntries)	
	#print(numInt)
	for x in range(0, numEntries - 1):
		rangeData = 0
		if np.isnan(data.ranges[x]) or np.isinf(data.ranges[x]):		#		data.ranges[x] == nan:
			rangeData = 5
		else:
			rangeData = data.ranges[x]

		if data.ranges[x] <= 1/10000:
			rangeData = 0
		tmp = np.array([x, rangeData], dtype='float')
		#print(tmp)
		dataArray[x][:] = tmp
		#rospy.loginfo(data.ranges[x], data.intensities[x])
#		print(rangeData)
#		time.sleep(.01)
	print(dataArray)
	print("END")
	dbscan(dataArray)
	time.sleep(1)	
	#for item in data.ranges:
		#rospy.loginfo(item)
	

def listener():
	#initialize node
	rospy.init_node('find_gap', anonymous=True)	

	#create publisher for topic lidar_gaps
	pub = rospy.Publisher('lidar_gaps', Vector3, queue_size=100)

	#subscribe to lidar data
	rospy.Subscriber('scan', LaserScan, callback)	
	print("END PRODUCT:")
	#print(gapInfo)
	
	v = Vector3()
	v.x = x
	v.y = y
	v.z = 0.0

	while not rospy.is_shutdown():
		v.x = x
		v.y = y
		rospy.sleep(1)	    		
		pub.publish(v)
	
	#define cycle rate
#	rate = rospy.Rate(1) #1GHz currently
	#pub.publish(gapCenter)
		
	rospy.spin()		

if __name__ == '__main__':
	listener()
