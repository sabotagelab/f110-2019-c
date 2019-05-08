#!/usr/bin/env python
import rospy
import instruction as instruction
from std_msgs import Bool, String

DIRECTION = None
VELOCITY = None
MSG = instruction()

pub = rospy.Publisher('file_instructions', instruction, queue_size=10)

file = open("instructions.csv", "r")

def convertToMessage(fileLine):
	DIRECTION = fileLine.split(" ")[0]
	VELOCITY = fileLine.split(" ")[1]
	MSG.direction = DIRECTION
	MSG.velocity = VELOCITY

def instruction_callback(data):
	if (data):
		nextLine = file.readline()
		convertToMessage(nextLine)

	pub.publish(MSG)


if __name__ == '__main__':
	rospy.init_node('file_instructions_node', anonymous=True)
	firstLine = file.readline()
	convertToMessage(firstLine)
	rospy.Subscriber("turn_finished", Bool, instruction_callback)
	rospy.spin()