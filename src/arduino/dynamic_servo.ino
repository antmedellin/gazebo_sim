#include <Servo.h>

Servo myServo;  // Create a servo object
int servoPin = 9;  // Pin connected to the servo signal wire
int angle = 0;     // Variable to store the servo position

void setup() {
  myServo.attach(servoPin);  // Attach the servo to pin 9
  Serial.begin(9600);        // Start serial communication
  Serial.println("Enter angle (0 to 180):");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');  // Read user input
    angle = input.toInt();  // Convert input to integer

    // Validate angle range
    if (angle >= 0 && angle <= 180) {
      myServo.write(angle);  // Move servo to the specified angle
      Serial.print("Moved to: ");
      Serial.println(angle);
    } else {
      Serial.println("Invalid angle. Enter a value between 0 and 180.");
    }
  }
}