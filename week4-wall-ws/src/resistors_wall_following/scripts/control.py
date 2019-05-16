#!/usr/bin/env python
import rospy
from wall_following.msg import drive_param
from std_msgs.msg import Float64
import numpy as np
import yaml

global configSpd

# TODO: modify PD values to make car follow walls smoothly.
KP =  0.11
KD = 0.1275
rad_10 = np.deg2rad(10)
rad_20 = np.deg2rad(20)
rad_30 = np.deg2rad(30)
# rad_10 = deg2rad(10)
# rad_20 = deg2rad(20)
global DATA_PREVIOUS
DATA_PREVIOUS = 0    # Variable for previous error. Need for KD(de/dt) calculation

global configSpd
configSpd = 10

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)

# Callback for receiving error data on the /pid_error topic
# data: the error from pid_error_node, published as a Float64
def control_callback(data):
	global DATA_PREVIOUS
	global configSpd
  	data = data.data


	#print('')
	#print("JUST GOT ERROR")
	#print('20 deg to rad: ' + str(np.deg2rad(20)))
	##print('Current Error: ' + str(data))
	#print('Previous Error: ' + str(DATA_PREVIOUS))
	#print('KP: ' + str(KP))
	#print('KD: ' + str(KD))
	# Prof said I could look a few points behind and average. Or, take the previous 2
	# time stamps (which gives me 3 points), calculate de/dt based on the PREVIOUS
	# time stamp, and then use that one. This gives adjustment one time stamp late.

    # PD for Angle
	angle_KP = (data*KP)
	#angle = angle_KP
	angle_KD = (data - DATA_PREVIOUS)*KD   # Time between scans is constant. Thus, don't need to divide by time because constant KD handles it
	angle = angle_KP + angle_KD

	if abs(angle) >= rad_30:
		angle = np.sign(angle)*rad_30

    # PD for Speed
	if angle >= -rad_10 and angle <= rad_10:
	 velocity = configSpd
	elif (angle > rad_10 and angle <= rad_20) or (angle < -rad_10 and angle >= -rad_20):
	 velocity = 0.9 * configSpd
	else:
	 velocity = 0.85 * configSpd

	print('VELOCITY: ' + str(velocity))

    # Save and Publish PD Output
	msg = drive_param()
	msg.velocity = 0.5
	# msg.velocity = 0
	msg.angle = angle
	# msg.angle = .3
	pub.publish(msg)

	# msg.velocity = 1
	# msg.angle = .30
#	pub.publish(msg)

	DATA_PREVIOUS = data   # Save Current Error for Next Time

	#print('angle_KP: ' + str(angle_KP))
	# print('angle_KD: ' + str(angle_KD))
	#print("PD Angle Output: " + str(msg.angle))
	#print("PD Velocity Output: " + str(msg.velocity))

# Boilerplate code to start this ROS node.
# DO NOT MODIFY!
if __name__ == '__main__':
	

	rospy.init_node('pid_controller_node', anonymous=True)

	configDir = ""
	configIns = False

	data = rospy.get_param('topic_list')

	configDir, configIns, configSpd = data

	#configDir = f.readline()
	#configIns = f.readline()
	#configSpd = f.readline()

	rospy.Subscriber("pid_error", Float64, control_callback)
	rospy.spin()















