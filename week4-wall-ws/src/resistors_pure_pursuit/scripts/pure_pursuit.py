#!/usr/bin/env python

import rospy
from race.msg import drive_param
from geometry_msgs.msg import PoseStamped
# from geometry_msgs.msg import PoseStamped, Pose
import math
import numpy as np
from numpy import linalg as LA
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from visualization_msgs.msg import Marker
import csv
import os


#############
# CONSTANTS #
#############

LOOKAHEAD_DISTANCE = 1.5 # meters
VELOCITY = 0.5 # m/s

###########
# GLOBALS #
###########

global car_position, startup_flag
car_position = [0,0]
startup_flag = 1;       # Flag so that first time in callback, it searches ALL waypoints to find closest

# Import waypoints.csv into a list
# path_points are [x, y, theta]
dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, '/home/nvidia/f110-2019-c/week4-wall-ws/src/resistors_pure_pursuit/waypoints/waypoints_one_curve.csv')
with open(filename) as f:
    path_points = [tuple(line) for line in csv.reader(f)]

# Turn path_points into a list of floats to eliminate the need for casts in the code below.
#path_points = [(float(point[0]+7.564), float(point[1]-9.147), float(point[2])) for point in path_points]
path_points = [(float(point[0]), float(point[1]), float(point[2])) for point in path_points]
#path_points = [path_points[0] +7.564, path_points[1]-9.147]
        
# Publisher for 'drive_parameters' (speed and steering angle)
pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)

# Publish Markers
pub_goal_world = rospy.Publisher('waypoint_goal_world', Marker, queue_size=1)
pub_goal_car = rospy.Publisher('waypoint_goal_car', Marker, queue_size=1)
pub_car_yaw = rospy.Publisher('car_yaw', Marker, queue_size=1)
pub_car_angle = rospy.Publisher('car_angle', Marker, queue_size=1)
pub_gamma = rospy.Publisher('car_gamma', Marker, queue_size=1)
pub_beta = rospy.Publisher('car_beta', Marker, queue_size=1)



# Publisher for '/initialpose' (y,x)
#pub_initialpose = rospy.Publisher('initialpose', Pose, queue_size=1)
#init_pose.position = [10, 10, 0];
#init_pose.orientation = [0, 0, 0, 1];
#pub.publish(init_pose)

#############
# FUNCTIONS #
#############
    
