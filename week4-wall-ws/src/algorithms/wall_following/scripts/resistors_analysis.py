#!/usr/bin/env python
import rospy
from wall_following.msg import error_analysis
from std_msgs.msg import Float64
import numpy as np

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
  	print('RECEIVED: pid_error msg')

	msg = error_analysis()
  	COUNT += 1
  	TOTAL += abs(data)
  	msg.average = TOTAL/COUNT
  	msg.max = MAX

  	print("Error's Current MAX: " + str(MAX))
  	print('Absolute Val. of New Error: ' + str(abs(data)))

  	if abs(data) > MAX:
  		print('We Just Got a New MAX! ')
  		MAX = abs(data)
  		msg.max = MAX

	print("Final MAX: " + str(MAX))
	print('Published AVE: ' + str(msg.average))
	print('Published MAX: ' + str(msg.max))
	pub.publish(msg)

# Boilerplate code to start this ROS node.
# DO NOT MODIFY!
if __name__ == '__main__':
	rospy.init_node('resistors_analysis', anonymous=True)
	rospy.Subscriber("pid_error", Float64, control_callback)
	rospy.spin()

