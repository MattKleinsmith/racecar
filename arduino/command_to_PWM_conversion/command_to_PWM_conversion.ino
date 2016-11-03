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

#include <Servo.h>

// input limits
const double MIN_INPUT = 0; // From serial port (original source is the Android, with the Jetson as an intermediate node)
const double MAX_INPUT = 100;
// output limits
const double MIN_THROTTLE = 0;
const double MAX_THROTTLE = 150;
const double MIN_STEERING = 30; // 60?(25 in)
const double MAX_STEERING = 150; // 132? (85 in)  // Arduino Uno (not micro) and not a fully charged battery
// neutral values
const double NEUTRAL_THROTTLE = 91;
const double NEUTRAL_STEERING = 90;
// Dealing with ASCII bytes
const int OFFSET = '0';
const int COMMA = 44 - OFFSET;
const int NEWLINE = 10 - OFFSET;
const int COMMAND_LEN = 3;
// Initializations
Servo eSpeedControl;  // The ESC on the TRAXXAS works like a Servo
Servo steeringServo;
double throttle;
double steering;

void setup() {
  eSpeedControl.attach(10);
  eSpeedControl.write(NEUTRAL_THROTTLE);
  steeringServo.attach(11);
  steeringServo.write(NEUTRAL_STEERING);
  Serial.begin(115200);
}

void loop() {
  throttle = getCommand(COMMA, COMMAND_LEN, MIN_THROTTLE, MAX_THROTTLE, NEUTRAL_THROTTLE);
  steering = getCommand(NEWLINE, COMMAND_LEN, MIN_STEERING, MAX_STEERING, NEUTRAL_STEERING);
  eSpeedControl.write(throttle);
  steeringServo.write(steering);
  printCommands(throttle, steering); // for debugging
  delay(1);
}

////////////////////////////////////////////////////////////////////////////////
double getCommand(int delim, int len, double min_out, double max_out, double neutral) {
  double command;
  int commandBytes[len];
  int commandIndex = 0;
  int newByte = 0;
  while (newByte != delim) {
    if (Serial.available() > 0) {
      newByte = Serial.read() - OFFSET;
      if (newByte >= 0 && newByte <= 9) {
        commandBytes[commandIndex] = newByte;
        commandIndex += 1;
      }
    }
  }
  if (commandIndex != 3) {
    stopCar("Error: Invalid command. Stopping car.");
    return neutral;
  }
  printArray(commandBytes, len); // for debugging
  command = catint(commandBytes, len); // turns {1,2,3} into 123
  command = scaleCommand(command, MIN_INPUT, MAX_INPUT, min_out, max_out);
  command = enforceBounds(command, min_out, max_out, neutral); // stops the car if out of bounds
  Serial.println(command); // for debugging
  return command;
}

// turns {1,2,3} into 123
double catint(int array[], int len) {
  int i = 0;
  double k = 0;
  for (i = 0; i < len; i++) {
    k = 10 * k + array[i];
  }
  return k;
}

// stops the car if out of bounds
double enforceBounds(double command, double lowerBound, double upperBound, double neutral) {
  if (command < lowerBound || command > upperBound) {
    stopCar("Error: Command out of bounds. Stopping car.");
    command = neutral;
  }
  return command;
}

// stretches or compresses an interval to fit another; think of stretching or compressing a line segment
// Certain Android UI limitations determined the input interval. Arduino servos determined the output interval.
double scaleCommand (double command, double min_in, double max_in, double min_out, double max_out) {
  return (command - min_in) * (max_out - min_out) / (max_in - min_in) + min_out;
}

////////////////////////////////////////////////////////////////////////////////
// safety
void stopCar(char *errorMsg) {
    eSpeedControl.write(NEUTRAL_THROTTLE);
    Serial.println(errorMsg);
}

////////////////////////////////////////////////////////////////////////////////

// debug tools
void printArray(int array[], int len) {
  int i;
  for (i = 0; i < len; i++) {
    Serial.print(array[i]);
    Serial.print(",");
    Serial.println(i);
  }
}

void printCommands(double throttle, double steering){
  Serial.print("Throttle: ");
  Serial.println(throttle);
  Serial.print("Steering: ");
  Serial.println(steering);
  Serial.println();
}


