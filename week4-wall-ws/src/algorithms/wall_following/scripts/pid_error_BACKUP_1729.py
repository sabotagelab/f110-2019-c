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
DES_DISTANCE = 0.4
LOOK_AHEAD = 0.05
THETA = .35          # .35 rad = 20 deg: Angle betwen beams a and b
CENTER_TO_START = 1.48  # 1.571 rad = 90 deg: From car center, starts looking this much to the side


# Convert raw LiDAR data. Eliminate NaN and inf.
# dataArray stores [Beam Number, Beam Angle, Corrected Range]
def cleanData(data):
  print("")
  print("JUST GOT LIDAR SCAN")

  # Get Various Information About LiDAR
  ang_inc = data.angle_increment     # Radians Between 2 Beam
  numEntries = len(data.ranges)      # Total Number of Beams from LiDAR
  mid_beam = (numEntries-1)/2        # Beam at Car's Centerline, (numEntries-1) because last entry is a dud
  print ('ang_inc: ' + str(ang_inc))
  print ('Num LiDar Readings: ' + str(numEntries))
  print ('mid_beam: ' + str(mid_beam))

  # Stores Final Data [Beam Number, Angle, Corrected Range]
  # Subtract one from numEntries because we throw out the very last beam (is dud beam)
  dataArray = np.zeros((numEntries-1,3), dtype='float')

  for x in range(0, numEntries - 1):
    rangeData = 0
    if np.isnan(data.ranges[x]) or np.isinf(data.ranges[x]):
      rangeData = 5     # Sets NaN and Inf to Max Range
    else:
      rangeData = data.ranges[x]
    if data.ranges[x] <= 1/1000:
      rangeData = 0
    tmp = np.array([x, x*ang_inc, rangeData], dtype='float')
    dataArray[x][:3] = tmp     # Stores [Beam Number, Beam Angle, Corrected Range] into dataArray
  return [dataArray, ang_inc, mid_beam]


# In: Data from the 2 beams you will calculate from
# Output: Distance [meters] To Wall accounting for Look Ahead Distance
def getRange(a_beam, b_beam):
  a = a_beam[2]                   # Beam Distances
  b = b_beam[2]
  theta = a_beam[1]-b_beam[1]     # Angle Between Beams
  num = a*np.cos(theta) - b
  denom = a*np.sin(theta)
  alpha = np.arctan(num/denom)    # Angle of Car
  d_current = b*np.cos(alpha)     # Current Distance to Wall
  d_ahead = d_current + LOOK_AHEAD*np.sin(alpha)

  print('theta: ' + str(theta))
  print('alpha: ' + str(alpha))
  print('alpha in degrees: ' + str(alpha*57.296))
  print("d_current Distance: " + str(d_current))
  print("d_ahead Distance: " + str(d_ahead))

  return d_ahead


# In: cleaned LiDAR data, radians between each LiDAR beam, and the car's center (forward) beam
# Out: error to the right wall. This will be used by the PD controller.
def followRight(dataArray, ang_inc, mid_beam):
  start_beam = int(mid_beam - round(CENTER_TO_START/ang_inc))   # Find right beam you want to start from
  steps_to_THETA = round(THETA/ang_inc)    # (radians)/(radians/step) = Steps to get to THETA
  end_beam = int(start_beam + steps_to_THETA)   # Find right beam you want to end at
  a_beam = dataArray[end_beam]             # Pull out end (a) beam data
  b_beam = dataArray[start_beam]           # Pull out start (b) beam data
  d_ahead = getRange(a_beam, b_beam)       # Calculate Look Ahead Distance using a/b beams
  error = DES_DISTANCE - d_ahead     # Calculate error for PD controller

  print('dataArray: ' + str(dataArray))
  print ('start_beam: ' + str(start_beam))
  print ('end_beam: ' + str(end_beam))
  print('Right Start Beam (b_beam): ' + str(dataArray[start_beam]))
  print('THETA Ahead Beam (a_beam)' + str(dataArray[end_beam]))
  print('Error: ' + str(error))

  return error


# In: cleaned LiDAR data, radians between each LiDAR beam, and the car's center (forward) beam
# Out: error to the right wall. This will be used by the PD controller.
def followLeft(dataArray, ang_inc, mid_beam):
  start_beam = int(mid_beam + round(CENTER_TO_START/ang_inc))   # Find left beam you want to start from
  steps_to_THETA = round(THETA/ang_inc)    # (radians)/(radians/step) = Steps to get to THETA
  end_beam = int(start_beam - steps_to_THETA)   # Find left beam you want to end at
  a_beam = dataArray[end_beam]             # Pull out end (a) beam data
  b_beam = dataArray[start_beam]           # Pull out start (b) beam data
  d_ahead = getRange(a_beam, b_beam)       # Calculate Look Ahead Distance using a/b beams
  # This error calculation is opposite from followRight. This flips the sign to match with followRight.
  error = d_ahead - DES_DISTANCE           # Calculate error for PD controller

  print('dataArray: ' + str(dataArray))
  print ('start_beam: ' + str(start_beam))
  print ('end_beam: ' + str(end_beam))
  print('Right Start Beam (b_beam): ' + str(dataArray[start_beam]))
  print('THETA Ahead Beam (a_beam)' + str(dataArray[end_beam]))
  print('Error: ' + str(error))

  return error


