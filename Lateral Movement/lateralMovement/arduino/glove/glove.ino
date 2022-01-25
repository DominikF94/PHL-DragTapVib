// Customized Variables
int desiredDirection = 0; // can be 0 or 1;
double tappingFrequency = 9;
double runInterval = 5000;

// Arduino Nano
// white = 5 V black= GND
const int a1a = 11; // Ehemals 10 grün
const int a1b = 10; // ehemals 12 Blau
const int b1a = 9; // Ehemals 6 black
const int b1b = 8; // Ehemals 8 braun



const int motor1 = 2;
const int motor2 = 3;
const int motor3 = 5;
const int motor4 = 12;
const int motor5 = 13;

const int vibration_duration = 869; // 869;

double interval = (1.0 / (tappingFrequency * 2)) * 1000.0;

int l_on = LOW;
int r_on = LOW;
int currentDirection = 0;

unsigned long previousMillis = 0;
unsigned long previousRun = 0;
unsigned long previousSwitch = 0;

void testMotor(int motor)
{
  digitalWrite(motor, HIGH);
  digitalWrite(motor3, HIGH);
  delay(vibration_duration);
  digitalWrite(motor, LOW);
  digitalWrite(motor3, LOW);
}


void setup()
{
  Serial.begin(9600);
  pinMode(motor1, OUTPUT);
  pinMode(motor2, OUTPUT);
  pinMode(motor3, OUTPUT);
  pinMode(motor4, OUTPUT);
  pinMode(motor5, OUTPUT);
  //Setting up DragTabVib
  pinMode(a1a, OUTPUT);
  pinMode(a1b, OUTPUT);
  pinMode(b1a, OUTPUT);
  pinMode(b1b, OUTPUT);

    // Initialization
  initiatePinouts();

  l_on = LOW;
  r_on = LOW;

  Serial.println("started");

  
}

int mapToMotor(int finger)
{
  if (finger == 1)
  {
    return motor1;
  }
  else if (finger == 2)
  {
    return motor2;
  }
  else if (finger == 3)
  {
    return motor3;
  }
  else if (finger == 4)
  {
    return motor4;
  }
  else if (finger == 5)
  {
    return motor5;
  }
  else if (finger == 6)
  {
    tap (vibration_duration/2, 0);
    return 0;
  }
  else
  {
    tap (vibration_duration/2, 1);
    return 1;
  }
}

void playSong(String input)
{
  int ind = input.indexOf(','); // finds location of first ,
  do
  {
    ind = input.indexOf(',');
    // Finger in diesem Durchgang
    String fingers = input.substring(0, ind);
    String remainingFingers = fingers;
    int ind_fingers = -1;
    int octaveJumpIndex = fingers.indexOf('#');

    int currentVibrationDuration = vibration_duration;

    // Es ist im remainingFingers String noch ein # ==> Jump
    if (octaveJumpIndex > -1)
    {
      //Ersten Motor ansprechen der im String steht
      int motor = mapToMotor(remainingFingers.substring(0, 1).toInt());
      //digitalWrite(motor, HIGH);
      //Nur halbe Zeit, da hier ja noch der VErschiebe Stimulus
      //delay((vibration_duration / 2));
      // Danach nur noch halb vibrieren
      currentVibrationDuration = vibration_duration - (vibration_duration / 2);
      //Restliche Finger aus dem Substring der mit 2 beginnt (sollte, oder; sein)
      remainingFingers = remainingFingers.substring(2);

      fingers = remainingFingers;
    }

    do
    {
      //ind_fingers bei erstem Durchlauf (Erstes Zeichen wegwerfen(entweder, oder ;))
      remainingFingers = remainingFingers.substring(ind_fingers + 1);
      //Erster Motor im String, also erster nach #
      int motor = mapToMotor(remainingFingers.substring(0, 1).toInt());
      digitalWrite(motor, HIGH);
      ind_fingers = remainingFingers.indexOf(';');
      //Falls ind_fingers > 0 (Wenn; also wenn 2 gleichzeitig) teste nochmal
    } while (ind_fingers > 0);
    delay(currentVibrationDuration);
    remainingFingers = fingers;
    ind_fingers = -1;
    do
    {
      //reset auf Fingers davor also wieder mit ; Damit am Ende alle Motoren die in Schleife davor aktiviert, wieder auf Low
      remainingFingers = remainingFingers.substring(ind_fingers + 1);
      int motor = mapToMotor(remainingFingers.substring(0, 1).toInt());
      digitalWrite(motor, LOW);
      ind_fingers = remainingFingers.indexOf(';');
    } while (ind_fingers > 0);
    //Delay zwischen Noten
    delay(48);
    input = input.substring(ind + 1);
  } while (ind > 0);
}

void test()
{
  digitalWrite(motor1, HIGH);
  delay(vibration_duration + 48);
  digitalWrite(motor1, LOW);
  digitalWrite(motor2, HIGH);
  delay(vibration_duration + 48);
  digitalWrite(motor2, LOW);
  digitalWrite(motor3, HIGH);
  delay(vibration_duration + 48);
  digitalWrite(motor3, LOW);
  digitalWrite(motor4, HIGH);
  delay(vibration_duration + 48);
  digitalWrite(motor4, LOW);
  digitalWrite(motor5, HIGH);
  delay(vibration_duration + 48);
  digitalWrite(motor5, LOW);
}

void loop()
{
  // test();
  if (Serial.available())
  {
    String input = Serial.readStringUntil('>');
    if (input == "reset")
    {
      // reset motors
    }
    else
    {
      delay(vibration_duration);
      playSong(input);
    }
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


void tap(int time, int direction) {
  desiredDirection = direction;
      unsigned long currentMillis = millis();
      previousRun = currentMillis;
      while (1)
      {
        if (currentMillis < previousRun + time)
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
      initiatePinouts();
}
