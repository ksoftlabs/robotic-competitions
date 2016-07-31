#include <Servo.h>

//Line following sensors
#define IR1 22
#define IR2 24
#define IR3 26
#define IR4 28
#define IR5 30
#define IR6 32
#define IR7 34
#define IR8 36
#define IR9 38
#define IR10 40
#define IR11 42
#define IR12 44
#define IR13 46

//[--------------s13-------------]
//[-------s10----s11----s12------]
//[s5-----s6-----s7-----s8-----s9]
//[-------s2-----s3-----s4-------]
//[--------------s1--------------]
int s1 = 0, s2 = 0, s3 = 0, s4 = 0, s5 = 0, s6 = 0, s7 = 0, s8 = 0, s9 = 0, s10 = 0, s11 = 0, s12 = 0, s13 = 0;

//Servo motors
Servo holdingServo;
Servo liftingServo;

int lSpeed = 0, rSpeed = 0;

String state = "";

void setup() {
  Serial.begin(9600);

  liftingServo.attach(10);    //Servo 1(0 to 180)
  holdingServo.attach(9);     //Servo 2(55 to 145)

  pinMode(IR1, INPUT);
  pinMode(IR2, INPUT);
  pinMode(IR3, INPUT);
  pinMode(IR4, INPUT);
  pinMode(IR5, INPUT);
  pinMode(IR6, INPUT);
  pinMode(IR7, INPUT);
  pinMode(IR8, INPUT);
  pinMode(IR9, INPUT);
  pinMode(IR10, INPUT);
  pinMode(IR11, INPUT);
  pinMode(IR12, INPUT);
  pinMode(IR13, INPUT);
}

void loop() {
  dryRun();
}
