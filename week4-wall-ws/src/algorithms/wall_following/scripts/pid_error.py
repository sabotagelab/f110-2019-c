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
LOOK_AHEAD = 1
DES_DISTANCE = 1.19
LOOK_AHEAD = 0.05
THETA = .35          # .35 rad = 20 deg: Angle betwen beams a and b
MIN_THETA = 0.09     # (.09 rad = 5 deg) Minimum theta required to get a "good" wall distance calculation
CENTER_TO_START = 1.48  # 1.571 rad = 90 deg: From car center, starts looking this much to the side
ANG_INC = 0   # Value that will store rad/beam_increment for this LiDAR
RIGHT_WALL = 1   # 1: Can See Right Wall     0: Can't See Right Wall
LEFT_WALL = 1   # 1: Can See Left Wall     0: Can't See Left Wall


# Convert raw LiDAR data. Eliminate NaN and inf.
# dataArray stores [Beam Number, Beam Angle, Corrected Range]
def cleanData(data):
  global ANG_INC
  print("")
  print("***** JUST GOT LIDAR SCAN *****")

  # Get Various Information About LiDAR
  ANG_INC = data.angle_increment     # Radians Between 2 Beam
  numEntries = len(data.ranges)      # Total Number of Beams from LiDAR
  mid_beam = (numEntries-1)/2        # Beam at Car's Centerline, (numEntries-1) because last entry is a dud
  print ('Number of LiDAR Beams: ' + str(numEntries))
  print ('Center Beam (mid_beam): ' + str(mid_beam))

  # dataArray will store final data [Beam Number, Angle, Corrected Range]
  # Subtract one from numEntries because we throw out the very last beam (is dud beam)
  dataArray = np.zeros((numEntries-1,3), dtype='float')

  for x in range(0, numEntries - 1):
    rangeData = 0
    if np.isnan(data.ranges[x]) or np.isinf(data.ranges[x]):
      rangeData = 5     # Sets NaN and Inf to Max Range
    else:
      rangeData = data.ranges[x]   # Stores Actual Range
    if data.ranges[x] <= 1/1000:
      rangeData = 0     # Sets Low Values to Zero
    tmp = np.array([x, x*ANG_INC, rangeData], dtype='float')
    dataArray[x][:3] = tmp     # Stores [Beam Number, Beam Angle, Corrected Range] into dataArray
  return [dataArray, mid_beam]


# Sometimes a_beam range is 5. Since this is not the actual wall locataion, it
# ruins the wall distance calculation. In this function, if a_beam range is 5,
# it finds a LiDAR beam with range <5 to use.
def checkBeam(a_beam, b_beam, direction, dataArray):
  global RIGHT_WALL, LEFT_WALL
  proceed = True     # Flag to say when search is exhausted, so stop the while loop
  min_theta_steps = round(MIN_THETA/ANG_INC)  # Establishes min theta needed for accurate calculation
  print('Checking Beams on the ' + str(direction) + ' Starting From ' + str(a_beam[0]))
  print(str(a_beam))
  beam_index = int(a_beam[0])     # The while search loop uses this as the counter

  # Do while loop until the range is <5 OR we have searched up to the min_theta_steps value
  while (a_beam[2] >= 5) and (proceed):
    # This if loop continues until the updated a_beam value reaches either +- from the b_beam value
    if (a_beam[0] != b_beam[0]+min_theta_steps) and (a_beam[0] != b_beam[0]-min_theta_steps):
      if direction == 'Right':
        beam_index -= 1    # Right side, thus a_beam counts down to b_beam
        RIGHT_WALL = 1
      elif direction == 'Left':
        beam_index += 1    # Left side, thus a_beam counts up to b_beam
        LEFT_WALL = 1
      else:
        print('ERROR: Bad Direction Value Passed to checkBeam')   # Catch-All Error
      a_beam = dataArray[beam_index]    # Provides next a_beam to check
      print(str(a_beam))
    else:
      if direction == 'Right':
        print('REACHED ' + str(round(np.rad2deg(MIN_THETA))) + ' DEGREES ('+ str(min_theta_steps) + ' steps) FROM B_BEAM (' + str(b_beam[0]) +')')
        print('CANT SEE RIGHT WALL')
        RIGHT_WALL = 0
      elif direction == 'Left':
        print('REACHED ' + str(round(np.rad2deg(MIN_THETA))) + ' DEGREES ('+ str(min_theta_steps) + ' steps) FROM B_BEAM (' + str(b_beam[0]) +')')
        print('CANT SEE LEFT WALL')
        LEFT_WALL = 0
      proceed = False    # Failed to see one of the walls. Set flag that ends the while loop search
  return a_beam          # Return updated a_beam that has gone though this check

