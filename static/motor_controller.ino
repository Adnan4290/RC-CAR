#include <Arduino.h>
#include <Wire.h>
#include <RoboClaw.h>

const int upPin = 2;
const int downPin = 3;
const int leftPin = 4;
const int rightPin = 5;
const int leftRoboClawAddress = 0x80;
const int rightRoboClawAddress = 0x81;
const int maxSpeed = 127;

bool controls[5] = {0, 0, 0, 0, 0}; // 0th index for speed, 1-4 for directions

RoboClaw leftRoboClaw(&Serial1);
RoboClaw rightRoboClaw(&Serial2);

void setup() {
  Serial.begin(115200);
  Serial1.begin(38400);
  Serial2.begin(38400);
  
  pinMode(upPin, INPUT);
  pinMode(downPin, INPUT);
  pinMode(leftPin, INPUT);
  pinMode(rightPin, INPUT);
}

void loop() {
  controls[1] = digitalRead(upPin);
  controls[2] = digitalRead(downPin);
  controls[3] = digitalRead(leftPin);
  controls[4] = digitalRead(rightPin);
  controls[0] = analogRead(speedPin);

  int speed = map(controls[0], 0, 1023, 0, maxSpeed);
  int leftSpeed = speed;
  int rightSpeed = speed;

  if (controls[1]) {
    leftSpeed = -maxSpeed;
    rightSpeed = -maxSpeed;
  } else if (controls[2]) {
    leftSpeed = maxSpeed;
    rightSpeed = maxSpeed;
  } else {
    if (controls[3]) {
      leftSpeed = -maxSpeed;
      rightSpeed = maxSpeed;
    } else if (controls[4]) {
      leftSpeed = maxSpeed;
      rightSpeed = -maxSpeed;
    }
  }

  leftRoboClaw.ForwardM1(leftRoboClawAddress, leftSpeed);
  rightRoboClaw.ForwardM2(rightRoboClawAddress, rightSpeed);

  // You can also add code to read encoder values, set PID constants, etc. here
}
