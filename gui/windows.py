from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import socket
import server
import struct
import numpy as np
from struct import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

port = 5000


class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.s = server.ServerSocket(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('서버')

        # 서버 설정 부분
        ipbox = QHBoxLayout()

        gb = QGroupBox('서버 설정')
        ipbox.addWidget(gb)

        box = QHBoxLayout()

        label = QLabel('Server IP')
        self.ip = QLineEdit(socket.gethostbyname(socket.gethostname()))
        box.addWidget(label)
        box.addWidget(self.ip)

        label = QLabel('Server Port')
        self.port = QLineEdit(str(port))
        box.addWidget(label)
        box.addWidget(self.port)

        self.btn = QPushButton('서버 실행')
        self.btn.setCheckable(True)
        self.btn.toggled.connect(self.toggleButton)
        box.addWidget(self.btn)

        gb.setLayout(box)

        # 접속자 정보 부분
        infobox = QHBoxLayout()
        gb = QGroupBox('접속자 정보')
        infobox.addWidget(gb)

        box = QHBoxLayout()

        self.guest = QTableWidget()
        self.guest.setRowCount(5)
        self.guest.setColumnCount(2)
        self.guest.setHorizontalHeaderItem(0, QTableWidgetItem('ip'))
        self.guest.setHorizontalHeaderItem(1, QTableWidgetItem('port'))

        box.addWidget(self.guest)
        gb.setLayout(box)

        # 채팅창 부분
        gb = QGroupBox('메시지')
        infobox.addWidget(gb)

        box = QVBoxLayout()

        label = QLabel('받은 메시지')
        box.addWidget(label)

        self.msg = QListWidget()
        box.addWidget(self.msg)

        label = QLabel('보낼 메시지')
        box.addWidget(label)

        hbox = QHBoxLayout()
        box.addLayout(hbox)

        # Header
        self.headerMsg = QTextEdit()
        self.headerMsg.setFixedHeight(30)
        self.headerMsg.setText('1')
        hbox.addWidget(self.headerMsg)
        # Cmd
        self.cmdMsg = QTextEdit()
        self.cmdMsg.setFixedHeight(30)
        self.cmdMsg.setText('4')
        hbox.addWidget(self.cmdMsg)
        # data
        self.dataLen = QTextEdit()
        self.dataLen.setFixedHeight(30)
        self.dataLen.setText('12')
        hbox.addWidget(self.dataLen)
        # data
        self.data1 = QTextEdit()
        self.data1.setFixedHeight(30)
        self.data1.setText('FF')
        hbox.addWidget(self.data1)
        # Header
        self.data2 = QTextEdit()
        self.data2.setFixedHeight(30)
        self.data2.setText('42C8')
        hbox.addWidget(self.data2)
        # Cmd
        self.data3 = QTextEdit()
        self.data3.setFixedHeight(30)
        self.data3.setText('1212')
        hbox.addWidget(self.data3)
        # # data
        # self.data4 = QTextEdit()
        # self.data4.setFixedHeight(30)
        # self.data4.setText('4212')
        # hbox.addWidget(self.data4)
        # data
        self.data5 = QTextEdit()
        self.data5.setFixedHeight(30)
        self.data5.setText('1')
        hbox.addWidget(self.data5)
        # # data
        # self.data6 = QTextEdit()
        # self.data6.setFixedHeight(30)
        # self.data6.setText('672')
        # hbox.addWidget(self.data6)
        # # data
        # self.data7 = QTextEdit()
        # self.data7.setFixedHeight(30)
        # self.data7.setText('673')
        # hbox.addWidget(self.data7)

        hbox = QHBoxLayout()

        # self.sendmsg = QLineEdit()
        # box.addWidget(self.sendmsg)

        # hbox = QHBoxLayout()

        self.sendbtn = QPushButton('보내기')
        self.sendbtn.clicked.connect(self.sendMsg)
        hbox.addWidget(self.sendbtn)

        self.clearbtn = QPushButton('채팅창 지움')
        self.clearbtn.clicked.connect(self.clearMsg)
        hbox.addWidget(self.clearbtn)

        box.addLayout(hbox)

        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(ipbox)
        vbox.addLayout(infobox)
        self.setLayout(vbox)

        self.show()

    def toggleButton(self, state):
        if state:
            ip = self.ip.text()
            port = self.port.text()
            if self.s.start(ip, int(port)):
                self.btn.setText('서버 종료')
        else:
            self.s.stop()
            self.msg.clear()
            self.btn.setText('서버 실행')

    def updateClient(self):
        self.guest.clearContents()
        i = 0
        for ip in self.s.ip:
            self.guest.setItem(i, 0, QTableWidgetItem(ip[0]))
            self.guest.setItem(i, 1, QTableWidgetItem(str(ip[1])))
            i += 1

    def updateMsg(self, header, cmd, addr, data):
        self.msg.addItem(QListWidgetItem(header))
        self.msg.addItem(QListWidgetItem(cmd))
        self.msg.addItem(QListWidgetItem(addr))
        self.msg.addItem(QListWidgetItem(data))
        self.msg.setCurrentRow(self.msg.count() - 1)

    def sendMsg(self):
        # if not self.s.bListen:
        #     self.sendmsg.clear()
        #     return
        # sendmsg = self.sendmsg.text()
        # self.updateMsg(sendmsg)
        # print(sendmsg)

        header = int(self.headerMsg.toPlainText(), 16)
        cmd = int(self.cmdMsg.toPlainText(), 16)
        datalen = int(self.dataLen.toPlainText(), 16)
        datan1 = int(self.data1.toPlainText(), 16)
        datan2 = int(self.data2.toPlainText(), 16)
        datan3 = int(self.data3.toPlainText(), 16)
        # datan4 = int(self.data4.toPlainText(), 16)
        datan5 = int(self.data5.toPlainText(), 16)
        # datan6 = int(self.data6.toPlainText(), 16)
        # datan7 = int(self.data7.toPlainText(), 16)

        values = (header, cmd, datalen, datan1, datan2, datan3, datan5)
        fmt = '>B B B B H H B'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)

        # self.c.send(sendData)

        self.s.send(sendData)
        # self.sendmsg.clear()

    def clearMsg(self):
        self.msg.clear()

    def closeEvent(self, e):
        self.s.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())