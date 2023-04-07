#include <Adafruit_PWMServoDriver.h>
//#include <Servo.h>

Adafruit_PWMServoDriver pwm=Adafruit_PWMServoDriver();

char state;  // 신호 상태를 저장할 변수
int prev = 0;  // 중복 동작 방지를 위한 flag
// flag를 사용한 이유는 수축일 때 수축, 이완일 때 이완이 발생하지 않도록 하기 위함, 즉 서로 반대의 신호를 받았을 때만 동작하도록 설계

void setup() {  // 전원 인가 시 초기화 코드
  pwm.begin();  // pwm 모듈은 기본 제공 라이브러리 코드 사용
  pwm.setOscillatorFrequency(27000000); 
  pwm.setPWMFreq(50);
  Serial.begin(9600);  // 시리얼 통신
  alltorest(); //for reset, 모터 각도 초기화
}

void loop() {
  if (Serial.available() > 0)  // 시리얼 통신이 가능하면
  {
    state = Serial.read();  // 값 읽어 옴
    if (state == '0')  // 이완 신호를 받았다면
    {
      if (prev == 1)  // 직전 동작이 수축이었을 때
        alltorest();
      prev = 0;  // 직전 동작 상태 이완으로 변경
    }
    else 
    {
      if (prev == 0)
        alltomax();
      prev = 1;
    }
  }
}

void alltorest() {  // 손가락 이완
  for(int pulse = 600; pulse >= 150; pulse--)  // 엄지 손가락을 먼저 이완시킨 후
      pwm.setPWM(0,0,pulse);
  for(int pulse = 600; pulse >= 150; pulse--) {  // 나머지 손가락들을 순차적으로 이완
      pwm.setPWM(2,0,pulse);
      pwm.setPWM(4,0,pulse);
      pwm.setPWM(6,0,pulse);
      pwm.setPWM(8,0,pulse);
    }
}
 
void alltomax() {  // 손가락 수축
  for(int pulse = 150; pulse <= 600; pulse++) {  // 엄지 손가락을 제외한 나머지 손가락들을 순차적으로 수축시킨 후
      pwm.setPWM(2,0,pulse);
      pwm.setPWM(4,0,pulse);
      pwm.setPWM(6,0,pulse);
      pwm.setPWM(8,0,pulse);
    }
  for(int pulse = 150; pulse <= 600; pulse++)  // 엄지 손가락 수축
      pwm.setPWM(0,0,pulse);
}