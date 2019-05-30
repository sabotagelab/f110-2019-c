#!/usr/bin/env python
import rospy
import csv
from file_instructions.msg import instruction
from geometry_msgs.msg import PoseStamped, Pose, Quaternion, Point
from std_msgs.msg import Float64, Header
from tf.transformations import euler_from_quaternion, quaternion_from_euler

csv.register_dialect('myDialect',quoting=csv.QUOTE_ALL,skipinitialspace=True)

def waypoint_callback(data):
	print("WAYPOINT: ")
	
	x_pos = data.pose.position.x 
	y_pos = data.pose.position.y
	quaternion = (
    		data.pose.orientation.x,
    		data.pose.orientation.y,
    		data.pose.orientation.z,
    		data.pose.orientation.w)
	euler = euler_from_quaternion(quaternion)
	yaw = euler[2]

	data_list = []
	data_list.append(x_pos)
	data_list.append(y_pos)
	data_list.append(yaw)
	print(data_list)
	
	with open('waypoints.csv', 'a') as writeFile:
                writer = csv.writer(writeFile)
		writer.writerow(data_list)
	writeFile.close()	


if __name__ == '__main__':
	rospy.init_node('waypoint_saver_node', anonymous=True)
	rospy.Subscriber("pf/viz/inferred_pose", PoseStamped, waypoint_callback)
	rospy.spin()
	
