// Written by Michaela Buchanan on 04/07/19

#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Float32.h"
#include "geometry_msgs/Twist.h"

// created class for storing data and functionality of average and to make getting data from callback easier
class Average
{
	float average = 0;
	
	public:
	void averageCallBack(const geometry_msgs::Twist& msg);
	void setAverage(float newAverage);
	float getAverage();	
};

// setter for Average class
void Average::setAverage(float newAverage)
{
	average = newAverage;
}

// getter for Average class
float Average::getAverage()
{
	return average;
}

// called every time you spin (ie get a new data point)
// data type for vertical velocity is geometry_msgs:Twist
void Average::averageCallBack(const geometry_msgs::Twist& msg)
{
	double av = msg.linear.x;
	float newAv = (float) av;
	this->setAverage(newAv);	
	ROS_INFO("Current X Velocity: [%f]", msg.linear.x);
}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "buchanan_average");

	ros::NodeHandle n;
	
	// initiate Average class
	Average average;
	
	//create subscriber and publisher
	ros::Subscriber sub = n.subscribe("/turtle1/cmd_vel", 1000, &Average::averageCallBack, &average);
	ros::Publisher pub = n.advertise<std_msgs::Float32>("average_velocity", 1000);

	// sets publish rate at 5Hz
	ros::Rate loop_rate(5);

	while(ros::ok())
	{
		float runningSum = 0;
				
		// get and create sum of next ten data points
		for (int i = 0; i < 10; i++)
		{
			ros::spinOnce();
			runningSum += average.getAverage();
		}

		// calculate and publish average of ten data points
		float cycles = 10.0;
		std_msgs::Float32 averageOfTen;
		averageOfTen.data = runningSum / cycles;
		ROS_INFO("Average of past 10 data points: [%f]", averageOfTen.data);
		pub.publish(averageOfTen);

		// reset average 
		average.setAverage(0);

		// sleep for achieving 5 Hz update
		loop_rate.sleep();
	}

	return 0;
}




