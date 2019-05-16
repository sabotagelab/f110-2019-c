#!/usr/bin/env python
import rospy
from file_instructions.msg import instruction
from std_msgs.msg import Bool, String
from sensor_msgs.msg import LaserScan
from drive_controller.msg import side_check
from resistors_wall_following.msg import drive_param, turn_ahead
from os import system
import numpy as np

# 1.571 rad = 90 deg:
pub_drive = rospy.Publisher('drive_parameters', drive_param, queue_size=10)
pub_turnstat = rospy.Publisher('turn_finished', String, queue_size=10)

global FOLLOWING_WALL, TURNING_DIRECTION, VELOCITY
FOLLOWING_WALL = False
TURNING_DIRECTION = None
VELOCITY = 0

def get_direction_callback(data):
	global TURNING_DIRECTION, VELOCITY
	TURNING_DIRECTION = data.direction
	VELOCITY = data.velocity
	print("~~~~~~~~~~~~~~ DIRECTION WE GET FROM FILE: " + str(TURNING_DIRECTION))
	print("~~~~~~~~~~~~~~ VELOCITy WE GET FROM FILE: " + str(VELOCITY))

	print("~~~~~~~~~~~~~~ DIRECTION LENGTH WE GET FROM FILE: " + str(len(str(TURNING_DIRECTION))))


def during_turn_callback(data):
	# stop wall following
	global FOLLOWING_WALL
	if (FOLLOWING_WALL):
		system('rosnode kill /pid_error_node')
		system('rosnode kill /control_node')
		print(">>>>>>>>>>>>>>>>>>>> Entering cornering mode <<<<<<<<<<<<<<<<<<<<<<<<<<")
		pub_turnstat.publish("True")
		FOLLOWING_WALL = False
	msg = drive_param()

	# wait for turn to be right next to the car
	if(not data.left and not data.right):
		msg.velocity = 1
		msg.angle = 0
		pub_drive.publish(msg)
		#print("Waiting for turn...")
		#rospy.Subscriber("check_side", side_check, during_turn_callback)
		

	#print('______________________  TURNING DIRECTION _____________________ : ' + str(TURNING_DIRECTION))

	# if direction says to go straight
	length = len(str(TURNING_DIRECTION))

	print("TURNING INStrUCTION LENGTH : " + str(length))
	print("LENGTH Of DATA LEFT" + str(len(str(data.left))))
	print("DATA LEFT " + str(data.left))
	if (length == 8):
		if(data.left or data.right):
			print("Going straight")
			msg.velocity = VELOCITY
			msg.angle = 0
			pub_drive.publish(msg)

		# publish that we finished the "turn" so we get next direction
		# pub_turnstat.Publish(True)

	elif (length == 4):
		if(data.left):
			print("!!!!!! TURNING LEFT!!!!!!")
			msg.velocity = VELOCITY
			msg.angle = np.deg2rad(30)
			pub_drive.publish(msg)
		# pub_turnstat.Publish(True)

	elif (length == 5):
		if(data.right):
			print("!!!!!! TURNING RIGHT!!!!!!")
			msg.velocity = VELOCITY
			msg.angle = np.deg2rad(-30)
			pub_drive.publish(msg)
		# pub_turnstat.publish(True)



def start_turn_callback(data):
	global FOLLOWING_WALL
	# if we see a gap in either direction ahead
	print('########### LEFT GAP PRESENT: ' + str(data.left))
	print('########### RIGHT GAP PRESENT: ' + str(data.right))
	if (data.left or data.right):
		print("--------------- HI ---------------")
		rospy.Subscriber("check_side", side_check, during_turn_callback)

	# otherwise continue wall following if not already happening
	else:
		if not FOLLOWING_WALL:
			system('roslaunch resistors_wall_following pid_error.py')
			system('roslaunch resistors_wall_following control.py')
			print("Restarting wall following")
			FOLLOWING_WALL = True
	pub_turnstat.publish("False")


if __name__ == '__main__':
	rospy.init_node('drive_control_node', anonymous=True)
	rospy.Subscriber("turn_ahead", turn_ahead, start_turn_callback)
	rospy.Subscriber("file_instructions", instruction, get_direction_callback)
	rospy.spin()
