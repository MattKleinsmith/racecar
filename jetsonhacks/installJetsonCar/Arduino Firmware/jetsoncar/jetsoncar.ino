/*
  Arduino ROS node for JetsonCar project
  The Arduino controls a TRAXXAS Rally Car
  MIT License
  JetsonHacks (2016)
*/

#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include <WProgram.h>
#endif

#include <Servo.h> 
#define USB_USBCON
#include <ros.h>
#include <std_msgs/UInt16.h>
#include <std_msgs/String.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Empty.h>
#include <geometry_msgs/Twist.h>

ros::NodeHandle nodeHandle;
// These are general bounds for the steering servo and the
// TRAXXAS Electronic Speed Controller (ESC)
const int MIN_THROTTLE_OUTPUT = 0;
const int MAX_THROTTLE_OUTPUT = 150;
const int MIN_STEERING_OUTPUT = 1083;//60;
const int MAX_STEERING_OUTPUT = 1958;//132;
const int BAUDRATE = 115200;
const int MIN_THROTTLE_INPUT = 0;
const int MAX_THROTTLE_INPUT = 100;
const int MIN_STEERING_INPUT = 0;
const int MAX_STEERING_INPUT = 600;
const int NEUTRAL_THROTTLE = 91;
const int NEUTRAL_STEERING = 1500; // TODO: Find true neutral.
const int LED = 13;
const int SETUP_DELAY = 1000;
const int SPIN_DELAY = 1;
const int STEERING_PIN = 9;
const int THROTTLE_PIN = 11;
const char *DEBUGGING_TOPIC = "/chatter";
const char *COMMANDS_TOPIC = "/bluetoothNode/commands";

Servo steeringServo;
Servo electronicSpeedController; // The ESC on the TRAXXAS works like a Servo

std_msgs::Int32 str_msg;
ros::Publisher chatter(DEBUGGING_TOPIC, &str_msg); 

// Arduino 'map' funtion for floating point
double fmap (double toMap, double in_min, double in_max, double out_min, double out_max) {
  return (toMap - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void driveCallback ( const geometry_msgs::Twist&  twistMsg )
{
  
  int steeringAngle = fmap(twistMsg.angular.z, MIN_STEERING_INPUT, MAX_STEERING_INPUT, MIN_STEERING_OUTPUT, MAX_STEERING_OUTPUT);
  // The following could be useful for debugging
  int title = -1;
  str_msg.data = title;
  chatter.publish(&str_msg);
  str_msg.data = steeringAngle;
  chatter.publish(&str_msg);
  // Check to make sure steeringAngle is within car range
  if (steeringAngle < MIN_STEERING_OUTPUT) { 
    steeringAngle = MIN_STEERING_OUTPUT;
  }
  if (steeringAngle > MAX_STEERING_OUTPUT) {
    steeringAngle = MAX_STEERING_OUTPUT;
  }
  steeringServo.writeMicroseconds(steeringAngle);
  
  int escCommand = fmap(twistMsg.linear.x, MIN_THROTTLE_INPUT, MAX_THROTTLE_INPUT, MIN_THROTTLE_OUTPUT, MAX_THROTTLE_OUTPUT);
  // Check to make sure throttle command is within bounds
  if (escCommand < MIN_THROTTLE_OUTPUT || escCommand > MAX_THROTTLE_OUTPUT) { 
    escCommand = NEUTRAL_THROTTLE; // Stop the car.
  }
  // The following could be useful for debugging
  int title2 = -2;
  str_msg.data = title2;
  chatter.publish(&str_msg);
  str_msg.data = escCommand;
  chatter.publish(&str_msg);
  
  electronicSpeedController.write(escCommand);
  digitalWrite(LED, HIGH-digitalRead(LED));  //toggle led  
 
}

ros::Subscriber<geometry_msgs::Twist> driveSubscriber(COMMANDS_TOPIC, &driveCallback);

void setup(){
  pinMode(LED, OUTPUT);
  Serial.begin(BAUDRATE);
  nodeHandle.initNode();
  // This can be useful for debugging purposes
  nodeHandle.advertise(chatter);
  // Subscribe to the steering and throttle messages
  nodeHandle.subscribe(driveSubscriber);
  // Attach the servos to actual pins
  steeringServo.attach(STEERING_PIN);
  electronicSpeedController.attach(THROTTLE_PIN);
  // Initialize Steering and ESC setting
  // Steering centered is 90, throttle at neutral is 90
  steeringServo.write(NEUTRAL_STEERING);
  electronicSpeedController.write(NEUTRAL_THROTTLE);
  delay(SETUP_DELAY);
  
}

void loop(){
  nodeHandle.spinOnce();
  delay(SPIN_DELAY); // Remove this to get to new messages faster?
}
