#include <Servo.h>

Servo myServo;
int pos = 90;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);
  myServo.write(pos);
}

void loop() {
  if (Serial.available() > 0) {
    String gesture = Serial.readStringUntil('\n');
    gesture.trim();

    if (gesture == "ROCK") pos = 0;
    else if (gesture == "PAPER") pos = 90;
    else if (gesture == "SCISSORS") pos = 180;

    myServo.write(pos);
  }
}
