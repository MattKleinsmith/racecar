/*
  License of original code:
    Arduino ROS node for JetsonCar project
    The Arduino controls a TRAXXAS Rally Car
    MIT License
    JetsonHacks (2016)
  Link to original code:
    https://github.com/jetsonhacks/installJetsonCar/blob/master/Arduino%20Firmware/jetsoncar/jetsoncar.ino
  License of this code:
    MIT License
    Matthew Kleinsmith (2016)
*/

#include <Servo.h>

// These are general bounds for the steering servo and the
// TRAXXAS Electronic Speed Controller (ESC)
const double minThrottle = 0;
const double neutralThrottle = 91;
const double maxThrottle = 150;
const double minSteering = 30; // 60?(25 in)
const double neutralSteering = 90;
const double maxSteering = 150; // 132? (85 in)  // Arduino Uno (not micro) and not a fully charged battery
// Test 1:
  // Board: Arduino Uno, many years old
  // Battery: Not fully charged (did two or three laps around the block with it beforehand)
  // Throttle:
    // Min: I don't even want to test this.
    // Neutral: [59, 63] ([88.5, 94.5])// 64 didn't, but then it did. Maybe the battery's charge changed the neutral range?
          // 64 didn't trigger, then it did, and then it didn't again. And then it did again. 64 is unstable.
    // Max: I don't even want to test this.
  // Steering:
    // Min: 25 (60 out)
    // Neutral: 50 (90 out)
    // Max: 85 (132 out)
// Important question: How does the charge of the battery affect the map from commands to actions?
    
// Dealing with ASCII bytes
const int OFFSET = '0';
const int COMMA = 44 - OFFSET;
const int NEWLINE = 10 - OFFSET;
const int MAXLEN = 3;

Servo eSpeedControl;  // The ESC on the TRAXXAS works like a Servo
Servo steeringServo;

int newByte = 0;
double throttle;
double steering;

void setup() {
  eSpeedControl.attach(10);
  eSpeedControl.write(neutralThrottle);
  steeringServo.attach(11);
  steeringServo.write(neutralSteering);
  Serial.begin(115200);
}

void loop() {
  throttle = getCommand(COMMA, MAXLEN, newByte, 0);
  steering = getCommand(NEWLINE, MAXLEN, newByte, 1);
  eSpeedControl.write(throttle);
  steeringServo.write(steering);
  printlog(throttle, steering); // for debugging
  delay(1);
}

//////////////////////////////////////////////////////////////////
double getCommand(int delim, int len, int newByte, int kind) {
  // @param kind: 0 means throttle; 1 means steering
  int commandBytes[len];
  memset(commandBytes, -1, sizeof commandBytes);
  int commandIndex = 0;
  while (newByte != delim) {
    if (Serial.available() > 0) {
      newByte = Serial.read() - OFFSET;
      if (newByte >= 0 && newByte <= 9) {
        commandBytes[commandIndex] = newByte;
        commandIndex += 1;
      }
    }
  }
  printarray(commandBytes, len); // for debugging
  double command = catint(commandBytes, len);
  Serial.println(command); // for debugging
  return cleanCommand(command, kind);
}

// turns {1,2,3} into 123
double catint(int array[], int len) {
  int i = 0;
  double k = 0;
  for (i = 0; i < len; i++) {
    if (array[i] != -1) { k = 10 * k + array[i];}
  }
  return k;
}

// normalize and keep within the interval
double cleanCommand(double command, int kind) {
  if (kind == 0) {
      command = normalizeCommand(command, 0, 100, minThrottle, maxThrottle);
      Serial.println(command); // for debugging
      if (command < minThrottle) {
        command = minThrottle;
      }
      if (command > maxThrottle) {
        command = maxThrottle;
      }
  }
  else {
      command = normalizeCommand(command, 0, 100, minSteering, maxSteering);
      Serial.println(command); // for debugging
      if (command < minSteering) {
        command = minSteering;
      }
      if (command > maxSteering) {
        command = maxSteering;
      }
  }
  Serial.println(command); // for debugging
  return command;
}

// stretches or compresses an interval to fit another; think of stretching or compressing a line segment
double normalizeCommand (double command, double in_min, double in_max, double out_min, double out_max) {
  return (command - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
//////////////////////////////////////////////////////////////////

//debug tool
void printarray(int array[], int len) {
  int i;
  for (i = 0; i < len; i++) {
    Serial.print(array[i]);
    Serial.print(",");
    Serial.println(i);
  }
}

void printlog(double throttle, double steering){
  Serial.print("Throttle: ");
  Serial.println(throttle);
  Serial.print("Steering: ");
  Serial.println(steering);
  Serial.println();
}

