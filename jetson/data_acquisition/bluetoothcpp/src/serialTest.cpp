#include <iostream>
#include <cstdlib>
#include <fstream>

#include "boost/thread/mutex.hpp"
#include "boost/thread/thread.hpp"

#include "split.h"

#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include "ros/console.h"


class BluetoothNode
{
    public:
        BluetoothNode();
    private:
        ros::NodeHandle ph_, nh_;

        void talker(std::string msg);
        geometry_msgs::Twist last_published_;

        void publish();
        ros::Publisher vel_pub_;
        ros::Timer timer_;
        boost::mutex publish_mutex_;
};

BluetoothNode::BluetoothNode():
    ph_("~")
{
    vel_pub_ = ph_.advertise<geometry_msgs::Twist>("commands", 1, true);
    timer_ = nh_.createTimer(ros::Duration(0.1), boost::bind(&BluetoothNode::publish, this));
}

void sleepok(int t, ros::NodeHandle &nh)
{
    if (nh.ok())
        sleep(t);
}

typedef std::vector<std::string> StringVector;
geometry_msgs::Twist createTwistMsg(std::string msg) {
    geometry_msgs::Twist twist;
    StringVector elems = split(msg, DELIM);
    StringVector::const_iterator i = elems.begin();
    twist.linear.x = *i;
    ++i;
    twist.angular.z =  *i;
    return twist;
}

void BluetoothNode::talker(std::string msg)
{
    std::fstream android = setupBluetoothStream();
    std::string msg;
    const char DELIM = ',';
    const int MSG_LEN = 32;
    while (true) {
        android >> msg;
        if (sizeof msg == MSG_LEN) {
            last_published_ = createTwistMsg(msg);
        }
    }
}

void BluetoothNode::publish() {
    boost::mutex::scoped_lock lock(publish_mutex_);
    vel_pub_.publish(last_published_);
}

fstream setupBluetoothStream() {
    system("./setupRFCOMMport.sh");
    const char* bluetooth = std::getenv("bluetooth");
    std::fstream android;
    android.open(bluetooth);
    return android; 
}

int main(int argc, char** argv) {
    ros::init(argc, argv, "bluetoothNode");
    ros::NodeHandle nh;
    BluetoothNode bluetoothNode;
    bluetoothNode.talker();
}
