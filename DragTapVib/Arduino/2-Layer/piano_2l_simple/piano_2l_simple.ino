// Customized Variables
int desiredDirection = 1; // can be 0 or 1;
double tappingFrequency = 8;
double runInterval = 5000;

// Arduino Nano
const int a1a = 10;
const int a1b = 12;
const int b1a = 6;
const int b1b = 8;
// // Arduino Uno
// const int a1a = 11;
// const int a1b = 13;
// const int b1a = 6;
// const int b1b = 8;

double interval = (1.0/(tappingFrequency * 2))*1000.0;

int l_on = LOW;
int r_on = LOW;
int currentDirection = 2;

unsigned long previousMillis = 0;
unsigned long previousRun = 0;
unsigned long previousSwitch = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(a1a, OUTPUT);
  pinMode(a1b, OUTPUT);
  pinMode(b1a, OUTPUT);
  pinMode(b1b, OUTPUT);


  // Initialization
  initiatePinouts();

  l_on = LOW;
  r_on = LOW;

}

void loop() {
  // put your main code here, to run repeatedly:
//  digitalWrite(a1a, HIGH);
//  digitalWrite(a1b, LOW);
//  digitalWrite(b1a, HIGH);
//  digitalWrite(b1b, LOW);
  unsigned long currentMillis = millis();


  //Switching direction every 1 seconds from
  if (currentMillis >= previousSwitch + 2000) {
    previousSwitch = currentMillis;
    desiredDirection = 1 - desiredDirection;
  }

  if (currentDirection != desiredDirection) {
    currentDirection = desiredDirection;
    l_on = desiredDirection;
    r_on = 1 - l_on;
    drag();
    delay(500);
  }
  
  if (currentMillis >= previousMillis + interval) {
      previousMillis = currentMillis;
      
      r_on = l_on = (l_on == LOW?HIGH:LOW);
      
      vibrateOneSide(currentDirection);
      //tapOrVibrate();      
    }
}


void initiatePinouts() {
  digitalWrite(a1a, LOW);
  digitalWrite(a1b, LOW);
  digitalWrite(b1a, LOW);
  digitalWrite(b1b, LOW);
  l_on = LOW;
  r_on = LOW;
}

void drag() {
  digitalWrite(a1a, LOW);
  digitalWrite(a1b, l_on);
  digitalWrite(b1a, LOW);
  digitalWrite(b1b, r_on);
}

void tapOrVibrate() {
  digitalWrite(a1a, l_on);
  digitalWrite(a1b, 1 - l_on);
  digitalWrite(b1a, r_on);
  digitalWrite(b1b, 1 - r_on);
}

void vibrateOneSide(int desiredDirection) {
  if (desiredDirection == 1) {
    digitalWrite(a1a, l_on);
    digitalWrite(a1b, 1 - l_on);
    digitalWrite(b1a, LOW);
    digitalWrite(b1b, LOW);
  } else if (desiredDirection == 0) {
    digitalWrite(a1a, LOW);
    digitalWrite(a1b, LOW);
    digitalWrite(b1a, r_on);
    digitalWrite(b1b, 1 - r_on);
  }
}
