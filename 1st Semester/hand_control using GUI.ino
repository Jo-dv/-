#include <Adafruit_PWMServoDriver.h>
//#include <Servo.h>

Adafruit_PWMServoDriver pwm=Adafruit_PWMServoDriver();

const byte numChars = 32;  // 배열의 
char receivedChars[numChars];  // 입력받은 데이터를 저장할 길이 32짜리 배열
String previousData = "";  // 갱신된 데이터와 일치여부를 판별하기 위해 마지막으로 들어온 값을 저장할 
boolean newData = false;  // 데이터 갱신 여부
 
void setup() {  // 전원 인가 시 초기화 코드
pwm.begin();  // pwm 모듈은 기본 제공 라이브러리 코드 사용
pwm.setOscillatorFrequency(27000000);
pwm.setPWMFreq(50);
Serial.begin(57600);  // 시리얼 통신
alltorest(); //for reset, 모터 각도 초기화
}

void loop() {
  recvWithEndMarker();  // 데이터 수신
  showNewData();  // 수신된 데이터 판별
}

void recvWithEndMarker() {
    static byte ndx = 0;  // 수신되는 문자열 형태의 데이터를 하나씩 확인하기 위한 인덱스 변수
    char endMarker = '\n';  // 데이터의 끝을 확인할 마커 지정
    char rc;  // 수신된 데이터를 하나씩 저장할 변수
    
    while (Serial.available() > 0 && newData == false) {  // 시리얼 통신이 가능하고 새로운 데이터가 없다면
        rc = Serial.read();  // 시리얼 통신을 통해 새로운 데이터 수신

        if (rc != endMarker) {  // 현재 들어온 데이터가 엔드 마커로 지정한 개행 문자가 아니라면
            receivedChars[ndx] = rc;  // 현재 인덱스에 해당 데이터 저장
            ndx++;  // 인덱스 갱신
            if (ndx >= numChars) {  // 만약 데이터가 많아서 인덱스를 초과할 경우
                ndx = numChars - 1;  // 인덱스를 항상 끝 자리에 맞춤
            }
        }
        else {  // 현재 들어온 데이터가 엔드 마커와 일치한다면
            receivedChars[ndx] = '\0';  // 최종 인덱스에 null 값 저장
            ndx = 0;  // 다음 데이터 수신을 위한 인덱스 초기화
            newData = true;  // 데이터 갱신
        }
    }
}

void showNewData() {
    if (newData == true) {  // 데이터가 갱신되었다면(= 새로운 데이터가 들어왔다면)
        String s = receivedChars;  // 문자열 배열의 값을 문자열로 저장
        if (!s.equals(previousData)) {  // 현재 들어온 값이 이전 값과 동일하지 않고
          if (s.equals("false")) {  // 들어온 값이 false(이완 신호)라면
            alltorest();
            delay(4000);  // 실시간 스트림을 통해 현재와 반대되는 값을 받았을 경우, 이완되는 도중 수축되는 것을 방지하기 위한 딜레이
          }
          else if (s.equals("true")) {  // 들어온 값이 true(수축 신호)라면
            alltomax();
            delay(4000);
          }
        }  // 현재 들어온 데이터가 이전 데이터와 동일하다면 동작을 수행하지 않음
        newData = false;  // 데이터 판독이 끝났으므로 다음 데이터를 받기 위해 데이터 여부 갱신
        previousData = s;  // 현재 데이터를 이전 데이터로 저장
    }
}

void alltorest() {  // 손가락 이완, 동작 코드는 adafruit에서 제공하는 기본 예제를 
for(int min_pulse = 600; min_pulse >= 150; min_pulse--)  // 엄지 손가락을 먼저 이완시킨 후
    pwm.setPWM(0,0,min_pulse);
for(int min_pulse = 600; min_pulse >= 150; min_pulse--) {  // 나머지 손가락들을 순차적으로 이완
    pwm.setPWM(1,0,min_pulse);
    pwm.setPWM(2,0,min_pulse);
    pwm.setPWM(3,0,min_pulse);
    pwm.setPWM(4,0,min_pulse);
  }
}
 
void alltomax() {  // 손가락 수축
for(int min_pulse = 150; min_pulse <= 600; min_pulse++) {  // 엄지 손가락을 제외한 나머지 손가락들을 순차적으로 수축시킨 후
    pwm.setPWM(1,0,min_pulse);
    pwm.setPWM(2,0,min_pulse);
    pwm.setPWM(3,0,min_pulse);
    pwm.setPWM(4,0,min_pulse);
  }
for(int min_pulse = 150; min_pulse <= 600; min_pulse++)  // 엄지 손가락 수축
    pwm.setPWM(0,0,min_pulse);
}
