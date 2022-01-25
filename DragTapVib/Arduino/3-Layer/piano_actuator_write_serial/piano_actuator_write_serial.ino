// Customized parameters
int vibDirection = 0; // 0 for left, 1 for right

// Layer 1 (horizontal)
const int a1a = 4;
const int a1b = 3;
const int b1a = 6;
const int b1b = 5;
double l1DragFreq = 1;
double l1DragInterval = (1.0 / (l1DragFreq * 2)) * 1000.0;
unsigned long l1DragPreviousMillis = 0;
int l1LOn = LOW;
int l1ROn = LOW;

// Layer 2 (vertical)
const int c1a = 9;
const int c1b = 8;
const int d1a = 11;
const int d1b = 10;
double l2VibFreq = 40;
double l2VibInterval = (1.0 / (l2VibFreq * 2)) * 1000.0;
unsigned long l2VibPreviousMillis = 0;
int l2LOn = LOW;
int l2ROn = LOW;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(a1a, OUTPUT);
  pinMode(a1b, OUTPUT);
  pinMode(b1a, OUTPUT);
  pinMode(b1b, OUTPUT);
  pinMode(c1a, OUTPUT);
  pinMode(c1b, OUTPUT);
  pinMode(d1a, OUTPUT);
  pinMode(d1b, OUTPUT);

  // Initialization
  l1InitiatePinOuts();
  l2InitiatePinOuts();
  while (!Serial) {}
}

void loop() {
  if (Serial.available()) {
    switch (Serial.read()) {
      case '0':

        while (true) {
          // put your main code here, to run repeatedly:
          if (millis() >= l1DragPreviousMillis + l1DragInterval) {
            l1DragPreviousMillis = millis();
            l1LOn = l1LOn == LOW ? HIGH : LOW;
            l1ROn = 1 - l1LOn;
            l1Drag();
          }

          if (vibDirection == 0) { // indicate left direction
            if (millis() >= l2VibPreviousMillis + l2VibInterval) {
              l2VibPreviousMillis = millis();
              l2ROn = l2ROn == LOW ? HIGH : LOW;
              l2RVib();
            }
          } else if (vibDirection == 1) { // indicate right direction
            if (millis() >= l2VibPreviousMillis + l2VibInterval) {
              l2VibPreviousMillis = millis();
              l2LOn = l2LOn == LOW ? HIGH : LOW;
              l2LVib();
            }
          }

          if (millis() >= l2VibPreviousMillis + l2VibInterval) {
            l2VibPreviousMillis = millis();
            l2ROn = l2ROn == LOW ? HIGH : LOW;
            l2RVib();
          }
          
        }
        break;
      default:

        break;
    }
  }
}

void l1InitiatePinOuts() {
  digitalWrite(a1a, LOW);
  digitalWrite(a1b, LOW);
  digitalWrite(b1a, LOW);
  digitalWrite(b1b, LOW);
  l1LOn = LOW;
  l1ROn = LOW;
}

void l2InitiatePinOuts() {
  digitalWrite(c1a, LOW);
  digitalWrite(c1b, LOW);
  digitalWrite(d1a, LOW);
  digitalWrite(d1b, LOW);
  l2LOn = LOW;
  l2ROn = LOW;
}

void l1Drag() {
  digitalWrite(a1a, LOW);
  digitalWrite(a1b, l1LOn);
  digitalWrite(b1a, LOW);
  digitalWrite(b1b, l1ROn);
}

void l1Vib() {
  digitalWrite(a1a, l1LOn);
  digitalWrite(a1b, 1 - l1LOn);
  digitalWrite(b1a, l1ROn);
  digitalWrite(b1b, 1 - l1ROn);
}

void l2Drag() {
  digitalWrite(c1a, LOW);
  digitalWrite(c1b, l2LOn);
  digitalWrite(b1a, LOW);
  digitalWrite(b1b, l2ROn);
}

void l2Vib() {
  digitalWrite(c1a, l2LOn);
  digitalWrite(c1b, 1 - l2LOn);
  digitalWrite(d1a, l2ROn);
  digitalWrite(d1b, 1 - l2ROn);
}

void l2LVib() {
  digitalWrite(c1a, l2LOn);
  digitalWrite(c1b, 1 - l2LOn);
  digitalWrite(d1a, LOW);
  digitalWrite(d1b, LOW);
}

void l2RVib() {
  digitalWrite(c1a, LOW);
  digitalWrite(c1b, LOW);
  digitalWrite(d1a, l2ROn);
  digitalWrite(d1b, 1 - l2ROn);
}
