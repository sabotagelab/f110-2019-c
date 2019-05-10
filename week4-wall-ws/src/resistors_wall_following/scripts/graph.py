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
runningAvg = 0.00
runningTotal = 0.00
runningMax = 0.00

# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

# plt.show()

pub = rospy.Publisher('wall_following_analysis', error_analysis, queue_size=1)

# Callback for receiving error data on the /pid_error topic
# data: the error from pid_error_node, published as a Float64
def control_callback(data):
	global COUNT
	global runningAvg
	global runningTotal
	global runningMax

	COUNT += 1

	runningTotal += data.data
	runningAvg = runningTotal / COUNT

	if abs(data.data) > runningMax:
		runningMax = abs(data.data)

	print("\n\n\n\n\n\n\n")
	print(str(runningMax) + "\n" +  str(runningAvg))
	print("\n\n\n\n\n\n\n")

	
	Xdata = []
	Ydata = []

	Xdata.append(COUNT)
	Ydata.append(data)

	# ax1.clear()
	# ax1.plot(Xdata, Ydata)
	# ani = animation.FuncAnimation(fig, animate, interval=1000)
	# plt.show()

	msg = error_analysis()

	msg.average = runningAvg
	msg.max = runningMax

	pub.publish(msg)

	if COUNT > 100:
		COUNT = 0
		runningTotal = 0.00

# Boilerplate code to start this ROS node.
# DO NOT MODIFY!
if __name__ == '__main__':
	rospy.init_node('resistors_analysis', anonymous=True)
	rospy.Subscriber("pid_error", Float64, control_callback)
	rospy.spin()

