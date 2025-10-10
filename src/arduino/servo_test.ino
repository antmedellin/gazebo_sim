#include <Servo.h>

Servo myServo;

// Define the servo pin
const int servoPin = 9;
// Define the angles
const int forwardAngle = 0;
const int backwardAngle = 180;
// Time to wait in milliseconds
const unsigned long interval = 5000;

void setup() {
  myServo.attach(servoPin);
  myServo.write(forwardAngle);
}

void loop() {
  myServo.write(forwardAngle);
  delay(interval);
  myServo.write(backwardAngle);
  delay(interval);
}
