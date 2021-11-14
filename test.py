import time
import serial
import numpy as np

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, NoiseTypes, WindowFunctions, DetrendOperations
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams
threshold = 0.8

def main():
    BoardShim.enable_dev_board_logger()  # 보드 연결시 상태 확인 메시지 활성화
    MLModel.disable_ml_logger()  # 예측값 출력시 발생하는 메시지 비활성화

    params = BrainFlowInputParams()  # 연결 설정 라이브러리 구조체 불러오기
    params.board_id = BoardIds.CYTON_BOARD.value  # 연결할 보드 id 설정
    params.serial_port = 'COM5'  # 연결할 보드의 통신 보드 포트 설정 ex)wifi shield, dongle이 통신 보드

    board = BoardShim(params.board_id, params)  # 보드 설정 라이브러리 구조체 불러오기
    sampling_rate = BoardShim.get_sampling_rate(params.board_id)  # 보드 자체에 설정된 샘플링 레이트 불러오기, OpenBCI는 250Hz
    eeg_channels = BoardShim.get_eeg_channels(params.board_id)  # 보드의 채널 불러오기, Cyton은 8채널이므로 [1, 2, .. ,7 ,8]의 형태
    eeg_channels = eeg_channels[:2]  # 사용할 채널이 1,2이므로 불러온 채널리스트를 슬라이싱

    concentration_params = BrainFlowModelParams(BrainFlowMetrics.CONCENTRATION.value, BrainFlowClassifiers.REGRESSION.value)  # ML 라이브러리 불러와서 모델 값 설정
    concentration = MLModel(concentration_params)  # ML 모델 생성

    #ser = serial.Serial('COM6', 9600)  # 아두이노 포트 및 보드레이트 설정
    
    board.prepare_session()  # 보드 연결 준비
    board.start_stream()  # 보드 스트림 시작
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')  # 스트림 시작시 메시지 출력

    while True:
        time.sleep(5)  # 계산 텀 설정
        data = board.get_board_data()  # 보드에서 데이터 읽어오기
        #DataFilter.remove_environmental_noise(data[0], sampling_rate, 1)
        #DataFilter.remove_environmental_noise(data[1], sampling_rate, 1)
        for count, channel in enumerate(eeg_channels):
            # filters work in-place
            if count == 0:
                DataFilter.perform_bandpass(data[channel], BoardShim.get_sampling_rate(params.board_id), 15.0, 6.0, 4, FilterTypes.BESSEL.value, 0)
            elif count == 1:
                DataFilter.perform_bandstop(data[channel], BoardShim.get_sampling_rate(params.board_id), 30.0, 1.0, 3, FilterTypes.BUTTERWORTH.value, 0)
            elif count == 2:
                DataFilter.perform_lowpass(data[channel], BoardShim.get_sampling_rate(params.board_id), 20.0, 5, FilterTypes.CHEBYSHEV_TYPE_1.value, 1)
            elif count == 3:
                DataFilter.perform_highpass(data[channel], BoardShim.get_sampling_rate(params.board_id), 3.0, 4, FilterTypes.BUTTERWORTH.value, 0)
            elif count == 4:
                DataFilter.perform_rolling_filter(data[channel], 3, AggOperations.MEAN.value)
            else:
                DataFilter.remove_environmental_noise(data[channel], BoardShim.get_sampling_rate(params.board_id), NoiseTypes.FIFTY.value)

        bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, True)  # 채널별 데이터 대역 파워의 평균 및 표준편차 계산
        feature_vector = np.concatenate((bands[0], bands[1]))  # 대역 평균[0], 표준편차[1] 취합

        concentration.prepare()  # 분류 준비
        prediction = concentration.predict(feature_vector)  # 예측값 생성
        print(f'Concentration: %f' % prediction)
        concentration.release()  # 분류 종료

        '''
        if prediction > threshold:  # 예측값이랑 임계값 비교후 아두이노에 전송
            ser.write(b'1')  # 집중 상태로 판단
        else:
            ser.write(b'0')  # 비집중 상태로 판단'''

    board.stop_stream()
    board.release_session()
    # 스트림 종료

if __name__ == "__main__":
    main()