# In: Data from the 2 beams you will calculate from
# Output: Distance [meters] To Wall accounting for Look Ahead Distance
def getRange(a_beam, b_beam, direction):
  a = a_beam[2]                   # Beam Distances
  b = b_beam[2]
  theta = a_beam[1]-b_beam[1]     # Angle Between Beams
  num = a*np.cos(theta) - b
  denom = a*np.sin(theta)
  alpha = np.arctan(num/denom)    # Angle of Car
  d_current = b*np.cos(alpha)     # Current Distance to Wall
  d_ahead = d_current + LOOK_AHEAD*np.sin(alpha)

  print(direction + ' Current Distance: ' + str(d_current))
  print(direction + ' Ahead Distance: ' + str(d_ahead))

  return d_ahead


# In: cleaned LiDAR data, radians between each LiDAR beam, and the car's center (forward) beam
# Out: error to the right wall. This will be used by the PD controller.
def followRight(dataArray, mid_beam):
  start_beam = int(mid_beam - round(CENTER_TO_START/ANG_INC))   # Find right beam you want to start from
  steps_to_THETA = round(THETA/ANG_INC)    # (radians)/(radians/step) = Steps to get to THETA
  end_beam = int(start_beam + steps_to_THETA)   # Find right beam you want to end at
  a_beam = dataArray[end_beam]             # Pull out end (a) beam data
  b_beam = dataArray[start_beam]           # Pull out start (b) beam data
  a_beam = checkBeam(a_beam, b_beam, 'Right', dataArray)   # Check that a_beam is usable
  print('Beams Going Into Calculations')
  print('a_beam: ' + str(a_beam))
  print('b_beam: ' + str(b_beam))
  d_ahead = getRange(a_beam, b_beam, 'Right')       # Calculate Look Ahead Distance using a/b beams

  # If We Saw the Right Wall
  if (RIGHT_WALL == 1):
    print('SEE RIGHT WALL, GO TO DES_DISTANCE')
    error = DES_DISTANCE - d_ahead     # Calculate error for PD controller    
  # If We Didn't See the Right Wall
  elif (RIGHT_WALL != 1):
    print('CANT SEE RIGHT WALL, TURN HARD RIGHT')
    error = -0.8  # Arbitrary Error to get Hard Right Turn

  print ('DES_DISTANCE: ' + str(DES_DISTANCE))
  print('Error: ' + str(error))

  return error


# In: cleaned LiDAR data, radians between each LiDAR beam, and the car's center (forward) beam
# Out: error to the right wall. This will be used by the PD controller.
def followLeft(dataArray, mid_beam):
  start_beam = int(mid_beam + round(CENTER_TO_START/ANG_INC))   # Find left beam you want to start from
  steps_to_THETA = round(THETA/ANG_INC)    # (radians)/(radians/step) = Steps to get to THETA
  end_beam = int(start_beam - steps_to_THETA)   # Find left beam you want to end at
  a_beam = dataArray[end_beam]             # Pull out end (a) beam data
  b_beam = dataArray[start_beam]           # Pull out start (b) beam data
  a_beam = checkBeam(a_beam, b_beam, 'Left', dataArray)   # Check that a_beam is usable
  print('Beams Going Into Calculations')
  print('a_beam: ' + str(a_beam))
  print('b_beam: ' + str(b_beam))
  d_ahead = getRange(a_beam, b_beam, 'Left')       # Calculate Look Ahead Distance using a/b beams
  
  # If We Saw the Left Wall
  if (LEFT_WALL == 1):
    print('SEE LEFT WALL, GO TO DES_DISTANCE')
    error = d_ahead - DES_DISTANCE           # Calculate error for PD controller   
  # If We Didn't See the Left Wall
  elif (LEFT_WALL != 1):
    print('CANT SEE LEFT WALL, TURN HARD LEFT')
    error = 0.8  # Arbitrary Error to get Hard Left Turn

  print ('DES_DISTANCE: ' + str(DES_DISTANCE))
  print('Error: ' + str(error))

  return error


