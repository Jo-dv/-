# Capstone2021 
본 repository는 21년도 부경대학교 컴퓨터공학과 졸업 프로젝트 소스 코드 저장 목적으로 21년 11월 15일 처음 생성되었습니다.  
23년 4월 7일부터 관리를 위해 기억이 나는 대로 최대한 정리 진행 예정입니다.

## 프로젝트 내용
OpenBCI를 이용한 이용한 의수 제어  
* 해당 프로젝트는 생체신호 감지 플랫폼인 OpenBCI를 이용하여 뇌파(EEG) 데이터를 수집 및 분석하여 집중 여부를 구분해 의수의 움직임을 제어하는 프로젝트입니다.  

<div>
    <a href="https://openbci.com/" target="_blank">
        <img src="https://user-images.githubusercontent.com/63555689/230773292-f3eb4260-bd46-4383-80a1-3909c666bca6.svg" width="150">
    </a>
    <a href="https://inmoov.fr/" target="_blank">
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
### `Software`
  * Language: Python
  * API: <a href="https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference" target="_blank">Brainflow</a>
  * IDE: PyCharm, Arduino IDE
  * <a href="https://openbci.com/downloads" target="_blank">OpenBCI GUI for WINDOWS</a>
### `Hardware`
  * <a href="https://docs.openbci.com/Cyton/CytonLanding/" target="_blank">OpenBCI Cyton Board</a>
  * Arduino UNO R3
  * MG946R
  * SZH-PWSDF-036
  * PCA9685
### `Material`
  * Model: <a href="https://inmoov.fr/hand-and-forarm/" target="_blank">InMoov Hand and Forarm</a>
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
      * GUI 업데이트로 인한 신호 비교 코드 변경
  * 경진대회 참여용 코드 구현 

## 구동 이미지
  
## 성과
2021 교내 국제 캡스톤디자인 경진대회 대상  
<img src="https://user-images.githubusercontent.com/63555689/230577670-e9190448-2af4-4579-a97d-0bd92e941bd5.jpg" width="450">  
<img src="https://user-images.githubusercontent.com/63555689/230578985-bb3d511e-5787-42d4-91cc-dcd04c3be9ed.png" width="450">
