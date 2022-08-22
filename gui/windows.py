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

ip = '127.0.0.1'
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
        self.ip = QLineEdit(ip)
        # self.ip = QLineEdit(socket.gethostbyname(socket.gethostname()))
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
        self.ack1 = QTextEdit()
        self.ack1.setFixedHeight(30)
        self.ack1.setText('AC')
        hbox.addWidget(self.ack1)
        # Cmd
        self.ack2 = QTextEdit()
        self.ack2.setFixedHeight(30)
        self.ack2.setText('13')
        hbox.addWidget(self.ack2)
        # data
        self.source = QTextEdit()
        self.source.setFixedHeight(30)
        self.source.setText('2')
        hbox.addWidget(self.source)
        # data
        self.destination = QTextEdit()
        self.destination.setFixedHeight(30)
        self.destination.setText('1')
        hbox.addWidget(self.destination)
        # Header
        self.opcode = QTextEdit()
        self.opcode.setFixedHeight(30)
        self.opcode.setText('5')
        hbox.addWidget(self.opcode)
        # Cmd
        self.dataSize = QTextEdit()
        self.dataSize.setFixedHeight(30)
        self.dataSize.setText('7')
        hbox.addWidget(self.dataSize)
        # data
        self.seqNum = QTextEdit()
        self.seqNum.setFixedHeight(30)
        self.seqNum.setText('1')
        hbox.addWidget(self.seqNum)
        # data
        self.data1 = QTextEdit()
        self.data1.setFixedHeight(30)
        self.data1.setText('2')
        hbox.addWidget(self.data1)
        # data
        self.data2 = QTextEdit()
        self.data2.setFixedHeight(30)
        self.data2.setText('FF')
        hbox.addWidget(self.data2)
        # data
        self.data3 = QTextEdit()
        self.data3.setFixedHeight(30)
        self.data3.setText('FF')
        hbox.addWidget(self.data3)
        # data
        self.data4 = QTextEdit()
        self.data4.setFixedHeight(30)
        self.data4.setText('FF')
        hbox.addWidget(self.data4)
        # data
        self.data5 = QTextEdit()
        self.data5.setFixedHeight(30)
        self.data5.setText('FF')
        hbox.addWidget(self.data5)
        # data
        self.data6 = QTextEdit()
        self.data6.setFixedHeight(30)
        self.data6.setText('FF')
        hbox.addWidget(self.data6)
        # data
        self.data7 = QTextEdit()
        self.data7.setFixedHeight(30)
        self.data7.setText('FF')
        hbox.addWidget(self.data7)
        # data
        self.data8 = QTextEdit()
        self.data8.setFixedHeight(30)
        self.data8.setText('FF')
        hbox.addWidget(self.data8)
        # data
        self.data9 = QTextEdit()
        self.data9.setFixedHeight(30)
        self.data9.setText('FF')
        hbox.addWidget(self.data9)
        # data
        self.checksum = QTextEdit()
        self.checksum.setFixedHeight(30)
        self.checksum.setText('FF')
        hbox.addWidget(self.checksum)
        # data
        self.etx1 = QTextEdit()
        self.etx1.setFixedHeight(30)
        self.etx1.setText('E7')
        hbox.addWidget(self.etx1)
        # data
        self.etx2 = QTextEdit()
        self.etx2.setFixedHeight(30)
        self.etx2.setText('E8')
        hbox.addWidget(self.etx2)

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

    def updateMsg(self, header):
        self.msg.addItem(QListWidgetItem(header))
        # self.msg.addItem(QListWidgetItem(cmd))
        # self.msg.addItem(QListWidgetItem(addr))
        # self.msg.addItem(QListWidgetItem(data))
        self.msg.setCurrentRow(self.msg.count() - 1)

    def sendMsg(self):
        # if not self.s.bListen:
        #     self.sendmsg.clear()
        #     return
        # sendmsg = self.sendmsg.text()
        # self.updateMsg(sendmsg)
        # print(sendmsg)

        ack1 = int(self.ack1.toPlainText(), 16)
        ack2 = int(self.ack2.toPlainText(), 16)
        source = int(self.source.toPlainText(), 16)
        destination = int(self.destination.toPlainText(), 16)
        opcode = int(self.opcode.toPlainText(), 16)
        dataSize = int(self.dataSize.toPlainText(), 16)
        seqNum = int(self.seqNum.toPlainText(), 16)
        data1 = int(self.data1.toPlainText(), 16)
        data2 = int(self.data2.toPlainText(), 16)
        data3 = int(self.data3.toPlainText(), 16)
        data4 = int(self.data4.toPlainText(), 16)
        data5 = int(self.data5.toPlainText(), 16)
        data6 = int(self.data6.toPlainText(), 16)
        data7 = int(self.data7.toPlainText(), 16)
        data8 = int(self.data8.toPlainText(), 16)
        data9 = int(self.data9.toPlainText(), 16)
        checksum = int(self.checksum.toPlainText(), 16)
        etx1 = int(self.etx1.toPlainText(), 16)
        etx2 = int(self.etx2.toPlainText(), 16)
        dummy = 0

        values = (ack1, ack2, source, destination, opcode, dataSize, seqNum, data1, data2, data3, data4, data5, data6, data7, data8, data9, checksum, etx1, etx2)
        fmt = '>B B B B B H H B B B B B B B B B B B B'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)
        print(sendData)

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