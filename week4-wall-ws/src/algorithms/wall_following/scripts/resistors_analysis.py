#!/usr/bin/env python
import rospy
# from wall_following.msg import drive_param
from wall_following.msg import error_analysis
from std_msgs.msg import Float64
import numpy as np

# rad_10 = deg2rad(10)
# rad_20 = deg2rad(20)
global COUNT, TOTAL, MAX
COUNT = 0
TOTAL = 0
MAX = 0

pub = rospy.Publisher('wall_following_analysis', error_analysis, queue_size=1)

# Callback for receiving error data on the /pid_error topic
# data: the error from pid_error_node, published as a Float64
def control_callback(data):
	global COUNT, TOTAL, MAX
  	data = data.data
  	print('')
  	print('START')

	msg = error_analysis()

  	COUNT += 1
  	TOTAL += abs(data)
  	msg.average = TOTAL/COUNT
  	msg.max = MAX

  	print("MAX: " + str(MAX))
  	print('data: ' + str(data))
  	print('abs data: ' + str(abs(data)))

  	if abs(data) > MAX:
  		print('Updated Max')
  		MAX = abs(data)
  		msg.max = MAX
  		

	


	# print('')
	# print('Got Next Error HEY!')
	# print('Current Error: ' + str(data))
	print('COUNT: ' + str(COUNT))
	print("TOTAL: " + str(TOTAL))
	print("MAX: " + str(MAX))
	print('Published Average: ' + str(msg.average))
	print('Published Max: ' + str(msg.max))

	pub.publish(msg)

# Boilerplate code to start this ROS node.
# DO NOT MODIFY!
if __name__ == '__main__':
	rospy.init_node('resistors_analysis', anonymous=True)
	rospy.Subscriber("pid_error", Float64, control_callback)
	rospy.spin()

