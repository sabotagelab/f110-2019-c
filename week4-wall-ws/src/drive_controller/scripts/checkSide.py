#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Bool, String
from sensor_msgs.msg import LaserScan
from drive_controller.msg import side_check

CENTER_TO_START = 1.48
THETA = .35 
pub = rospy.Publisher('check_side', side_check, queue_size=10)

# Convert raw LiDAR data. Eliminate NaN and inf.
# dataArray stores [Beam Number, Beam Angle, Corrected Range]
def cleanData(data):
  # Get Various Information About LiDAR
  ang_inc = data.angle_increment     # Radians Between 2 Beam
  numEntries = len(data.ranges)      # Total Number of Beams from LiDAR
  mid_beam = (numEntries-1)/2        # Beam at Car's Centerline, (numEntries-1) because last entry is a dud
  
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

def check_callback(data):
  #get both side beams (range)
  [dataArray, ang_inc, mid_beam] = cleanData(data)
  msg = side_check()
  # ang_inc = data.angle_increment
  # numEntries = len(data.ranges)
  # mid_beam = (numEntries-1)/2 
  start_beam_right = int(mid_beam - round(CENTER_TO_START/ang_inc))   # Find left beam you want to start from
  start_beam_left = int(mid_beam + round(CENTER_TO_START/ang_inc)) 
  steps_to_THETA = round(THETA/ang_inc)    # (radians)/(radians/step) = Steps to get to THETA
  # end_beam_left = int(start_beam - steps_to_THETA)   # Find left beam you want to end at
  # end_beam_right = int(start_beam + steps_to_THETA)   # Find right beam you want to end at
  left_side = dataArray[start_beam_left]             # Pull out end (a) beam data
  right_side = dataArray[start_beam_right]

  print('TESTING LEFT SIDE :::::::::::::::: ' + str(left_side))

  print('TESTING RIGHT SIDE :::::::::::::::: ' + str(right_side))

  if left_side[2] > 2 and right_side[2] < 2:
    msg.left = True
    msg.right = False
    print("LEFT SIDE GAP")
  
  if right_side[2] > 2 and left_side[2] < 2:
    msg.right = True
    msg.left = False
    print("RIGHT SIDE GAP")

  if left_side[2] > 2 and right_side[2] > 2:
    msg.left = True
    msg.right = True
    print("LEFT AND RIGHT SIDE GAP")
    	
  else:
    msg.left = False
    msg.right = False

  pub.publish(msg)
	
if __name__ == '__main__':
	rospy.init_node('check_side_node', anonymous=True)
	rospy.Subscriber("scan", LaserScan, check_callback)
	rospy.spin()