#!/usr/bin/env python
import rospy
from file_instructions.msg import instruction
from std_msgs.msg import Bool, String

global DIRECTION
global VELOCITY
DIRECTION = "straight"
VELOCITY = 0

pub = rospy.Publisher('file_instructions', instruction, queue_size=10)
file = open("/home/nvidia/f110-2019-c/week4-wall-ws/src/file_instructions/scripts/instructions.csv", 'r+')

def instruction_callback(data):
	global DIRECTION, VELOCITY
	print("DATA FROM TURN FINISHED: " + str(data))
	data_string = str(data)
	size = len(data_string)
	print('Size of data: ' + str(size))
	if (size == 12):
		print("READING FROM FILE OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
		msg = instruction()
		nextLine = file.readline()
		print(nextLine)
		DIRECTION = nextLine.split(" ")[0]
		VELOCITY = nextLine.split(" ")[1]
		VELOCITY = VELOCITY[:-1]
		msg.direction = DIRECTION
		msg.velocity = float(VELOCITY)
		print(msg.velocity)
		print(msg.direction)
		#MSG = msg
		pub.publish(msg)
	else:
		print("In instction callback when false")
		msg = instruction()
		msg.direction = DIRECTION
		msg.velocity = float(VELOCITY)
		pub.publish(msg)


if __name__ == '__main__':
	rospy.init_node('file_instructions_node', anonymous=True)
	print("^^^^^^^^^^^^^^ READING FROM FILE ^^^^^^^^^^^^^^^^^")
	# firstLine = file.readline()
	# DIRECTION = firstLine.split(" ")[0]
	# VELOCITY = firstLine.split(" ")[1]
	# VELOCITY = VELOCITY[:-2]
	# MSG.direction = DIRECTION
	# MSG.velocity = VELOCITY
	rospy.Subscriber("turn_finished", String, instruction_callback)
	rospy.spin()
