#!/usr/bin/env python

import rospy
import math
import numpy as np
import yaml
import sys
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64, Float32
from geometry_msgs.msg import Vector3
import turn_ahead.msg
import pdb
import itertools

# pub = rospy.Publisher('pid_error', Float64, queue_size=10)
cenDis = rospy.Publisher('centerDistance', Float64, queue_size=10)
testMarker = rospy.Publisher('edgeDetected', Vector3, queue_size=10)
turnAhead = rospy.Publisher('turn_ahead', turn_ahead, queue_size=10)

radarDistance = 4.00
angleInc = 0.00

scanBuffer = 20

oldrangeAvgLeft = 0.00
oldrangeAvgRight = 0.00

gapPercentError= 0.15

def scan_callback(data):
	global angleInc
	global oldrangeAvgLeft
	global oldrangeAvgRight

	distanceRightWall = 0.00
	distanceLeftWall = 0.00

	print("\n\n\n")

	numEntries = len(data.ranges)
	dataArray = np.zeros((numEntries,1), dtype='float')
	for x in range(0, numEntries - 1):
		rangeData = 0
		if np.isnan(data.ranges[x]) or np.isinf(data.ranges[x]):
			rangeData = 100
		else:
			rangeData = data.ranges[x]
		if data.ranges[x] <= 1/1000:
			rangeData = 0

		dataArray[x] = rangeData

	i = len(dataArray) - 1
	while True:
		if dataArray[i] > 0:
			distanceLeftWall = dataArray[i]
			break
		i -= 1
	
	i = 0
	while True:
		if dataArray[i] > 0:
			distanceRightWall = dataArray[i]
			break
		i += 1

	print("Distance Left: " + str(distanceLeftWall))
	print("Distance Right: " + str(distanceRightWall))

	angleInc = data.angle_increment

	middleIndice = len(data.ranges)/2

	# print("Middle: " + str(middleIndice))

	if distanceRightWall < 5:
		angleRight = math.acos(np.float64(distanceRightWall) / np.float64(radarDistance))
	else:
		angleRight = 0
	if distanceLeftWall < 5:
		angleLeft = math.acos(np.float64(distanceLeftWall) / np.float64(radarDistance))
	else:
		angleLeft = 0

	angleRightMid = math.pi/2 - angleRight
	angleLeftMid = math.pi/2 - angleLeft

	#print("Right Angle: " + str(angleRightMid))
	#print("Left Angle: " + str(angleLeftMid))	

	angleLeftInd = middleIndice + math.floor(angleLeftMid/angleInc)
	angleRightInd = middleIndice - math.floor(angleRightMid/angleInc)

	leftBufferCount = 0
	rightBufferCount = 0

	# print("Right Ind: " + str(angleRightInd))
	# print("Left Ind: " + str(angleLeftInd))

	if angleRight != 0:
		i = 0
		for i in itertools.islice(dataArray, angleRightInd - 2*scanBuffer, angleRightInd):
		 	#print("Right Indice: " +str(i))
			if i > 5:
				rightBufferCount += 1
	else:
		print("Right Wall Not detected!")

	if angleLeft != 0:
		i = 0
		for i in itertools.islice(dataArray, angleLeftInd, angleLeftInd + 2*scanBuffer):
			#print("Left Indice: " + str(i))
			if i > 5:
				leftBufferCount += 1
	else:
		print("Left Wall Not detected!")

	print("Right count: " + str(rightBufferCount))
	print("Left Count: "  + str(leftBufferCount))

	v = Vector3()
	msg = turn_ahead()
	msg.left = False
	msg.right = False
	if rightBufferCount > scanBuffer:
		print("Gap Detected on Right Side")
		v.y = -distanceRightWall
		v.x = distanceRightWall * math.tan(angleRight - angleInc * rightBufferCount)
		msg.right = True

	if leftBufferCount > scanBuffer:
		print("Gap Detected on Left Side")
		v.y = distanceLeftWall
		v.x = distanceLeftWall * math.tan(angleLeft - angleInc * leftBufferCount)
		msg.left = True

	# Walls lie above and below the x axis, right being negative.

	# v.y = -distanceLeftWall
	# v.x = distanceLeftWall * math.tan(angleLeft)
	v.z = 0.0

	testMarker.publish(v)
	turnAhead.publish(msg)

	print("X: " + str(v.x))
	print("Y: " + str(v.y))


# Boilerplate code to start this ROS node.
# DO NOT MODIFY!
if __name__ == '__main__':
	rospy.init_node('edgeDet', anonymous = True)
	rospy.Subscriber("scan", LaserScan, scan_callback)
	rospy.spin()
