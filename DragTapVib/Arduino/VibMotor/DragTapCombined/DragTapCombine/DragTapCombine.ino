// Customized Variables
int desiredDirection = 0; // can be 0 or 1;
double tappingFrequency = 8;
double runInterval = 5000;

// Arduino Nano
// white = 5 V black= GND
const int a1a = 11; // Ehemals 10 grün
const int a1b = 10; // ehemals 12 Blau
const int b1a = 9; // Ehemals 6 black
const int b1b = 8; // Ehemals 8 braun

const int motorPin1 = 2; 
const int motorPin2 = 3;
const int motorPin3 = 5;
const int motorPin4 = 12;
const int motorPin5 = 13;
// // Arduino Uno
// const int a1a = 11;
// const int a1b = 13;
// const int b1a = 6;
// const int b1b = 8;

double interval = (1.0 / (tappingFrequency * 2)) * 1000.0;

int l_on = LOW;
int r_on = LOW;
int currentDirection = 0;

unsigned long previousMillis = 0;
unsigned long previousRun = 0;
unsigned long previousSwitch = 0;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(a1a, OUTPUT);
  pinMode(a1b, OUTPUT);
  pinMode(b1a, OUTPUT);
  pinMode(b1b, OUTPUT);

  // setting up motor pins
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  pinMode(motorPin5, OUTPUT);
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
  digitalWrite(motorPin5, LOW);

  // Initialization
  initiatePinouts();

  l_on = LOW;
  r_on = LOW;
  while (!Serial)
  {
  }
}

void loop()
{
  if (Serial.available())
  {
    unsigned long currentMillis = millis();

    /*
      if (Serial.available()) {
      int x = Serial.read();
      if (x == 0) {
        //Only run this code for  1000 ms ==> after
    */
    char sent = Serial.read();
    if (sent == 'r' || sent == 'l')
    {
      if (sent == 'r')
      {
        desiredDirection = 0;
      }
      else
      {
        desiredDirection = 1;
      }
      previousRun = currentMillis;
      while (1)
      {
        if (currentMillis < previousRun + 1000)
        {
          /*
            //Switching direction every 1 seconds from
            if (currentMillis >= previousSwitch + 1000) {
            previousSwitch = currentMillis;
            //Direction switch
            //desiredDirection = 1 - desiredDirection;


            }
          */

          if (currentDirection != desiredDirection)
          {
            currentDirection = desiredDirection;
            l_on = desiredDirection;
            r_on = 1 - l_on;
            drag();
          }

          // Changing the values at the frequence to tap the pin
          if (currentMillis >= previousMillis + interval)
          {
            previousMillis = currentMillis;

            r_on = l_on = l_on == LOW ? HIGH : LOW;

            vibrateOneSide(currentDirection);
          }
          currentMillis = millis();
        }
        else
        {
          break;
        }
      }
    }
    else if (sent == '1')
    {
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, HIGH);
      delay(1000);
      digitalWrite(motorPin1, LOW);
      digitalWrite(motorPin2, LOW);
    }
    else if (sent == '2')
    {
      digitalWrite(motorPin2, HIGH);
      delay(1000);
      digitalWrite(motorPin2, LOW);
    }
    else if (sent == '3')
    {
      digitalWrite(motorPin5, HIGH);
      delay(1000);
      digitalWrite(motorPin5, LOW);
    }
    else if (sent == '4')
    {
      digitalWrite(motorPin3, HIGH);
      delay(1000);
      digitalWrite(motorPin3, LOW);
    }
    else if (sent == '5')
    {
      digitalWrite(motorPin4, HIGH);
      delay(1000);
      digitalWrite(motorPin4, LOW);
    }

    initiatePinouts();
    //    }
    //  }
  }
}

void initiatePinouts()
{
  digitalWrite(a1a, LOW);
  digitalWrite(a1b, LOW);
  digitalWrite(b1a, LOW);
  digitalWrite(b1b, LOW);
  l_on = LOW;
  r_on = LOW;
}

void drag()
{
  digitalWrite(a1a, LOW);
  digitalWrite(a1b, l_on);
  digitalWrite(b1a, LOW);
  digitalWrite(b1b, r_on);
}

void tapOrVibrate()
{
  digitalWrite(a1a, l_on);
  digitalWrite(a1b, 1 - l_on);
  digitalWrite(b1a, r_on);
  digitalWrite(b1b, 1 - r_on);
}

void vibrateOneSide(int desiredDirection)
{
  if (desiredDirection == 1)
  {
    digitalWrite(a1a, l_on);
    digitalWrite(a1b, 1 - l_on);
    digitalWrite(b1a, LOW);
    digitalWrite(b1b, LOW);
  }
  else if (desiredDirection == 0)
  {
    digitalWrite(a1a, LOW);
    digitalWrite(a1b, LOW);
    digitalWrite(b1a, r_on);
    digitalWrite(b1b, 1 - r_on);
  }
}
