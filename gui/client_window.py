from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import client
import struct
import numpy as np
from struct import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

port = 5000


class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.c = client.ClientSocket(self)

        self.initUI()

    def __del__(self):
        self.c.stop()

    def initUI(self):
        self.setWindowTitle('클라이언트')

        # 클라이언트 설정 부분
        ipbox = QHBoxLayout()

        gb = QGroupBox('서버 설정')
        ipbox.addWidget(gb)

        box = QHBoxLayout()

        label = QLabel('Server IP')
        self.ip = QLineEdit()
        self.ip.setInputMask('127.0.1.1;_')
        box.addWidget(label)
        box.addWidget(self.ip)

        label = QLabel('Server Port')
        self.port = QLineEdit(str(port))
        box.addWidget(label)
        box.addWidget(self.port)

        self.btn = QPushButton('접속')
        self.btn.clicked.connect(self.connectClicked)
        box.addWidget(self.btn)

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

        # Header
        self.headerMsg = QTextEdit()
        self.headerMsg.setFixedHeight(30)
        self.headerMsg.setText('41')
        box.addWidget(self.headerMsg)
        # Cmd
        self.cmdMsg = QTextEdit()
        self.cmdMsg.setFixedHeight(30)
        self.cmdMsg.setText('01')
        box.addWidget(self.cmdMsg)
        # data
        self.dataMsg = QTextEdit()
        self.dataMsg.setFixedHeight(30)
        self.dataMsg.setText('1234')
        box.addWidget(self.dataMsg)

        hbox = QHBoxLayout()

        box.addLayout(hbox)
        self.sendbtn = QPushButton('보내기')
        self.sendbtn.setAutoDefault(True)
        self.sendbtn.clicked.connect(self.sendMsg)

        self.clearbtn = QPushButton('채팅창 지움')
        self.clearbtn.clicked.connect(self.clearMsg)

        hbox.addWidget(self.sendbtn)
        hbox.addWidget(self.clearbtn)
        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(ipbox)
        vbox.addLayout(infobox)
        self.setLayout(vbox)

        self.show()

    def connectClicked(self):
        if self.c.bConnect == False:
            ip = self.ip.text()
            port = self.port.text()
            if self.c.connectServer(ip, int(port)):
                self.btn.setStyleSheet("background-color: green")
                self.btn.setText('접속 종료')
            else:
                self.c.stop()
                self.recvmsg.clear()
                self.btn.setText('접속')
        else:
            self.c.stop()
            self.recvmsg.clear()
            self.btn.setText('접속')

    def updateMsg(self, msg):
        self.recvmsg.addItem(QListWidgetItem(msg))

    def updateDisconnect(self):
        self.btn.setText('접속')

    def sendMsg(self):
        header = int(self.headerMsg.toPlainText(), 16)
        cmd = int(self.cmdMsg.toPlainText(), 16)
        # float 적용
        # data = float(self.dataMsg.toPlainText())
        # data = np.uint16(data)        
        data = int(self.dataMsg.toPlainText(), 16)

        values = (header, cmd, data)
        fmt = '>B B H'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)
        print(sendData[0])

        self.c.send(sendData)

    def clearMsg(self):
        self.recvmsg.clear()

    def closeEvent(self, e):
        self.c.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())