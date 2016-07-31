int baseSpeed = 150;
double P = 0.0, I = 0.0, D = 0.0;
float kP = 60.0, kI = 0.45, kD = 125.0;
float error = 0.0, preError = 0.0;
float turn;

void pid() {
  preError = error;    //Previous error
  if ((s5 + s6 + s7 + s8 + s9) != 0) {
    error = ((s5 * 1.0) + (s6 * 2.0) + (s7 * 3.0) + (s8 * 4.0) + (s9 * 5.0)) / (s5 + s6 + s7 + s8 + s9);    //Current error
    error -= 3;
  }
  else {
    return;
  }

  P = kP * error;
  if (error == 0.0) {
    I = 0.0;
  }
  I = (I + error) * kI;
  D = (error - preError) * kD;
  turn = P + I + D;
  lSpeed = baseSpeed + turn;
  rSpeed = baseSpeed - turn;

  if (lSpeed < 110) {
    lSpeed -= 220;
  }
  if (rSpeed < 110) {
    rSpeed -= 220;
  }
}