# In: cleaned LiDAR data, radians between each LiDAR beam, and the car's center (forward) beam
# Out: error to the hallway's center. This will be used by the PD controller.
def followCenter(dataArray, ang_inc, mid_beam):
  start_beam = int(mid_beam + round(CENTER_TO_START/ang_inc))   # Find left beam you want to start from
  steps_to_THETA = round(THETA/ang_inc)    # (radians)/(radians/step) = Steps to get to THETA
  end_beam_left = int(start_beam - steps_to_THETA)   # Find left beam you want to end at
  end_beam_right = int(start_beam + steps_to_THETA)   # Find right beam you want to end at
  a_beam_left = dataArray[end_beam_left]             # Pull out end (a) beam data
  a_beam_right = dataArray[end_beam_right]
  b_beam = dataArray[start_beam]           # Pull out start (b) beam data
  d_ahead_left = getRange(a_beam_left, b_beam)       # Calculate Look Ahead Distance using a/b beams
  d_ahead_right = getRange(a_beam_right, b_beam)
  # This error calculation is opposite from followRight. This flips the sign to match with followRight.
  center = (d_ahead_left + d_ahead_right) / 2
  error = center - (d_ahead_right - d_ahead_left)           # Calculate error for PD controller

  print('dataArray: ' + str(dataArray))
  print ('start_beam: ' + str(start_beam))
  print ('end_beam_right: ' + str(end_beam_right))
  print('Right Start Beam (b_beam): ' + str(dataArray[start_beam]))
  print('THETA Ahead Beam (a_beam)' + str(dataArray[end_beam_right]))
  print('Error: ' + str(error))

  return error

  """ # split data for left and right wall
  dataArray_cut_left = dataArray[:-128,:]
  dataArray_cut_right = dataArray[128:,:]

  # insert raw angle for each data point
  for x in range(0, len(dataArray_cut_left)):
    dataArray_cut_left[x][2] = x*ang_inc

  for x in range(0, len(dataArray_cut_right)):
    dataArray_cut_right[x][2] = x*ang_inc

  # get a and b beam
  b_beam_left = dataArray_cut_left[-1,:]
  b_beam_right = dataArray_cut_right[0,:]

  # (1 step)/(ang_ing) = steps/rad
  rads_to_steps = round(THETA/ang_inc)

  a_beam_right = dataArray_cut_right[int(rads_to_steps),:]

  a_beam_index = len(dataArray_cut_left) - rads_to_steps
  a_beam_left = dataArray_cut_left[int(a_beam_index),:]

  # get distances
  d_ahead_right = getRange(a_beam_right, b_beam_right)
  d_ahead_left = getRange(a_beam_left, b_beam_left)

  ideal_center = (d_ahead_left + d_ahead_right) / 2
  print('IDEAL CENTER:' + str(ideal_center))
  actual_path = d_ahead_right - d_ahead_left
  print('ACTUAL PATH:' + str(actual_path))

  error = ideal_center - actual_path 
  print('Error: ' + str(error))
  return error """


# Callback for receiving LIDAR data on the /scan topic.
# data: the LIDAR data, published as a list of distances to the wall.
def scan_callback(data):
  [dataArray, ang_inc, mid_beam] = cleanData(data)     # Get rid of NaN and Inf

  # CHOOSE ONE OF THE THREE WALL FOLLOWING ALGORITHMS:
<<<<<<< HEAD
  # error = followRight(dataArray, ang_inc, mid_beam)
  error = followLeft(dataArray, ang_inc, mid_beam)
=======
  error = followRight(dataArray, ang_inc, mid_beam)
  #error = followLeft(dataArray, ang_inc, mid_beam)
>>>>>>> b44cbbe35b5b8ce52e02a9cb5c5420931153814b
  # error = followCenter(dataArray, ang_inc, mid_beam)

  msg = Float64()
  msg.data = error
  pub.publish(msg)

# Boilerplate code to start this ROS node.
# DO NOT MODIFY!
if __name__ == '__main__':
	rospy.init_node('pid_error_node', anonymous = True)
	rospy.Subscriber("scan", LaserScan, scan_callback)
	rospy.spin()
