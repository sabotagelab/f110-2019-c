#!/usr/bin/env python

import rospy
import math
import numpy as np
import yaml
import sys
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64, Float32
from geometry_msgs.msg import Vector3
from resistors_wall_following.msg import turn_ahead
import pdb
import itertools
from resistors_wall_following.msg import drive_param

# pub = rospy.Publisher('pid_error', Float64, queue_size=10)
cenDis = rospy.Publisher('centerDistance', Float64, queue_size=10)
testMarkerR = rospy.Publisher('edgeDetectedR', Vector3, queue_size=10)
testMarkerL = rospy.Publisher('edgeDetectedL', Vector3, queue_size=10)
turnAhead = rospy.Publisher('turn_ahead', turn_ahead, queue_size=10)

radarDistance = 4.00
angleInc = 0.00

scanBuffer = 15

oldrangeAvgLeft = 0.00
oldrangeAvgRight = 0.00

gapPercentError= 0.15

global repeatRight, repeatLeft, repeatability, VELOCITY
repeatRight = 0
repeatLeft = 0
repeatability = 5
VELOCITY = 0

def vel_callback(data):
	global VELOCITY
	VELOCITY = data.velocity

def scan_callback(data):
	global angleInc
	global oldrangeAvgLeft
	global oldrangeAvgRight
	global repeatRight, repeatLeft, repeatability

	distanceRightWall = 0.00
	distanceLeftWall = 0.00

	print("\n\n\n")
	print("-------------------------Edge Det--------------------------")

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

	print("Right Buffer Count: " + str(rightBufferCount))
	print("Left Buffer Count: "  + str(leftBufferCount))

	latestLeft = Vector3()
	latestRight = Vector3()
	v = Vector3()

	# Check if the number of empties clears the detector, if so tick up the repeater.
	if rightBufferCount > scanBuffer:
		print("Gap Detected on Right Side")
		latestRight.y = -distanceRightWall
		latestRight.x = distanceRightWall * math.tan(angleRight - angleInc * rightBufferCount)
		latestRight.z = 0.0
		repeatRight += 1
	
	if rightBufferCount <= scanBuffer:
		repeatRight = 0

	if leftBufferCount > scanBuffer:
		print("Gap Detected on Left Side")
		latestLeft.y = distanceLeftWall
		latestLeft.x = distanceLeftWall * math.tan(angleLeft - angleInc * leftBufferCount)
		latestLeft.z = 0.0
		repeatLeft += 1

	if leftBufferCount <= scanBuffer:
		repeatLeft = 0

	# Walls lie above and below the x axis, right being negative.

	msg = turn_ahead()
	msg.left = False
	msg.right = False

	v.x = 0.0
	v.y = 0.0
	v.z = 0.0

	if repeatLeft > repeatability:
		msg.left = True
		testMarkerL.publish(latestLeft)
		repeatLeft = 0
	else:
		testMarkerL.publish(v)

	if repeatRight > repeatability:
		msg.right = True
		testMarkerR.publish(latestRight)
		repeatRight = 0
	else:
		testMarkerR.publish(v)
	
	print("VELOCITY IN EDGE DET ()()())()()()(): " + str(VELOCITY))	
	if VELOCITY != 0:
		turnAhead.publish(msg)

	print("Repeat Left: " + str(repeatLeft))
	print("Repeat Right: " + str(repeatRight))
	print("Repeatability: " + str(repeatability))
	print("X: " + str(v.x))
	print("Y: " + str(v.y))
	print("-------------------------Edge Det--------------------------")
	print("\n\n\n")

# Boilerplate code to start this ROS node.
# DO NOT MODIFY!
if __name__ == '__main__':
	rospy.init_node('edgeDet', anonymous = True)
	rospy.Subscriber("scan", LaserScan, scan_callback)
	rospy.Subscriber("drive_parameters", drive_param, vel_callback)
	rospy.spin()
