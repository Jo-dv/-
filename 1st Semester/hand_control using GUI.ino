#include <Adafruit_PWMServoDriver.h>
#include <Servo.h>

Adafruit_PWMServoDriver pwm=Adafruit_PWMServoDriver();

const byte numChars = 32;
char receivedChars[numChars];
String previousData = "";
boolean newData = false;
 
void setup() {
pwm.begin();
pwm.setOscillatorFrequency(27000000);
pwm.setPWMFreq(50);
Serial.begin(57600);
alltorest(); //for reset
}

void loop() {
  recvWithEndMarker();
  showNewData();
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;
    
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0';
            ndx = 0;
            newData = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        String s = receivedChars;
        if (!s.equals(previousData)) {
          if (s.equals("false")) {
            alltorest();
            delay(4000);
          }
          else if (s.equals("true")) {
            alltomax();
            delay(4000);
          }
        }
        newData = false;
        previousData = s;
    }
}

void alltorest() {
for(int min_pulse = 600; min_pulse >= 150; min_pulse--)
    pwm.setPWM(0,0,min_pulse);
for(int min_pulse = 600; min_pulse >= 150; min_pulse--) {
    pwm.setPWM(1,0,min_pulse);
    pwm.setPWM(2,0,min_pulse);
    pwm.setPWM(3,0,min_pulse);
    pwm.setPWM(4,0,min_pulse);
  }
}
 
void alltomax() {
for(int min_pulse = 150; min_pulse <= 600; min_pulse++) {
    pwm.setPWM(1,0,min_pulse);
    pwm.setPWM(2,0,min_pulse);
    pwm.setPWM(3,0,min_pulse);
    pwm.setPWM(4,0,min_pulse);
  }
for(int min_pulse = 150; min_pulse <= 600; min_pulse++)
    pwm.setPWM(0,0,min_pulse);
}

 
