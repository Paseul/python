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

port = 'COM7' # 시리얼 포트
baud = 115200 # 시리얼 보드레이트(통신속도)

class Signal(QObject):
  recv_signal = pyqtSignal(str, str)
  disconn_signal = pyqtSignal()


class SerialSocket:

  def __init__(self, parent):
    self.parent = parent

    self.recv = Signal()
    self.recv.recv_signal.connect(self.parent.updateLaser)
    self.disconn = Signal()
    self.disconn.disconn_signal.connect(self.parent.disconnectLaser)

    self.line = [] #라인 단위로 데이터 가져올 리스트 변수

    self.rcvFlag = False
    self.cmdFlag = False
    self.bConnect = False

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
      for c in ser.readline():  
        #line 변수에 차곡차곡 추가하여 넣는다.      
        self.rcvFlag = True
        if chr(c) == '=':
          self.cmdFlag = True
          cmd = ''.join(self.line)
          self.line = []
          continue
        if chr(c) == ',':
          data = ''.join(self.line)
          if cmd == 'TOFW' or cmd == 'TMONRT' or cmd == 'ENVC' or cmd == 'PD':
            self.line.append(chr(c))
            continue
          else:
            self.recv.recv_signal.emit(cmd, data)
            del self.line[:]
            continue
        self.line.append(chr(c))
      if self.rcvFlag and self.cmdFlag:         
        data = ''.join(self.line)       
        self.recv.recv_signal.emit(cmd, data)
        del self.line[:]
        self.rcvFlag = False
      elif self.rcvFlag and self.cmdFlag==False:
        cmd = ''.join(self.line)
        data=''        
        self.recv.recv_signal.emit(cmd, data)
        del self.line[:]
        self.cmdFlag = False
        self.rcvFlag = False

    self.stop()

  def send(self, cmd, data):
    self.ser.write((cmd+data).encode())