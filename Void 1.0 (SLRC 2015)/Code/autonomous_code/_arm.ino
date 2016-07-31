#define LIFTING_SERVO_MIN 50
#define LIFTING_SERVO_MAX 130
#define HOLDING_SERVO_MIN 55
#define HOLDING_SERVO_MAX 140

void turnServo(Servo servo, int angle) {
  int pos = servo.read();
  if (pos < angle) {
    for (; pos < angle; pos++) {
      servo.write(pos);
      delay(10);
    }
  }
  else {
    for (; pos > angle; pos--) {
      servo.write(pos);
      delay(10);
    }
  }
}

void liftBlock() {
}

void releaseBlock() {
}

