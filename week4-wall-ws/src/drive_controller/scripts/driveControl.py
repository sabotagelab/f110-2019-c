#!/usr/bin/env python
import rospy
import instruction as instruction
from std_msgs import Bool, String
from sensor_msgs.msg import LaserScan
from drive_control.msg import side_check

# 1.571 rad = 90 deg:
pub_drive = rospy.Publisher('drive_parameters', drive_param, queue_size=10)
pub_turnstat = rospy.Publisher('turn_finished', bool, queue_size=10)

FOLLOWING_WALL = True
TURNING_DIRECTION = None
VELOCITY = 0

def get_direction_callback(data):
	TURNING_DIRECTION = data.direction
	VELOCITY = data.velocity


def during_turn_callback(data):
	# stop wall following
	system('rosnode kill wall_following')
	print("Entering cornering mode")
	FOLLOWING_WALL = False
	msg = drive_control()

	# wait for turn to be right next to the car
	while(!data.left and !data.right):
		msg.velocity = VELOCITY
		msg.angle = 0
		pub_drive.Publish(msg)
		print("Waiting for turn...")

	# if direction says to go straight
	if (TURNING_DIRECTION == "straight"):
		while(data.left or data.right):
			print("Going straight")

		# publish that we finished the "turn" so we get next direction
		pub_turnstat.Publish(True)

	elif (TURNING_DIRECTION == "left"):
		while(data.left):
			msg.velocity = VELOCITY
			msg.angle = -15
			pub_drive.Publish(msg)
		pub_turnstat.Publish(True)

	elif (TURNING_DIRECTION == "right"):
		while(data.right):
			msg.velocity = VELOCITY
			msg.angle = 15
			pub_drive.Publish(msg)
		pub_turnstat.Publish(True)



def start_turn_callback(data):
	# if we see a gap in either direction ahead
	if (data):
		rospy.Subscriber("file_instructions", instruction, check_direction_callback)
		rospy.Subscriber("check_side", side_check, during_turn_callback)

	# otherwise continue wall following if not already happening
	else:
		if !(FOLLOWING_WALL)
			system('roslaunch wall_following wall_following.py')
			print("Restarting wall following")
			FOLLOWING_WALL = True


if __name__ == '__main__':
	rospy.init_node('drive_control_node', anonymous=True)
	rospy.Subscriber("turn_ahead", Bool, start_turn_callback)
	rospy.spin()
