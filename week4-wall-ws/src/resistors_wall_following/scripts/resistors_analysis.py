#!/usr/bin/env python
import rospy
# from wall_following.msg import drive_param
from visualization_msgs.msg import Marker
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
pub_ave = rospy.Publisher('analysis_average', Marker, queue_size="1")
pub_max = rospy.Publisher('analysis_max', Marker, queue_size="1")

def make_marker(marker):
	marker.header.frame_id = "/laser"
	marker.pose.position.x = 1
	# marker.pose.position.y = 1
	marker.pose.position.z = 0 # or set this to 0
	marker.type = marker.TEXT_VIEW_FACING
	marker.scale.x = .2 # If marker is too small in Rviz can make it bigger here
	marker.scale.y = .2
	marker.scale.z = .2
	marker.color.a = 1.0
	marker.color.r = 1.0
	marker.color.g = 1.0
	marker.color.b = 0.0

	return marker



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


  	marker_ave = Marker()
  	marker_ave.text = 'Average Error: ' + str(np.round(msg.average, decimals = 3))
  	marker_ave.pose.position.y = 1
  	marker_ave = make_marker(marker_ave)
  	pub_ave.publish(marker_ave)
  		
  	marker_max = Marker()
  	marker_max.text = 'Max Error: ' + str(np.round(msg.max, decimals = 3))
  	marker_max.pose.position.y = 2
  	marker_max = make_marker(marker_max)
  	pub_max.publish(marker_max)
	


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

