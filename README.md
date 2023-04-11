# Capstone2021 
본 repository는 21년도 부경대학교 컴퓨터공학과 졸업 프로젝트 소스 코드 저장 목적으로 21년 11월 15일 처음 생성되었습니다.  
23년 4월 7일부터 관리를 위해 기억이 나는 대로 최대한 정리 진행 예정입니다.

## 프로젝트 내용
OpenBCI를 이용한 이용한 의수 제어  
* 해당 프로젝트는 생체신호 감지 플랫폼인 OpenBCI를 이용하여 뇌파(EEG) 데이터를 수집 및 분석하여 집중 여부를 구분해 의수의 움직임을 제어하는 프로젝트입니다.  

<div>
    <a href="https://openbci.com/">
        <img src="https://user-images.githubusercontent.com/63555689/230773292-f3eb4260-bd46-4383-80a1-3909c666bca6.svg" width="150">
    </a>
    <a href="https://inmoov.fr/">
        <img src="https://user-images.githubusercontent.com/63555689/230773991-e2af11dd-bc38-481e-b132-dc37820ec605.png" width="200">
    </a>
</div> 

## 진행 기간
* 2021.03.04 ~ 2021.06.03 - 1학기  
* 2021.09.02 ~ 2021.12.02 - 2학기

## 참여 인원
### 1학기
* 김\*금 - 자료 조사 및 발표  
* 조\*재 - 서류 처리, 의수 제작 및 코드 구현
### 2학기
* 김\*금 - 자료 조사 및 발표  
* 이\*형 - 서류 처리  
* 조\*재 - 유지보수

## 개발 및 구현 환경
### Software
  * Language: Python
  * API: <a href="https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference">Brainflow</a>
  * IDE: PyCharm, Arduino IDE
  * <a href="https://openbci.com/downloads">OpenBCI GUI for WINDOWS</a>
### Hardware
  * <a href="https://docs.openbci.com/Cyton/CytonLanding/">OpenBCI Cyton Board</a>
  * Arduino UNO R3
  * MG946R
  * SZH-PWSDF-036
  * PCA9685
### Material
  * Model: <a href="https://inmoov.fr/hand-and-forarm/">InMoov Hand and Forarm</a>
  * Power Supply: 18650 Li-ion battery(3500mAh)
  * M3x20 Bolt and Nut
  
## 진행 내용
### 1학기
  * WiFi Shield를 이용한 Ganglion Board 작동 테스트
  * 의수 제작
  * OpenBCI와 Arduino(의수) 연결
    * GUI의 Networking Widget과 Focusing Widget 사용
### 2학기
  * Motor Imagery를 이용한 제어를 위해 Cyton Board로 교체
    * Motoar Iamgery 실험
      * 실험 실패로 GUI를 이용하여 논문 진행
  * 경진대회 참여용 코드 구현 

## 트러블 슈팅
<details>
<summary>OpenBCI USB Dongle 인식 문제</summary>
  <div markdown="1">

  * 관련 드라이버가 설치되어 있지 않아서 발생한 문제
  * 드라이버(D2XX Driver)를 설치해 줌으로써 해결
    * 설치 당시 버전: 2.12.28
    * https://ftdichip.com/drivers/d2xx-drivers/
  
  </div>
</details>

<details>
<summary>Focus 실험 문제</summary>
  <div markdown="1">

  * 1학기 실험 당시 Focus Widget은 High beta and low alpha, 즉 Meditation 형태의 집중 상태를 측정하는 Widget
    
    > Reading the paragraph again, the “research” that led to the conclusion “high alpha low beta”, was actually referring to the small tests we did using OpenBCI, when Jordan’s performing meditation, and when other users are trying to “focus” during our spring exhibition.
    > <br></br>
    > For the exact values “0.7-2.0uv” or “0.0-0.7uv”, they were also actually referring to this “high alpha low beta” pattern. That’s why later versions of the focus widget would have tweak-able thresholds compared to set values.
    > <br></br>
    > The word “focus” was a generic term. While the original data was derived from my classmate Jordan’s brainwave when he’s doing “meditation”, it also mostly worked when I told users to “focus”. I would suggest “focus of visual attention” or “meditation” as more accurate to describe the desired “focused” state.
    > <br></br>
    > https://openbci.com/forum/index.php?p=/discussion/2418/gui-focus-widget-algorithm-question (2023.04.10)
    * 해당 사실을 모르고 Concentraion에 맞춰 실험을 진행하였기에 제어하는 데 어려움이 발생  
  
  * 2학기 시점, 업데이트된 GUI는 Meditation과 Concentraion을 모두 지원하였기에 이를 인지하고 실험을 진행함으로써 해결  

    > Choose from "Relaxation" or "Concentration" as the desired flavor of Focus to detect.
    > <br></br>
    > "Relaxation" generally looks at FFT values associated with Delta, Theta and Alpha brainwaves, while "Concentration" looks at Beta and Gamma brainwaves.
    > <br></br>
    > Relaxation is usually achieved by "meditating" with eyes closed, while Concentration can be achieved by focusing intently with eyes open. 
    > <br></br>
    > https://docs.openbci.com/Software/OpenBCISoftware/GUIWidgets/#focus-widget (2023.04.10)
    
  </div>
