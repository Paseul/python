from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import struct
import numpy as np
import threading
import socket
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024

class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        # 클라이언트 쪽에서 UDP 소켓 생성
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.seqNum = 0

    def __del__(self):
        print("Quit")

    def initUI(self):
        self.setWindowTitle('FSM 제어 프로그램')

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

        # Mode
        self.ModeMsg = QTextEdit()
        self.ModeMsg.setFixedHeight(30)
        self.ModeMsg.setText('4')
        messageBox.addWidget(self.ModeMsg)
        # Tilt
        self.tiltMsg = QTextEdit()
        self.tiltMsg.setFixedHeight(30)
        self.tiltMsg.setText('1')
        messageBox.addWidget(self.tiltMsg)
        # data
        self.tipMsg = QTextEdit()
        self.tipMsg.setFixedHeight(30)
        self.tipMsg.setText('1')
        messageBox.addWidget(self.tipMsg)
        # 전송
        self.sendBtn = QPushButton('보내기')
        self.sendBtn.setAutoDefault(True)
        self.sendBtn.clicked.connect(self.defaultMsg)
        messageBox.addWidget(self.sendBtn)
        # 채팅창 삭제
        self.clearBtn = QPushButton('채팅창 지움')
        self.clearBtn.clicked.connect(self.clearMsg)        
        messageBox.addWidget(self.clearBtn)

        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(infobox)
        self.setLayout(vbox)

        self.show()

    def defaultMsg(self):
        mode = int(self.ModeMsg.toPlainText())
        tilt = int(self.tiltMsg.toPlainText())
        tip = int(self.tipMsg.toPlainText())
        checksum = mode + tilt + tip + self.seqNum

        print(self.seqNum)

        values = (mode, tilt, tip, (self.seqNum % pow(2, 32)), (checksum % pow(2, 32)))
        fmt = '>I i i I I'
        packer = struct.Struct(fmt)
        bytesToSend = packer.pack(*values)

        print(bytesToSend)

        self.UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        self.seqNum += 1

    def clearMsg(self):
        self.recvmsg.clear()

    def closeEvent(self, e):
        print("Close")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())