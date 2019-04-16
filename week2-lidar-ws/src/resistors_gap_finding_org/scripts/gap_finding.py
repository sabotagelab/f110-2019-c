#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan
 
def callback(data):
	rospy.loginfo(data.data)

def listener():
	#initialize node
	ros.init_mode('', anonymous=True)	

	#create publisher for topic lidar_gaps
	pub = rospy.Publisher('lidar_gaps', anonymous=True)
	
	#subscribe to lidar data
	rospy.Subscriber('scan', LaserScan, callback)	

	#define cycle rate
	rate = rospy.Rate(1) #1GHz currently
	
	rospy.spin()		

if __name__ == '__main__':
	listener()
