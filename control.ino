#include <Servo.h>

// Define the servo objects
Servo servo1;  // Servo for controlling the grabber
Servo servo2;  // Additional servo for grabber if needed

// Define ultrasonic sensor pins
const int trigPin = 9;  // Trigger pin of ultrasonic sensor
const int echoPin = 10; // Echo pin of ultrasonic sensor

void setup() {
  // Attach servo motors to pins
  servo1.attach(6);  // Attach servo1 to pin 6
  servo2.attach(7);  // Attach servo2 to pin 7

  // Initialize serial communication for debugging
  Serial.begin(9600);

  // Set ultrasonic sensor pins as OUTPUT and INPUT
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Control the robot grabber
  controlGrabber();

  // Read ultrasonic sensor and print distance
  readUltrasonicSensor();
  
  // Delay for stability
  delay(100);
}

void controlGrabber() {
  // Move servo1 to open and close the grabber
  servo1.write(0);  // Adjust angles as needed (0 is closed, 90 is open)
  delay(1000);      // Wait for the grabber to close
  servo1.write(90);
  delay(1000);      // Wait for the grabber to open

  // Additional control for servo2 if needed
  // servo2.write(angle);  // Adjust angle as needed
  // delay(1000);
}

void readUltrasonicSensor() {
  // Trigger ultrasonic sensor to get distance
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure the time it takes for the ultrasonic pulse to return
  long duration = pulseIn(echoPin, HIGH);

  // Calculate distance in centimeters (speed of sound is approximately 343 m/s)
  float distance_cm = duration * 0.034 / 2;

  // Print the distance to the Serial Monitor
  Serial.print("Distance: ");
  Serial.print(distance_cm);
  Serial.println(" cm");
}
