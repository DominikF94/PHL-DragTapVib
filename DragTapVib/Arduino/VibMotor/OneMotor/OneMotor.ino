const int motorPin1 = 5;

const int motorPin2 = 2;
const int led =13;
const int motorPin3 = 3;
const int motorPin4 = 13;
const int motorPin5 = 12;

void setup()
{
  pinMode(led, OUTPUT);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  pinMode(motorPin5, OUTPUT);
}

void loop()
{
digitalWrite(motorPin1, HIGH);
digitalWrite(motorPin2, HIGH);
digitalWrite(motorPin3, HIGH);
digitalWrite(motorPin4, HIGH);
digitalWrite(motorPin5, HIGH);
delay(1000);
digitalWrite(led, LOW);
digitalWrite(motorPin1, LOW);
digitalWrite(motorPin2, LOW);
digitalWrite(motorPin3, LOW);
digitalWrite(motorPin4, LOW);
digitalWrite(motorPin5, LOW);
delay(1000);
}