# Computes the Euclidean distance between two 2D points p1 and p2.
def dist(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def make_marker(mark, closest_coordinates):
	mark.header.frame_id = "/map"
        #print(str(closest_coordinates))
	mark.pose.position.x = closest_coordinates[0]
	mark.pose.position.y = closest_coordinates[1]
	mark.pose.position.z = 0 # or set this to 0
	mark.type = mark.SPHERE
	mark.scale.x = .5 # If marker is too small in Rviz can make it bigger here
	mark.scale.y = .5
	mark.scale.z = .5
	mark.color.a = 1.0
	mark.color.r = 1.0
	mark.color.g = 0.0
	mark.color.b = 0.0

	return mark


# Input data is PoseStamped message from topic /pf/viz/inferred_pose.
# Runs pure pursuit and publishes velocity and steering angle.
def callback(data):
    global car_position, startup_flag, closest_index, shortest_dis, num_path_points
    print('')
    print('JUST GOT POSE UPDATE')

    # Get Car's Current Position
    car_position[0] = data.pose.position.x
    car_position[1] = data.pose.position.y
    print('Car Location: ' + str(car_position))


    # If this is first time in callback, must search ALL waypoints to find closest
    if startup_flag == 1:
        startup_flag = 0;
        num_path_points = len(path_points)   # How many waypoints are there to search?
        shortest_dis = 50000;       # Arbitrarily Large
        closest_index = num_path_points +10;   # Artibtrarily Large
        for i in range(0,num_path_points):
            dist_temp = dist(car_position,[path_points[i][0], path_points[i][1]])   # Find Car to Waypoint Distance
            if dist_temp < shortest_dis:
                # If you found a new shortest waypoint distance
                shortest_dis = dist_temp;
                closest_index = i;
    
    print('Shortest Point: ' + str(closest_index) + '   Shortest Dis: ' + str(shortest_dis))


    # Note: These following numbered steps below are taken from R. Craig Coulter's paper on pure pursuit.

    # 1. Determine the current location of the vehicle (we are subscribed to vesc/odom)
    # Hint: Read up on PoseStamped message type in ROS to determine how to extract x, y, and yaw.


    quaternion = (
    data.pose.orientation.x,
    data.pose.orientation.y,
    data.pose.orientation.z,
    data.pose.orientation.w)

    euler = euler_from_quaternion(quaternion)
    # roll = euler[0]
    # pitch = euler[1]
    yaw = euler[2]

    print('Yaw is: ' + str(yaw))


    # 2. Find the path point closest to the vehicle that is >= 1 lookahead distance from vehicle's current location.
    # print('path_points: ' + str(path_points))

    closest_coordinates = [path_points[closest_index][0], path_points[closest_index][1]]
    closest_dis = dist(car_position, closest_coordinates)

    print('Closest Point: ' + str(closest_coordinates) + '   Closest Dis: ' + str(closest_dis))


    # Find Waypoint that is Right at the LOOKAHEAD_DISTANCE
    while closest_dis <= LOOKAHEAD_DISTANCE:
        closest_index = closest_index + 1;     # If inside LOOKAHEAD, increment to next waypoint
        if closest_index >= num_path_points:
            closest_index = 0;        # Reset to 0 when you get to the last waypoint
        closest_dis = dist(car_position, [path_points[closest_index][0], path_points[closest_index][1]])  # Find distance to that next waypoint
    # closest_index = closest_index - 1;     # Current index is ouside of LOOKAHEAD_DISTANCE, so step one back

    # Recalculate Coordinates and Distance with New Waypoint
    closest_coordinates = [path_points[closest_index][0], path_points[closest_index][1]]
    closest_dis = dist(car_position, closest_coordinates)
    print('Waypoint at Lookahead Distance: Index(' + str(closest_index) + ')   Dis(' + str(closest_dis)+')')

    print('Ready to Publish World Goal')
    #temp = raw_input()
    world_goal = Marker()
    world_goal = make_marker(world_goal, closest_coordinates);
    pub_goal_world.publish(world_goal);




    # 3. Transform the goal point to vehicle coordinates.
    print('Ready to Transform World Goal to Car Goal')
    #temp = raw_input
    x = car_position[0];
    y = car_position[1];
    a = path_points[closest_index][0];
    b = path_points[closest_index][1];
    num = b-y;
    den = a-x;
    print('b-y = ' + str(num))
    print('a-x = ' + str(den))


    # ERROR IN MANUAL: They mix up beta and gamma. I swapped the two in these equations.
    gamma = np.arctan(num/den);
    beta = (np.pi)/2 - yaw - gamma;
    x_car2goal = closest_dis*np.cos(beta)
    y_car2goal = closest_dis*np.sin(beta)
    #x_car2goal = 10
    #y_car2goal = 0


    print('Ready to Publish Car Goal')
    #temp = raw_input()
    marker_goal = Marker()
    marker_goal = make_marker(marker_goal, [x_car2goal, y_car2goal]);
    marker_goal.type = marker_goal.CUBE
    marker_goal.color.b = 1.0
    marker_goal.header.frame_id = "/laser"
    pub_goal_car.publish(marker_goal)

    print('Car  X,Y: ' + str(x) + '   '+str(y))
    print('Goal X,Y: ' + str(a) + '   '+str(b))
    print('Beta: ' + str(beta))
    print('Gamma: ' + str(gamma))
    print('C2G  X,Y: ' + str(x_car2goal) + '   '+str(y_car2goal))


    # 4. Calculate the curvature = 1/r = 2x/l^2
    # The curvature is transformed into steering wheel angle by the vehicle on board controller.
    # Hint: You may need to flip to negative because for the VESC a right steering angle has a negative value.
    #curvature = (2*x_car2goal)/(100);
    curvature = (2*x_car2goal)/(closest_dis*closest_dis);
    angle = curvature;

    # Convert all Radians to Degrees for Display
    yaw_deg = np.rad2deg(yaw)
    angle_deg = np.rad2deg(angle)
    gamma_deg = np.rad2deg(gamma)
    beta_deg = np.rad2deg(beta)

    #### Yaw of Car (Yaw) ##########
    marker_yaw = Marker()
    marker_yaw_location = [1, 3]
    marker_yaw = make_marker(marker_yaw, marker_yaw_location);
    marker_yaw.type = marker_yaw.TEXT_VIEW_FACING
    marker_yaw.text = 'Car Yaw: ' + str(np.round(yaw_deg, decimals = 2))
    pub_car_yaw.publish(marker_yaw)

    #### Drive Command (Theta) #####
    marker_angle = Marker()
    marker_angle_location = [1, 3.5]
    marker_angle = make_marker(marker_angle, marker_angle_location);
    marker_angle.type = marker_angle.TEXT_VIEW_FACING
    marker_angle.text = 'Drive Cmd (Angle): ' + str(np.round(angle_deg, decimals = 4))
    pub_car_angle.publish(marker_angle)

    #### Map Origin to Goal Point (Gamma) #####
    marker_gamma = Marker()
    marker_gamma_location = [1, 4]
    marker_gamma = make_marker(marker_gamma, marker_gamma_location);
    marker_gamma.type = marker_angle.TEXT_VIEW_FACING
    marker_gamma.text = 'Map to Goal (Gamma): ' + str(np.round(gamma_deg, decimals = 4))
    pub_gamma.publish(marker_gamma)

    #### Car Origin to Goal Point (Beta) #####
    marker_beta = Marker()
    marker_beta_location = [1, 4.5]
    marker_beta = make_marker(marker_beta, marker_beta_location);
    marker_beta.type = marker_beta.TEXT_VIEW_FACING
    marker_beta.text = 'Car to Goal (Beta): ' + str(np.round(beta_deg, decimals = 4))
    pub_beta.publish(marker_beta)




    # print(data)
    # angle = 0
    angle = np.clip(angle, -0.4189, 0.4189) # 0.4189 radians = 24 degrees because car can only turn 24 degrees max

    msg = drive_param()
    msg.velocity = VELOCITY
    msg.angle = angle
    pub.publish(msg)
    
if __name__ == '__main__':
    rospy.init_node('pure_pursuit')
    rospy.Subscriber('/pf/viz/inferred_pose', PoseStamped, callback, queue_size=1)
    rospy.spin()

