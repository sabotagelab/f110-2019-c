#!/usr/bin/env python

import time
import rospy
from scipy.cluster.vq import vq, kmeans2, whiten
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan
import numpy as np
import math

def kmeans(data):
	whiten(data)
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
	gapCenter = [x, y, 0.0]
	pub.publish(gapCenter)

 
def callback(data):
	# create numpy array from data
	# format: [ range , intensity ]
	dataArray = np.empty((1081,3), dtype='float')
	numEntries = len(data.ranges)
	
	for x in range(0, numEntries):
		tmp = np.array([x, data.ranges[x], data.intensities[x]], dtype='float')
		#print(tmp)
		dataArray[x][:] = tmp
		#rospy.loginfo(data.ranges[x], data.intensities[x])
	print(dataArray)
	print("END")
	kmeans(dataArray)
	time.sleep(10)	
	#for item in data.ranges:
		#rospy.loginfo(item)
	

def listener():
	#initialize node
	rospy.init_node('find_gap', anonymous=True)	

	#create publisher for topic lidar_gaps
	pub = rospy.Publisher('lidar_gaps', Vector3, queue_size=100)
	
	#subscribe to lidar data
	rospy.Subscriber('scan', LaserScan, callback)	
	
	
	#define cycle rate
#	rate = rospy.Rate(1) #1GHz currently
	#pub.publish(gapCenter)
		
	rospy.spin()		

if __name__ == '__main__':
	listener()
