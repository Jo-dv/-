import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import keyboard

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams

def main():
    option = ['serial_port', 'arduino_port', 'baud_rate', 'focusing_option', 'threshold']  # 옵션 label
    op_val = []  # 옵션 value

    for i in option:  # 사용할 옵션 입력
        print(f'{i}: ', end='')
        op_val.append(input())
    op_val[3] = int(op_val[3])
    op_val[4] = float(op_val[4])
    threshold = op_val[4]

    BoardShim.enable_dev_board_logger()  # 보드 연결시 상태 확인 메시지 활성화
    MLModel.disable_ml_logger()  # 예측값 출력시 발생하는 메시지 비활성화

    params = BrainFlowInputParams()  # 연결 설정 라이브러리 구조체 불러오기
    params.board_id = BoardIds.CYTON_BOARD.value  # 연결할 보드 id 설정
    params.serial_port = op_val[0]  # 연결할 보드의 통신 보드 포트 설정 ex)wifi shield, dongle이 통신 보드

    board = BoardShim(params.board_id, params)  # 보드 설정 라이브러리 구조체 불러오기
    sampling_rate = BoardShim.get_sampling_rate(params.board_id)  # 보드 자체에 설정된 샘플링 레이트 불러오기, OpenBCI는 250Hz
    eeg_channels = BoardShim.get_eeg_channels(params.board_id)  # 보드의 채널 불러오기, Cyton은 8채널이므로 [1, 2, .. ,7 ,8]의 형태
    eeg_channels = eeg_channels[:2]  # 사용할 채널이 1,2이므로 불러온 채널리스트를 슬라이싱

    if op_val[3] == 0:  # ML 라이브러리 불러와서 모델 값 설정
        focusing_params = BrainFlowModelParams(BrainFlowMetrics.RELAXATION.value,BrainFlowClassifiers.REGRESSION.value)
    else:
        focusing_params = BrainFlowModelParams(BrainFlowMetrics.CONCENTRATION.value,BrainFlowClassifiers.REGRESSION.value)

    focusing = MLModel(focusing_params)  # ML 모델 생성

    ser = serial.Serial(op_val[1], int(op_val[2]))  # 아두이노 포트 및 보드레이트 설정
    
    board.prepare_session()  # 보드 연결 준비
    board.start_stream()  # 보드 스트림 시작
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'Stream start')  # 스트림 시작시 메시지 출력

    trial = 0  # 예측 데이터 생성 횟수
    focusing_point = 0  # 예측 데이터 중, 집중한 데이터 갯수
    while True:
        time.sleep(5)  # 계산 텀 설정
        data = board.get_board_data()  # 보드에서 데이터 읽어오기
        trial += 1

        bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, True)  # 채널별 데이터 대역 파워의 평균 및 표준편차 계산
        feature_vector = np.concatenate((bands[0], bands[1]))  # 대역 평균[0], 표준편차[1] 취합

        focusing.prepare()  # 분류 준비
        prediction = focusing.predict(feature_vector)  # 예측값 생성
        print('Focusing: %f' % prediction)
        focusing.release()  # 분류 종료

        if prediction > threshold:  # 예측값이랑 임계값 비교후 아두이노에 전송
            ser.write(b'1')  # 집중 상태로 판단
            focusing_point += 1  # 집중 데이터 갯수 증가
        else:
            ser.write(b'0')  # 비집중 상태로 판단

        if keyboard.is_pressed('enter'):
            break

    board.stop_stream()
    board.release_session()
    # 스트림 종료

    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'Stream end')  # 스트림 종료 메시지 출력
    x = np.arange(2)
    trial_label = ['Trial', 'Focusing']
    trial_value = [trial, focusing_point]
    plt.bar(x, trial_value)
    plt.xticks(x, trial_label)
    plt.show()
    # 데이터 스트림 횟수와 그 중 집중한 횟수 시각화

if __name__ == "__main__":
    main()
