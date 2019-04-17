#!/usr/bin/env python

import time
import rospy
from scipy.cluster.vq import vq, kmeans2, whiten
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

def kmeans(data):
	whiten(data, check_finite=False)
	#random.seed((1000,2000))
	codes = 3
	results = kmeans2(data, 3, iter=2, minit='points')
	print(results)
	pickGap(results[0])

def pickGap(results):
	np.argsort(results, axis=0)
	middleGap = results[1,:]
	print("MIDDLE GAP: ")
	print(middleGap)
	polarToCartesian(middleGap)	

def polarToCartesian(middleGap):
	x = middleGap[1] * math.cos(0.004363 * middleGap[0])
	y = middleGap[1] * math.sin(0.004363 * middleGap[0])
	print("X: ")
	print(x)
	print("Y: ")
	print(y)
	#callback_pub = rospy.Publisher("callback_gap",geometry_msgs/Vector3)
	#gapCenter[0] = [x, y, 0.0]
	#callback_pub.publish(gapCenter)

 
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
			rangeData = 1000
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
	kmeans(dataArray)
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
	pub.publish(v)	
	
	#define cycle rate
#	rate = rospy.Rate(1) #1GHz currently
	#pub.publish(gapCenter)
		
	rospy.spin()		

if __name__ == '__main__':
	listener()
