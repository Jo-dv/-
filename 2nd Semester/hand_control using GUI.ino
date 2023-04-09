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
          if (s.equals("0")) {
            alltorest();
            delay(5000);
          }
          else if (s.equals("1")) {
            alltomax();
            delay(5000);
          }
        }
        newData = false;
        previousData = s;
    }
}

void alltorest() {
for(int pulse = 600; pulse >= 150; pulse--)
    pwm.setPWM(0,0,pulse);
for(int pulse = 600; pulse >= 150; pulse--) {
    pwm.setPWM(2,0,pulse);
    pwm.setPWM(4,0,pulse);
    pwm.setPWM(6,0,pulse);
    pwm.setPWM(8,0,pulse);
  }
}
 
void alltomax() {
for(int pulse = 150; pulse <= 600; pulse++) {
    pwm.setPWM(2,0,pulse);
    pwm.setPWM(4,0,pulse);
    pwm.setPWM(6,0,pulse);
    pwm.setPWM(8,0,pulse);
  }
for(int pulse = 150; pulse <= 600; pulse++)
    pwm.setPWM(0,0,pulse);
}
