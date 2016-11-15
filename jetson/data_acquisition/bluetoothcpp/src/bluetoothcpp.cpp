/*
 * Copyright (c) 2010, Willow Garage, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the Willow Garage, Inc. nor the names of its
 *       contributors may be used to endorse or promote products derived from
 *       this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 * Parts Copyright (c) 2016, JetsonHacks
 *
 * Parts 2016, Matthew Kleinsmith; MIT License
 */

#include <iostream>
#include <cstdlib>

#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/Joy.h>
#include "boost/thread/mutex.hpp"
#include "boost/thread/thread.hpp"
#include "ros/console.h"


class JetsonCarTeleop
{
public:
  JetsonCarTeleop();

private:
  void talker(serial bluetooth, file cmdLog, file cmdErr);
  void publish();

  ros::NodeHandle ph_, nh_;
  ros::Publisher vel_pub_;
  geometry_msgs::Twist last_published_;
  boost::mutex publish_mutex_;
  ros::Timer timer_;
};

JetsonCarTeleop::JetsonCarTeleop():
{
  vel_pub_ = ph_.advertise<geometry_msgs::Twist>("cmd_vel", 1, true);
  timer_ = nh_.createTimer(ros::Duration(0.1), boost::bind(&JetsonCarTeleop::publish, this));
}

void sleepok(int t, ros::NodeHandle &nh)
{
   if (nh.ok())
     sleep(t);
}

void JetsonCarTeleop::talker(serial bluetooth, file cmdLog, file cmdErr)
{ 
    geometry_msgs::Twist vel;
    vel.angular.z = 50 // steering
    vel.linear.x = 61 // throttle
    last_published_ = vel;
}

void JetsonCarTeleop::publish()
{
  boost::mutex::scoped_lock lock(publish_mutex_);
  vel_pub_.publish(last_published_);
}

int main(int argc, char** argv)
{
  ros::init(argc, argv, "jetsoncar_teleop");
  ros::NodeHandle nh;

  JetsonCarTeleop jetsoncar_teleop;
  ros::spin();
}
