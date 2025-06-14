const int enPin = 8;
const int stepPin = 3;  // stepYPin
const int dirPin = 6;   // dirYPin

const int stepsPerRev = 200;
int pulseWidthMicros = 100;    // microseconds
int microsBtwnSteps = 1000;    // microseconds

void setup() {
  Serial.begin(9600);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);  // Enable motor
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  Serial.println(F("CNC Shield Initialized"));
  digitalWrite(dirPin, HIGH); // Sens horaire (fixe)
}

void loop() {
  // Rotation continue dans le sens horaire
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(pulseWidthMicros);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(microsBtwnSteps);
}
