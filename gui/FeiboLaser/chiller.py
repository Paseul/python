# sudo chmod 666 /dev/ttyUSB0
# ls -al /dev/ttyUSB*

from threading import *
import serial
import signal
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import struct
import numpy as np
import datetime

line = [] #라인 단위로 데이터 가져올 리스트 변수

port = 'COM8' # 시리얼 포트
baud = 19200 # 시리얼 보드레이트(통신속도)

class Signal(QObject):
  recv_signal = pyqtSignal(str, str, str, str)
  disconn_signal = pyqtSignal()


class SerialSocket:

  def __init__(self, parent):
    self.parent = parent

    self.recv = Signal()
    self.recv.recv_signal.connect(self.parent.updateChiller)
    self.disconn = Signal()
    self.disconn.disconn_signal.connect(self.parent.disconnectChiller)

    self.line = [] #라인 단위로 데이터 가져올 리스트 변수

    self.rcvFlag = False
    self.bConnect = False
    self.size = 0

  #쓰레드 종료용 시그널 함수+
  def handler(signum, frame):
    self.bConnect = True

  def __del__(self):
    self.stop()

  def connect(self):
    #종료 시그널 등록
    signal.signal(signal.SIGINT, self.handler)

    self.ser = serial.Serial(port, baud, timeout=1)
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
      self.size = 0
      for c in ser.readline():
        self.rcvFlag = True
        self.line.append(chr(c))
        self.size += 1

      if self.rcvFlag:
        cmd = ''.join(self.line[1:4])
        sc = self.line[4]
        len = ''.join(self.line[5:7])
        data = ''.join(self.line[7:self.size - 1])

        self.recv.recv_signal.emit(cmd, sc, len, data)
        del self.line[:]
        self.rcvFlag = False

    self.stop()

  def send(self, cmd, sc, length, data):
    sendPacket = []
    temp = (cmd+sc+length+data).encode()
    sendPacket.append(0x02)
    for c in temp:
      sendPacket.append(c)
    sendPacket.append(0x03)
    self.ser.write(sendPacket)