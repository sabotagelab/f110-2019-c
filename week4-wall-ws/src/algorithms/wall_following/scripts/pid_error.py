#!/usr/bin/env python

import rospy
import math
import numpy as np
import yaml
import sys
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64
import pdb
from scipy.cluster.vq import vq, kmeans2, whiten

pub = rospy.Publisher('pid_error', Float64, queue_size=10)

# You can define constants in Python as uppercase global names like these.
MIN_DISTANCE = 0.1
MAX_DISTANCE = 30.0
MIN_ANGLE = -45.0
MAX_ANGLE = 225.0

DES_DISTANCE = 0.5
LOOK_AHEAD = 0.2
ANGLE = .35          # .35 radians = 20 degrees, angle betwen beams a and b


# Convert raw data. Eliminate NaN and inf.
def cleanData(data):
  print("")
  print("JUST GOT LIDAR SCAN")

  ang_inc = data.angle_increment
  print("angle increment: " + str(ang_inc))

  numEntries = len(data.ranges)
  dataArray = np.zeros((numEntries,4), dtype='float')

  for x in range(0, numEntries - 1):
    rangeData = 0
    if np.isnan(data.ranges[x]) or np.isinf(data.ranges[x]):    #   data.ranges[x] == nan:
      rangeData = 5
    else:
      rangeData = data.ranges[x]

    if data.ranges[x] <= 1/1000:
      rangeData = 0
    # 45 Degrees = .7854 Radians = 128 Steps. Puts 0 Degrees at 45 Degrees forward of
    # extreme right beam, per lab instructions
    tmp = np.array([x, x*ang_inc, rangeData], dtype='float')
    dataArray[x][:3] = tmp

  return [dataArray, ang_inc]


# data: single message from topic /scan
# angle: between -45 to 225 degrees, where 0 degrees is directly to the right
# Outputs length in meters to object with angle in lidar scan field of view
def getRange(a_beam, b_beam):
  # TODO: implement
  print('a_beam' + str(a_beam))
  print('b_beam' + str(b_beam))
  a = a_beam[2]
  b = b_beam[2]
  theta = a_beam[3]-b_beam[3]
  num = a*np.cos(theta) - b
  denom = a*np.sin(theta)
  alpha = np.arctan(num/denom)
  d_current = b*np.cos(alpha)
  d_ahead = d_current + LOOK_AHEAD*np.sin(alpha)
  print("d_ahead Distance: " + str(d_ahead))
  return d_ahead


# data: single message from topic /scan
# desired_distance: desired distance to the left wall [meters]
# Outputs the PID error required to make the car follow the left wall.
def followRight(dataArray, desired_distance, ang_inc):
  # TODO: implement

  # 45 Degrees = .7854 Radians = 128 Steps
  dataArray_cut = dataArray[128:,:]
  size_dataArray_cut = len(dataArray_cut)
  for x in range(0,size_dataArray_cut):
    dataArray_cut[x][3] = x*ang_inc
  b_beam = dataArray_cut[0,:]
  # (1 step)/(ang_ing) = steps/rad
  rads_to_steps = round(ANGLE/ang_inc)
  a_beam = dataArray_cut[rads_to_steps,:]

  d_ahead = getRange(a_beam, b_beam)
  error = desired_distance - d_ahead
  print('Error: ' + str(error))
  return error


# data: single message from topic /scan
# desired_distance: desired distance to the right wall [meters]
# Outputs the PID error required to make the car follow the right wall.
def followLeft(dataArray, desired_distance, ang_inc):
  # TODO: implement

  # 45 Degrees = .7854 Radians = 128 Steps
  dataArray_cut = dataArray[:-128,:]
  size_dataArray_cut = len(dataArray_cut)
  for x in range(0, size_dataArray_cut):
    dataArray_cut[x][3] = x*ang_inc
  b_beam = dataArray_cut[-1,:]
  # (1 step)/(ang_ing) = steps/rad
  rads_to_steps = round(ANGLE/ang_inc)
  a_beam_index = size_dataArray_cut - rads_to_steps
  a_beam = dataArray_cut[a_beam_index,:]

  d_ahead = getRange(a_beam, b_beam)
  error = desired_distance - d_ahead
  print('Error: ' + str(error))
  return error

# data: single message from topic /scan
# Outputs the PID error required to make the car drive in the middle
# of the hallway.
def followCenter(dataArray, ang_inc):
  # split data for left and right wall
  dataArray_cut_left = dataArray[:-128,:]
  dataArray_cut_right = dataArray[128:,:]

  # insert raw angle for each data point
  for x in range(0, len(dataArray_cut_left)):
    dataArray_cut_left[x][3] = x*ang_inc

  for x in range(0, len(dataArray_cut_right)):
    dataArray_cut_right[x][3] = x*ang_inc

  # get a and b beam
  b_beam_left = dataArray_cut_left[-1,:]
  b_beam_right = dataArray_cut_right[0,:]

  # (1 step)/(ang_ing) = steps/rad
  rads_to_steps = round(ANGLE/ang_inc)

  a_beam_right = dataArray_cut_right[int(rads_to_steps),:]

  a_beam_index = len(dataArray_cut_left) - rads_to_steps
  a_beam_left = dataArray_cut_left[int(a_beam_index),:]

  # get distances
  d_ahead_right = getRange(a_beam_right, b_beam_right)
  d_ahead_left = getRange(a_beam_left, b_beam_left)

  ideal_center = (d_ahead_left + d_ahead_right) / 2
  actual_path = d_ahead_right - d_ahead_left

  error = ideal_center - actual_path 
  print('Error: ' + str(error))
  return error

# Callback for receiving LIDAR data on the /scan topic.
# data: the LIDAR data, published as a list of distances to the wall.
def scan_callback(data):
  error = 0.0 # TODO: replace with followLeft, followRight, or followCenter

  [dataArray, ang_inc] = cleanData(data)

  # error = followRight(dataArray, DES_DISTANCE, ang_inc)
  #error = followLeft(dataArray, DES_DISTANCE, ang_inc)
  error = followCenter(dataArray, ang_inc)  

  msg = Float64()
  msg.data = error
  pub.publish(msg)

# Boilerplate code to start this ROS node.
# DO NOT MODIFY!
if __name__ == '__main__':
	rospy.init_node('pid_error_node', anonymous = True)
	rospy.Subscriber("scan", LaserScan, scan_callback)
	rospy.spin()
