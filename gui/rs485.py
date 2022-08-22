# sudo chmod 666 /dev/ttyUSB0

import serial
from serial import rs485
import threading
import time

line = []  # 라인 단위로 데이터 가져올 변수
port = 'COM7' # 시리얼 포트
baud = 115200  # 시리얼 보드레이트(통신속도)

ser = serial.Serial(port, baud, timeout=3)

def run():
    ser.rs485_mode = serial.rs485.RS485Settings()
    ser.write(b'hello')

while True:
    run()
