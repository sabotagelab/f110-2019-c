#include "ros/ros.h"
#include "std_msgs/String.h"
#include "geometry_msgs/Twist.h"
#include <sstream>
#include <algorithm>

double arr [10] = {0,0,0,0,0,0,0,0,0,0};
int count = 1;

ros::Publisher average_velocity_pub;

void chatterCallback(const geometry_msgs::Twist vel)
{
	double sum = 0;
	double temp = 0;
	int i;
	arr[0] = vel.linear.x;

	for(i = 0; i < 10; i++)
	{
		sum += arr[i];
	}

	ROS_INFO("\n\nEntering CallBack!");

	std_msgs::String msg;

	std::stringstream ss;
	if(count < 11)
	{
		ss << sum/count;
	}
	else
	{
		ss << (sum/10);
	}
	msg.data = ss.str();

	ROS_INFO("Avg: [%s]", msg.data.c_str());

	average_velocity_pub.publish(msg);

	std::rotate(arr, arr + 1, arr + 10);

	count++;
}

int main(int argc, char **argv)
{
	ROS_INFO("Starting!");

	ros::init(argc, argv, "torres_average");

	ros::NodeHandle n;
	
	average_velocity_pub = n.advertise<std_msgs::String>("average_velocity", 50);

	ros::Rate loop_rate(5);

	ros::Subscriber sub = n.subscribe("turtle1/cmd_vel", 10, chatterCallback);

	ros::spin();

	return 0;
}
