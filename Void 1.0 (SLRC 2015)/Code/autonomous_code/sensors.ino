#include <NewPing.h>

#define TRIGGER_PIN_FORWARD 53
#define ECHO_PIN_FORWARD 51
#define MAX_DISTANCE_FORWARD 200
NewPing forward_sonar(TRIGGER_PIN_FORWARD, ECHO_PIN_FORWARD, MAX_DISTANCE_FORWARD);

#define TRIGGER_PIN_DEPTH 50
#define ECHO_PIN_DEPTH 52
#define MAX_DEPTH 200
NewPing depth_sonar(TRIGGER_PIN_DEPTH, ECHO_PIN_DEPTH, MAX_DEPTH);

double getDistance() {
  delay(50);
  return forward_sonar.ping_cm();
}

double getDepth() {
  delay(50);
  return depth_sonar.ping_cm();
}

void readIRSensors() {
  s1 = digitalRead(IR1);
  s2 = digitalRead(IR2);
  s3 = digitalRead(IR3);
  s4 = digitalRead(IR4);
  s5 = digitalRead(IR5);
  s6 = digitalRead(IR6);
  s7 = digitalRead(IR7);
  s8 = digitalRead(IR8);
  s9 = digitalRead(IR9);
  s10 = digitalRead(IR10);
  s11 = digitalRead(IR11);
  s12 = digitalRead(IR12);
  s13 = digitalRead(IR13);
}
