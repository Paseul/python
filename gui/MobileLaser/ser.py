# sudo chmod 666 /dev/ttyUSB0
# ls -al /dev/ttyUSB*

from multiprocessing import Process, Queue
import serial
import signal
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import struct
import numpy as np
import csv
import datetime

line = [] #라인 단위로 데이터 가져올 리스트 변수

port = 'COM16' # 시리얼 포트
baud = 9600 # 시리얼 보드레이트(통신속도)

class Signal(QObject):
    recv_signal = pyqtSignal(str)
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
        self.t = Process(target=self.receive, args=(self.ser,))
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
        try:
            while self.bConnect:
                #데이터가 있있다면
                if self.ser.read() == True:
                    self.recv.recv_signal.emit(ser.read())
            self.stop()
        except:
            pass

    def send(self, address, command1, command2):
        sync = 255
        data1 = 0
        data2 = 0
        checksum = address + command1 + command2 + data1 + data2

        values = (sync, address, command1, command2, data1, data2, checksum)
        fmt = '>B B B B B B B'
        packer = struct.Struct(fmt)
        bytesToSend = packer.pack(*values)
        print(bytesToSend)

        self.ser.write(bytesToSend)
