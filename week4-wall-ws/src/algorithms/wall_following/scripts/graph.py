#!/usr/bin/env python
import rospy
from matplotlib import pyplot as plt
import matplotlib.animation as animation
# from wall_following.msg import drive_param
from wall_following.msg import error_analysis
from std_msgs.msg import Float64
import numpy as np

# rad_10 = deg2rad(10)
# rad_20 = deg2rad(20)
# global COUNT, TOTAL, MAX
# COUNT = 0
# TOTAL = 0
# MAX = 0

COUNT = 0
runningAvg = 0
runningTotal = 0
runningMax = 0

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

# pub = rospy.Publisher('wall_following_analysis', error_analysis, queue_size=1)

# Callback for receiving error data on the /pid_error topic
# data: the error from pid_error_node, published as a Float64
def control_callback(data):
	plt.plot([5,6,7,8], [7, 3, 8, 3])

	plt.show()

	COUNT += 1

	runningTotal += data
	runningAvg = runningTotal / COUNT

	if data > runningMax:
		runningMax = data
	
	Xdata = []
	Ydata = []

	Xdata.append(COUNT)
	Ydata.append(data)

	ax1.clear()
	ax1.plot(Xdata, Ydata)
	ani = animation.FuncAnimation(fig, animate, interval=1000)
	plt.show()

	msg = error_analysis

	msg.average = runningAvg
	msg.max = runningMax

	# print('')
	# print('Got Next Error HEY!')
	# print('Current Error: ' + str(data))
	# print('COUNT: ' + str(COUNT))
	# print("TOTAL: " + str(TOTAL))
	# print("MAX: " + str(MAX))
	# print('Published Average: ' + str(msg.average))
	# print('Published Max: ' + str(msg.max))

	# pub.publish(msg)

# Boilerplate code to start this ROS node.
# DO NOT MODIFY!
if __name__ == '__main__':
	rospy.init_node('resistors_analysis', anonymous=True)
	rospy.Subscriber("pid_error", Float64, control_callback)
	rospy.spin()