</details>

<details>
<summary>GUI 업데이트 이후 Arduino 비작동 문제</summary>
  <div markdown="1">

  * Serial 프로토콜을 이용한 Focus 데이터 변경으로 인해 발생한 문제
    * Networking Data Format 변경 전후  
      |변경 전  |변경 후|
      |:--:     |:--: |
      |"true\n" |"1\n"|
      |"false\n"|"0\n"|
  * 수신된 데이터를 비교하는 코드를 변경된 Format에 맞춰 변경해 줌으로써 해결
    * 변경 전
      ```
      if (s.equals("false")) {
        \\Code
      }
      else if (s.equals("true")) { 
        \\Code
      }
      ```
    * 변경 후
      ```
      if (s.equals("1")) {
        \\Code
      }
      else if (s.equals("0")) { 
        \\Code
      }
      ```
  
  </div>
</details>

<details>
<summary>Motor imagery 적용 문제</summary>
  <div markdown="1">

  1. NeuroPype Motor Imagery 파이프라인 실행 시 에러 발생  
      * 에러 내용
        ```
        ERROR: The following error occurred in node Common Spatial Patterns: the leading minor of order 1 of 'b' is not positive definite. The factorization of 'b' could not be completed and no eigenvalues or eigenvectors were computed.  
        ERROR: CSP must be trained before it can be used
        ERROR: CSP must be trained before it can be used
        ERROR: CSP must be trained before it can be used
        ...
        ERROR: CSP must be trained before it can be used
        ```
      * 해결
        * 해당 문제에 대해 NeuroPype에 문의 후, 학습 데이터가 부족 혹은 EEG 채널 간 단락으로 발생하는 문제로 보인다는 답변 수신
        * 데이터 수집 시 시도 횟수 변경: 120회 $\rightarrow$ 360회
  2. 에러 해결 후 저조한 성능 문제 발생
     * 5번의 실험 동안 평균 약 46.2%의 Loss(MisClassification Rate) 획득
       * 상상하는 방식에 대한 의문 발생
     * 해결
       * 사용하지 않은 채널을 비활성화하여 노이즈를 제거하고 기존 CSP 알고리즘에서 FBCSP 알고리즘으로 변경하여 학습 시 보다 많은 파라미터 생성
         * 데이터 수집 시 시도 횟수 변경: 360회 $\rightarrow$ 120회
           * 실험 시간 단축
         * Loss 0.067 획득
  3. 상상에 대한 불확실성 문제
     * 움직임을 상상하는 것 대신 눈 깜빡임이나 이를 꽉 다무는 행위를 함으로써 발생하는 노이즈를 학습시켜 각각 0.01, 0.06의 Loss 획득
     * 결론
       * 미숙한 움직임 상상으로 인해 발생하는 스파이크 미미하여 1번 및 2번 문제가 발생한 것으로 추정
       * 이후 실험들에서 2번만큼의 결과가 나오지 않아서 여건상 Motor Imagery 실험 중단
  </div>
</details>

## 구동 이미지
  * 작성 예정
  
## 성과
2021 교내 국제 캡스톤디자인 경진대회 대상  
<img src="https://user-images.githubusercontent.com/63555689/230577670-e9190448-2af4-4579-a97d-0bd92e941bd5.jpg" width="450">  
<img src="https://user-images.githubusercontent.com/63555689/230578985-bb3d511e-5787-42d4-91cc-dcd04c3be9ed.png" width="450">
