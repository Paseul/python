from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import ser
import struct
import numpy as np
import threading
from time import sleep
from struct import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

port = 5000
ip = '192.168.0.99' #'127.0.1.1'
coolerPort = 502
coolerIp = '192.168.0.3'
coolerIp2 = '192.168.0.4'

class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.ser = ser.SerialSocket(self)

        self.initUI()

    def __del__(self):
        print('delete')

    def initUI(self):
        self.setWindowTitle('KC4AF 제어 프로그램')

        # 전원 제어부
        lensControlBox = QHBoxLayout()

        gb = QGroupBox('렌즈 제어부')
        lensControlBox.addWidget(gb)

        box = QVBoxLayout()

        # 전원 BIT
        controlBtnBox = QHBoxLayout()
        box.addLayout(controlBtnBox)

        self.p_Btn = QPushButton('접속')
        self.p_Btn.clicked.connect(self.powerConnect)
        controlBtnBox.addWidget(self.p_Btn)

        self.focusNearBtn = QPushButton('Focus Near')
        self.focusNearBtn.clicked.connect(self.focusNear)
        controlBtnBox.addWidget(self.focusNearBtn)

        self.focusWideBtn = QPushButton('Focus Wide')
        self.focusWideBtn.clicked.connect(self.focusWide)
        controlBtnBox.addWidget(self.focusWideBtn)

        self.zoomWideBtn = QPushButton('Zoom Wide')
        self.zoomWideBtn.clicked.connect(self.zoomWide)
        controlBtnBox.addWidget(self.zoomWideBtn)

        self.zoomTeleBtn = QPushButton('Zoom Tele')
        self.zoomTeleBtn.clicked.connect(self.zoomTele)
        controlBtnBox.addWidget(self.zoomTeleBtn)

        self.irisCloseBtn = QPushButton('Iris Close')
        self.irisCloseBtn.clicked.connect(self.irisClose)
        controlBtnBox.addWidget(self.irisCloseBtn)

        self.irisOpenBtn = QPushButton('Iris Open')
        self.irisOpenBtn.clicked.connect(self.irisOpen)
        controlBtnBox.addWidget(self.irisOpenBtn)

        self.stopBtn = QPushButton('Stop')
        self.stopBtn.clicked.connect(self.stop)
        controlBtnBox.addWidget(self.stopBtn)

        gb.setLayout(box)

        # 채팅창 부분
        infobox = QHBoxLayout()
        gb = QGroupBox('메시지')
        infobox.addWidget(gb)

        box = QVBoxLayout()

        label = QLabel('받은 메시지')
        box.addWidget(label)

        self.recvmsg = QListWidget()
        box.addWidget(self.recvmsg)

        label = QLabel('보낼 메시지')
        box.addWidget(label)

        messageBox = QHBoxLayout()
        box.addLayout(messageBox)

        # Header
        self.headerMsg = QTextEdit()
        self.headerMsg.setFixedHeight(30)
        self.headerMsg.setText('29')
        messageBox.addWidget(self.headerMsg)
        # Cmd
        self.cmdMsg = QTextEdit()
        self.cmdMsg.setFixedHeight(30)
        self.cmdMsg.setText('01')
        messageBox.addWidget(self.cmdMsg)
        # data
        self.dataMsg = QTextEdit()
        self.dataMsg.setFixedHeight(30)
        self.dataMsg.setText('0001')
        messageBox.addWidget(self.dataMsg)
        # 채팅창 삭제
        self.clearBtn = QPushButton('채팅창 지움')
        self.clearBtn.clicked.connect(self.clearMsg)        
        messageBox.addWidget(self.clearBtn)

        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(lensControlBox)
        vbox.addLayout(infobox)
        self.setLayout(vbox)

        self.show()

    def powerConnect(self):
        if self.ser.bConnect == False:
            if self.ser.connect():
                self.p_Btn.setStyleSheet("background-color: green")
                self.p_Btn.setText('접속 종료')
                self.serConnect = True
            else:
                self.ser.stop()
                self.recvmsg.clear()
                self.p_Btn.setText('접속')
                self.p_Btn.setStyleSheet("background-color: lightgray")
                self.serConnect = False
        else:
            self.ser.stop()
            self.recvmsg.clear()
            self.p_Btn.setText('접속')
            self.p_Btn.setStyleSheet("background-color: lightgray")
            self.serConnect = False

    def focusNear(self):
        self.ser.send(1, 1, 0)

    def focusWide(self):
        self.ser.send(1, 0, 128)

    def zoomWide(self):
        self.ser.send(1, 0, 64)

    def zoomTele(self):
        self.ser.send(1, 0, 32)

    def irisClose(self):
        self.ser.send(1, 4, 0)

    def irisOpen(self):
        self.ser.send(1, 2, 0)

    def stop(self):
        self.ser.send(1, 0, 0)

    def updatePower(self, msg):
        self.recvmsg.addItem(msg)

    def powerDisconnect(self):
        self.p_btn.setText('접속')  

    def swap16(self, x):
        return ((x << 8) & 0xFF00 |
               ((x >> 8) & 0x00FF))

    def clearMsg(self):
        self.recvmsg.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())