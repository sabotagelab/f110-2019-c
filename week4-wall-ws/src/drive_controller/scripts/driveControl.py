#!/usr/bin/env python
import rospy
import instruction as instruction
from std_msgs import Bool, String
from sensor_msgs.msg import LaserScan

# 1.571 rad = 90 deg:

FOLLOWING_WALL = False

def turn_callback(data):
	if (data):
		# stop wall following
		system(rosnode kill wall_following)
		print("Entering cornering mode")
		# TURNING STUFF

	else:
		if (!FOLLOWING_WALL)
			system(roslaunch wall_following wall_following.py)
			print("Restarting wall following")
			FOLLOWING_WALL = True


if __name__ == '__main__':
	rospy.init_node('drive_control_node', anonymous=True)
	rospy.Subscriber("turn_ahead", Bool, turn_callback)
	rospy.spin()