#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;

void setup() {
  Serial.begin(9600);

  servo1.attach(3);   // Servo 1 sur pin 3
  servo2.attach(5);   // Servo 2 sur pin 5
  servo3.attach(4);   // Servo 3 sur pin 4
}

void loop() {
  if (Serial.available()) {
    char incomingChar = Serial.read();

    switch (incomingChar) {
      case '1':
        bougerServo(servo1);
        break;
      case '2':
        bougerServo(servo2);
        break;
      case '3':
        bougerServo(servo3);
        break;
      default:
        break;
    }
  }
}

// Mouvement : 30° -> 120° -> 30°
void bougerServo(Servo& servo) {
  servo.write(120);   // Va à 120°
  delay(300);         

  servo.write(0);    // Retour à 30° (ou 0° si tu préfères)
  delay(300);         
}
