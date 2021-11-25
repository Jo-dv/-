import time
import keyboard
import serial
import numpy as np
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
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

    bandStopFrequency = 60.0  # 노치 필터 값
    bp_lowerBound = 5.0  # 하한
    bp_upperBound = 50.0  # 상한
    bp_centerFreq = (bp_upperBound + bp_lowerBound) / 2.0  # 중간값
    bp_bandWidth = bp_upperBound - bp_lowerBound  # 폭

    BoardShim.enable_dev_board_logger()  # 보드 연결시 상태 확인 메시지 활성화
    MLModel.disable_ml_logger()  # 예측값 출력시 발생하는 메시지 비활성화

    params = BrainFlowInputParams()  # 연결 설정 라이브러리 구조체 불러오기
    params.board_id = BoardIds.CYTON_BOARD.value  # 연결할 보드 id 설정
    params.serial_port = op_val[0]  # 연결할 보드의 통신 보드 포트 설정 ex)wifi shield, dongle이 통신 보드

    board = BoardShim(params.board_id, params)  # 보드 설정 라이브러리 구조체 불러오기
    sampling_rate = BoardShim.get_sampling_rate(params.board_id)  # 보드 자체에 설정된 샘플링 레이트 불러오기, OpenBCI는 250Hz
    eeg_channels = BoardShim.get_exg_channels(params.board_id)  # 보드의 채널 불러오기, Cyton은 8채널이므로 [1, 2, .. ,7 ,8]의 형태
    eeg_channels = eeg_channels[:2]  # 사용할 채널이 1,2이므로 불러온 채널리스트를 슬라이싱

    if op_val[3] == 0:  # ML 라이브러리 불러와서 모델 값 설정
        focusing_params = BrainFlowModelParams(BrainFlowMetrics.RELAXATION.value, BrainFlowClassifiers.REGRESSION.value)
    else:
        focusing_params = BrainFlowModelParams(BrainFlowMetrics.CONCENTRATION.value, BrainFlowClassifiers.REGRESSION.value)

    focusing = MLModel(focusing_params)  # ML 모델 생성

    ser = serial.Serial(op_val[1], int(op_val[2]))  # 아두이노 포트 및 보드레이트 설정

    board.prepare_session()  # 보드 연결 준비
    board.config_board("x3161000X")  # 채널 3 비활성화
    board.config_board("x4161000X")  # 채널 4 비활성화
    board.config_board("x5161000X")  # 채널 5 비활성화
    board.config_board("x6161000X")  # 채널 6 비활성화
    board.config_board("x7161000X")  # 채널 7 비활성화
    board.config_board("x8161000X")  # 채널 8 비활성화
    board.start_stream()  # 보드 스트림 시작
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'Stream start')  # 스트림 시작시 메시지 출력
    trial = 0  # 예측 데이터 생성 횟수
    focusing_point = 0  # 예측 데이터 중, 집중한 데이터 갯수
    continuous_focusing_point = 0  # 지속적인 집중을 수행한 횟수
    continuous_focusing_table = []  # 지속적인 집중에 대한 정보 테이블

    while True:
        time.sleep(5)  # 계산 텀 설정
        data = board.get_board_data()[:3, :]  # 보드에서 데이터 읽어오기

        for i in range(len(eeg_channels)):  # 필터링
            DataFilter.perform_bandstop(data[i + 1], sampling_rate, bandStopFrequency, 4.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)  # 노치 필터
            DataFilter.perform_bandpass(data[i + 1], sampling_rate, bp_centerFreq, bp_bandWidth, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)  # 대역 통과 필터

        bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, True)  # 채널별 데이터 대역 파워의 평균 및 표준편차 계산
        feature_vector = np.concatenate((bands[0], bands[1]))  # 대역 평균[0], 표준편차[1] 취합

        focusing.prepare()  # 분류 준비
        prediction = focusing.predict(feature_vector)  # 예측값 생성
        print('Focusing: %f' % prediction)
        focusing.release()  # 분류 종료
        trial += 1  # 예측 데이터 생성 횟수 갱신

        if prediction > threshold:  # 예측값이랑 임계값 비교후 아두이노에 전송
            ser.write(b'1')  # 집중 상태로 판단
            focusing_point += 1  # 집중 데이터 갯수 증가
            continuous_focusing_point += 1  # 지속적인 집중 판단을 위해 값 갱신
        else:
            ser.write(b'0')  # 비집중 상태로 판단
            if continuous_focusing_point >= 3:  # 이전 텀에서 집중으로 판단된 횟수가 3이상이라면
                continuous_focusing_table.append(continuous_focusing_point)  # 해당 정보 기록
            continuous_focusing_point = 0  # 집중이 끊어지면 새로운 값을 기록하기 위해 초기화

        if keyboard.is_pressed('space'):
            continuous_focusing_table.append(continuous_focusing_point)  # 집중이 지속되는 상태에서 종료했을 때 값 손실을 막기위해
            break

    board.stop_stream()
    board.release_session()
    # 스트림 종료

    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'Stream end')  # 스트림 종료 메시지 출력
    x = np.arange(4)
    trial_label = ['Trial', 'Focusing', 'Continuous', 'Maximum']  # 스트림 횟수, 집중 횟수, 지속적인 집중 횟수, 최대 지속 계산 텀
    if len(continuous_focusing_table) != 0:
        maximum = max(continuous_focusing_table)
    else:
        maximum = 0
    trial_value = [trial, focusing_point, len(continuous_focusing_table), maximum]
    plt.bar(x, trial_value)
    plt.xticks(x, trial_label)
    plt.show()
    # 데이터 스트림 횟수와 그 중 집중한 횟수 시각화
    print('\nYour Result: {:.2f}'.format((focusing_point / trial) * 100))
    print('Press enter to exit..')
    exit = input()


if __name__ == "__main__":
    main()