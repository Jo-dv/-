#include <Adafruit_PWMServoDriver.h>
#include <Servo.h>

Adafruit_PWMServoDriver pwm=Adafruit_PWMServoDriver();

char state;
int prev = 0;

void setup() {
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(50);
  Serial.begin(9600);
  alltorest(); //for reset
}

void loop() {
  if (Serial.available() > 0) 
  {
    state = Serial.read();
    if (state == '0') 
    {
      if (prev == 1) 
        alltorest();
      prev = 0;
    }
    else 
    {
      if (prev == 0)
        alltomax();
      prev = 1;
    }
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
