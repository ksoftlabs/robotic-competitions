#include <Servo.h>

char junk;
String inputString = "";
int const s = 180;
int const t = 100;


// Declare classes for Servo connectors of the MotorShield.
Servo servo_1;
Servo servo_2;

void setup()
{
  Serial.begin(9600);
  Serial1.begin(9600);
  
  pinMode(52, OUTPUT);

  servo_1.attach(10);
  servo_2.attach(9);
  
  digitalWrite(52, HIGH);
}


void loop()
{
  if (Serial1.available()) {
    while (Serial1.available()) {
      char inChar = (char)Serial1.read(); //read the input
      inputString += inChar;        //make a string of the characters coming on serial
    }
    Serial1.println(inputString);
    while (Serial1.available() > 0) {
      junk = Serial1.read();
    }      // clear the serial buffer
    if (inputString == "f") {       //in case of 'a' turn the LED on
      drive(s,s,s,s);

      delay(t);
    }
    if (inputString == "b") {
      drive(-s,-s,-s,-s);
      delay(t);
    }
    if (inputString == "r") {
      drive(s,s,-s,-s);
      delay(t);
    }
    if (inputString == "l") {
      drive(-s,-s,s,s);
      delay(t);
    }
    if (inputString == "u") {
      int l = 0;
      while (l < 90) {
        servo_1.write(l);
        delay(25);
        l++;
      }
    }
    if (inputString == "d") {
      int k = 90;
      while (k <= 90 && k != 0) {
        servo_1.write(k);
        delay(25);
        k--;
      }
    }
    if (inputString == "c") {
      servo_2.write(120);
      delay(1000);
    }
    if (inputString == "e") {
      servo_2.write(55);
      delay(1000);
    }
    inputString = "";
    if (inputString == "") {
      drive(0,0,0,0);
    }
    if (inputString == "c") {
      servo_1.write(120);
    }
    if (inputString == "e") {
      servo_1.write(55);
    }
  }
}


