#include <AFMotor.h>

AF_DCMotor leftForwardMotor(3);
AF_DCMotor leftBackwardMotor(1);
AF_DCMotor rightForwardMotor(4);
AF_DCMotor rightBackwardMotor(2);

byte lastSeen = 7;

void drive(int lFPower, int lBPower, int rFPower, int rBPower) {
  if (lFPower > 0) {
    leftForwardMotor.run(FORWARD);
  }
  else if (lFPower < 0) {
    leftForwardMotor.run(BACKWARD);
  }
  else if (lFPower == 0) {
    leftForwardMotor.run(RELEASE);
  }

  if (lBPower > 0) {
    leftBackwardMotor.run(FORWARD);
  }
  else if (lBPower < 0) {
    leftBackwardMotor.run(BACKWARD);
  }
  else if (lBPower == 0) {
    leftBackwardMotor.run(RELEASE);
  }

  if (rFPower > 0) {
    rightForwardMotor.run(FORWARD);
  }
  else if (rFPower < 0) {
    rightForwardMotor.run(BACKWARD);
  }
  else if (rFPower == 0) {
    rightForwardMotor.run(RELEASE);
  }

  if (rBPower > 0) {
    rightBackwardMotor.run(FORWARD);
  }
  else if (rBPower < 0) {
    rightBackwardMotor.run(BACKWARD);
  }
  else if (rBPower == 0) {
    rightBackwardMotor.run(RELEASE);
  }

  leftForwardMotor.setSpeed(abs(lFPower));
  leftBackwardMotor.setSpeed(abs(lBPower));
  rightForwardMotor.setSpeed(abs(rFPower));
  rightBackwardMotor.setSpeed(abs(rBPower));
}