# In: cleaned LiDAR data, radians between each LiDAR beam, and the car's center (forward) beam
# Out: error to the hallway's center. This will be used by the PD controller.
def followCenter(dataArray, mid_beam):
  global DES_DISTANCE

  start_beam_left = int(mid_beam + round(CENTER_TO_START/ANG_INC))   # Find Left Beam Index to start at
  start_beam_right = int(mid_beam - round(CENTER_TO_START/ANG_INC))   # Find Right Beam Index to start at
  steps_to_THETA = round(THETA/ANG_INC)    # (radians)/(radians/step) = Steps to get to THETA
  end_beam_left = int(start_beam_left - steps_to_THETA)   # Find Left Beam Index to end at
  end_beam_right = int(start_beam_right + steps_to_THETA)   # Find Right Beam Index to end at
  a_beam_left = dataArray[end_beam_left]             # Get Data from Left Beams
  b_beam_left = dataArray[start_beam_left]
  a_beam_left = checkBeam(a_beam_left, b_beam_left, 'Left', dataArray)   # Check that a_beam is usable
  a_beam_right = dataArray[end_beam_right]           # Get Data from Right Beams
  b_beam_right = dataArray[start_beam_right]
  a_beam_right = checkBeam(a_beam_right, b_beam_right, 'Right', dataArray)   # Check that a_beam is usable
  
  print('Beams Going Into Calculations')
  print('a_beam_left: ' + str(a_beam_left))
  print('b_beam_left: ' + str(b_beam_left))
  print('a_beam_right: ' + str(a_beam_right))
  print('b_beam_right: ' + str(b_beam_right))

  d_ahead_left = getRange(a_beam_left, b_beam_left, 'Left')       # Calculate Look Ahead Distance using a/b beams
  d_ahead_right = getRange(a_beam_right, b_beam_right, 'Right')

  # If We Saw Both Walls
  if (RIGHT_WALL == 1) and (LEFT_WALL == 1):
    print('SEE BOTH WALLS, GO TO CENTER')
    center = (d_ahead_left + d_ahead_right) / 2
    DES_DISTANCE = center    # If we lose a wall later, the car will drive this distance from the visible wall

    # Error calculations based on car's position
    if d_ahead_right > d_ahead_left:
      print('Car is Left of Center')
      error = d_ahead_left - center
    elif d_ahead_right < d_ahead_left:
      print('Car is Right of Center')
      error = center - d_ahead_right
    else:
      print('Car is at Center')
      error = 0
    
  # If we only saw the left wall
  elif (RIGHT_WALL == 0) and (LEFT_WALL == 1):
    print('IGNORING RIGHT WALL DISTANCE')
    error = d_ahead_left - DES_DISTANCE
    
  # If we only saw the right wall
  elif (RIGHT_WALL == 1) and (LEFT_WALL == 0):
    print('IGNORING LEFT WALL DISTANCE')
    error = DES_DISTANCE - d_ahead_right
    
  # If we saw no walls
  else:
    print('CANT SEE ANY RIGHT OR LEFT WALLS')
    error = 0     # Makes car go forward. In future, may want it to go slow as well

  print ('Center and DES_DISTANCE: ' + str(DES_DISTANCE))
  print('Error: ' + str(error))

  return error




# Callback for receiving LIDAR data on the /scan topic.
# data: the LIDAR data, published as a list of distances to the wall.
def scan_callback(data):
  [dataArray, mid_beam] = cleanData(data)     # Get rid of NaN and Inf

  # CHOOSE ONE OF THE THREE WALL FOLLOWING ALGORITHMS:
  # error = followRight(dataArray, mid_beam)
  error = followLeft(dataArray, mid_beam)
  # error = followCenter(dataArray, mid_beam)

  msg = Float64()
  msg.data = error
  pub.publish(msg)

# Boilerplate code to start this ROS node.
# DO NOT MODIFY!
if __name__ == '__main__':
	rospy.init_node('pid_error_node', anonymous = True)
	rospy.Subscriber("scan", LaserScan, scan_callback)
	rospy.spin()
