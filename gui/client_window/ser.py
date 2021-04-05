# sudo chmod 666 /dev/ttyUSB0
# ls -al /dev/ttyUSB*

from threading import *
import serial
import signal
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import struct
import numpy as np

line = [] #라인 단위로 데이터 가져올 리스트 변수

port = '/dev/ttyUSB0' # 시리얼 포트
baud = 115200 # 시리얼 보드레이트(통신속도)

class Signal(QObject):
    recv_signal = pyqtSignal(int, int, int, int, int, int, int)
    disconn_signal = pyqtSignal()


class SerialSocket:

    def __init__(self, parent):
        self.parent = parent

        self.recv = Signal()
        self.recv.recv_signal.connect(self.parent.updatePower)
        self.disconn = Signal()
        self.disconn.disconn_signal.connect(self.parent.powerDisconnect)

        self.line = [] #라인 단위로 데이터 가져올 리스트 변수

        self.bConnect = False

    #쓰레드 종료용 시그널 함수+
    def handler(signum, frame):
        self.bConnect = True

    def __del__(self):
        self.stop()

    def connect(self):
        #종료 시그널 등록
        signal.signal(signal.SIGINT, self.handler)
    
        self.ser = serial.Serial(port, baud, timeout=0)
        self.bConnect = True
        self.t = Thread(target=self.receive, args=(self.ser,))
        self.t.daemon = True
        self.t.start()
        print('Connected')

        return True

    def stop(self):
        self.bConnect = False
        if hasattr(self, 'client'):
            self.ser.close()
            del (self.ser)
            print('Client Stop')
            self.disconn.disconn_signal.emit()

    def receive(self, ser):
        while self.bConnect:
            #데이터가 있있다면
            for c in self.ser.read():
                #line 변수에 차곡차곡 추가하여 넣는다.
                self.line.append(c)
                if self.line[0] != 2:
                    del self.line[:]
                    continue
                if len(self.line) == 20 and c == 3:  #라인의 끝을 만나면..
                    #데이터 처리 함수로 호출
                    max_length = len(self.line)
                    max_volt = self.line[4]<<8 | self.line[3]
                    min_volt = self.line[6]<<8 | self.line[5]
                    max_temp = self.line[8]<<8 | self.line[7]
                    min_temp = self.line[10]<<8 | self.line[9]
                    s_o_charge = self.line[12]<<8 | self.line[11]
                    a_capacity = self.line[14]<<8 | self.line[13]
                    t_t_discharge = self.line[16]<<8 | self.line[15]
                    self.recv.recv_signal.emit(max_volt, min_volt, max_temp, min_temp, s_o_charge, a_capacity, t_t_discharge)
                    #line 변수 초기화
                    del self.line[:]
                elif if len(self.line) == 20:
                    print(self.line)
                    del self.line[:]
        self.stop()
