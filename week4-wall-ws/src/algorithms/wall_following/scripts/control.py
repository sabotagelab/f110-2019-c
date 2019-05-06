#!/usr/bin/env python
import rospy
from wall_following.msg import drive_param
from std_msgs.msg import Float64
import numpy as np

# TODO: modify PD values to make car follow walls smoothly.
KP = 1.0
KD = 1.0
global DATA_PREVIOUS
DATA_PREVIOUS = 0    # Variable for previous error. Need for KD(de/dt) calculation

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)

# Callback for receiving error data on the /pid_error topic
# data: the error from pid_error_node, published as a Float64
def control_callback(data):
	global DATA_PREVIOUS
  	data = data.data

	print('')
	print("JUST GOT ERROR")
	print('Current Error: ' + str(data))
	print('Previous Error: ' + str(DATA_PREVIOUS))
	print('KP: ' + str(KP))
	print('KD: ' + str(KD))
	# Prof said I could look a few points behind and average. Or, take the previous 2
	# time stamps (which gives me 3 points), calculate de/dt based on the PREVIOUS
	# time stamp, and then use that one. This gives adjustment one time stamp late.

    # PD for Angle
	angle_KP = (data*KP)
	angle_KD = (data - DATA_PREVIOUS)*KD   # Time between scans is constant. Thus, don't need to divide by time because constant KD handles it
	angle = angle_KP + angle_KD

    # PD for Speed
  	if angle >= -10 and angle <= 10:
		velocity = 1.5
 	elif (angle > 10 and angle <= 20) or (angle < -10 and angle >= -20):
		velocity = 1.0
  	else:
		velocity = 0.5

    # Save and Publish PD Output
	msg = drive_param()
	msg.velocity = velocity
	msg.angle = angle
	pub.publish(msg)
	DATA_PREVIOUS = data   # Save Current Error for Next Time

	print('angle_KP: ' + str(angle_KP))
	print('angle_KD: ' + str(angle_KD))
	print("PD Angle Output: " + str(msg.angle))
	print("PD Velocity Output: " + str(msg.velocity))

# Boilerplate code to start this ROS node.
# DO NOT MODIFY!
if __name__ == '__main__':
	rospy.init_node('pid_controller_node', anonymous=True)
	rospy.Subscriber("pid_error", Float64, control_callback)
	rospy.spin()

