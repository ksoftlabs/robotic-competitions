#include <AFMotor.h>

AF_DCMotor leftMotor(3);
AF_DCMotor rightMotor(4);

byte lastSeen = 7;

void drive(int lPower, int rPower) {
  if (lPower > 255) {
    lPower = 255;
  }
  else if (lPower < -255) {
    lPower = -255;
  }
  if (rPower > 255) {
    rPower = 255;
  }
  else if (rPower < -255) {
    rPower = -255;
  }

  if (lPower > 0) {
    leftMotor.run(FORWARD);
  }
  else if (lPower < 0) {
    leftMotor.run(BACKWARD);
  }
  else if (lPower == 0) {
    leftMotor.run(RELEASE);
  }

  if (rPower > 0) {
    rightMotor.run(FORWARD);
  }
  else if (rPower < 0) {
    rightMotor.run(BACKWARD);
  }
  else if (rPower == 0) {
    rightMotor.run(RELEASE);
  }

  leftMotor.setSpeed(abs(lPower));
  rightMotor.setSpeed(abs(rPower));
}

void followLine() {
  pid();
  drive(lSpeed, rSpeed);
}

void brake(int t) {
  drive(0, 0);
  delay(t);
}

void reverse() {
  drive(-180, -180);
}

void turnLeft() {
  brake(500);
drive(-180,180);
  delay(780);
  brake(500);
}

void turnBack() {
  brake(500);
  drive(-180, 180);
  delay(1500);
  brake(500);
}

