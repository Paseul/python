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
ip = '127.0.1.1'


class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.c = client.ClientSocket(self)
        self.connect = False
        self.mainStart = False
        self.ldStart = False
        self.ld1 = False
        self.ld2 = False
        self.ld3 = False
        self.ld4 = False
        self.ld5 = False

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
        self.ip = QLineEdit(str(ip))

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

        # 버튼 설정
        btbox = QHBoxLayout()

        gb = QGroupBox('실행 버튼')
        btbox.addWidget(gb)

        box = QHBoxLayout()

        self.mainBtn = QPushButton('Start')
        self.mainBtn.clicked.connect(self.mainToggle)
        box.addWidget(self.mainBtn)

        self.ldBtn = QPushButton('LD Start')
        self.ldBtn.clicked.connect(self.ldToggle)
        box.addWidget(self.ldBtn)

        self.ld1Btn = QPushButton('LD No1')
        self.ld1Btn.clicked.connect(self.ld1On)
        box.addWidget(self.ld1Btn)

        self.ld2Btn = QPushButton('LD No2')
        self.ld2Btn.clicked.connect(self.ld2On)
        box.addWidget(self.ld2Btn)

        self.ld3Btn = QPushButton('LD No3')
        self.ld3Btn.clicked.connect(self.ld3On)
        box.addWidget(self.ld3Btn)

        self.ld4Btn = QPushButton('LD No4')
        self.ld4Btn.clicked.connect(self.ld4On)
        box.addWidget(self.ld4Btn)

        self.ld5Btn = QPushButton('LD No5')
        self.ld5Btn.clicked.connect(self.ld5On)
        box.addWidget(self.ld5Btn)

        self.interBtn = QPushButton('Interlock')
        self.interBtn.setEnabled(False)
        box.addWidget(self.interBtn)

        gb.setLayout(box)

        # 세부 설정
        bitbox = QHBoxLayout()

        gb = QGroupBox('BIT')
        bitbox.addWidget(gb)

        box = QVBoxLayout()

        hbox = QHBoxLayout()
        box.addLayout(hbox)

        label = QLabel('LD No.')
        hbox.addWidget(label)
        label = QLabel('Amp Set')
        hbox.addWidget(label)
        label = QLabel('Voltage')
        hbox.addWidget(label)
        label = QLabel('Amp')
        hbox.addWidget(label)

        # gb.setLayout(box)

        # LD1 설정
        ld1box = QHBoxLayout()
        box.addLayout(ld1box)

        self.ld1SetBtn = QPushButton('LD 1')
        self.ld1SetBtn.setAutoDefault(True)
        self.ld1SetBtn.clicked.connect(self.ld1AmpSet)
        ld1box.addWidget(self.ld1SetBtn)
        self.ld1Amp = QTextEdit()
        self.ld1Amp.setText('0.123')
        self.ld1Amp.setFixedHeight(27)
        ld1box.addWidget(self.ld1Amp)
        self.ld1VolRcv = QTextEdit()
        self.ld1VolRcv.setFixedHeight(27)
        ld1box.addWidget(self.ld1VolRcv)
        self.ld1AmpRcv = QTextEdit()
        self.ld1AmpRcv.setFixedHeight(27)
        ld1box.addWidget(self.ld1AmpRcv)

        # gb.setLayout(box)

        # LD2 설정
        ld2box = QHBoxLayout()
        box.addLayout(ld2box)

        self.ld2SetBtn = QPushButton('LD 2')
        self.ld2SetBtn.setAutoDefault(True)
        self.ld2SetBtn.clicked.connect(self.ld2AmpSet)
        ld2box.addWidget(self.ld2SetBtn)
        self.ld2Amp = QTextEdit()
        self.ld2Amp.setText('0.234')
        self.ld2Amp.setFixedHeight(27)
        ld2box.addWidget(self.ld2Amp)
        self.ld2VolRcv = QTextEdit()
        self.ld2VolRcv.setFixedHeight(27)
        ld2box.addWidget(self.ld2VolRcv)
        self.ld2AmpRcv = QTextEdit()
        self.ld2AmpRcv.setFixedHeight(27)
        ld2box.addWidget(self.ld2AmpRcv)

        # gb.setLayout(box)

        # LD3 설정
        ld3box = QHBoxLayout()
        box.addLayout(ld3box)

        self.ld3SetBtn = QPushButton('LD 3')
        self.ld3SetBtn.setAutoDefault(True)
        self.ld3SetBtn.clicked.connect(self.ld3AmpSet)
        ld3box.addWidget(self.ld3SetBtn)
        self.ld3Amp = QTextEdit()
        self.ld3Amp.setText('0.345')
        self.ld3Amp.setFixedHeight(27)
        ld3box.addWidget(self.ld3Amp)
        self.ld3VolRcv = QTextEdit()
        self.ld3VolRcv.setFixedHeight(27)
        ld3box.addWidget(self.ld3VolRcv)
        self.ld3AmpRcv = QTextEdit()
        self.ld3AmpRcv.setFixedHeight(27)
        ld3box.addWidget(self.ld3AmpRcv)

        # gb.setLayout(box)

        # LD4 설정
        ld4box = QHBoxLayout()
        box.addLayout(ld4box)

        self.ld4SetBtn = QPushButton('LD 4')
        self.ld4SetBtn.setAutoDefault(True)
        self.ld4SetBtn.clicked.connect(self.ld4AmpSet)
        ld4box.addWidget(self.ld4SetBtn)
        self.ld4Amp = QTextEdit()
        self.ld4Amp.setText('0.456')
        self.ld4Amp.setFixedHeight(27)
        ld4box.addWidget(self.ld4Amp)
        self.ld4VolRcv = QTextEdit()
        self.ld4VolRcv.setFixedHeight(27)
        ld4box.addWidget(self.ld4VolRcv)
        self.ld4AmpRcv = QTextEdit()
        self.ld4AmpRcv.setFixedHeight(27)
        ld4box.addWidget(self.ld4AmpRcv)

        # gb.setLayout(box)

        # LD5 설정
        ld5box = QHBoxLayout()
        box.addLayout(ld5box)

        self.ld5SetBtn = QPushButton('LD 5')
        self.ld5SetBtn.setAutoDefault(True)
        self.ld5SetBtn.clicked.connect(self.ld5AmpSet)
        ld5box.addWidget(self.ld5SetBtn)
        self.ld5Amp = QTextEdit()
        self.ld5Amp.setText('0.564')
        self.ld5Amp.setFixedHeight(27)
        ld5box.addWidget(self.ld5Amp)
        self.ld5VolRcv = QTextEdit()
        self.ld5VolRcv.setFixedHeight(27)
        ld5box.addWidget(self.ld5VolRcv)
        self.ld5AmpRcv = QTextEdit()
        self.ld5AmpRcv.setFixedHeight(27)
        ld5box.addWidget(self.ld5AmpRcv)

        # Temp 설정
        powerBox = QHBoxLayout()
        box.addLayout(powerBox)

        label = QLabel('1st Front Optical Power')
        powerBox.addWidget(label)
        self.frontPower = QTextEdit()
        self.frontPower.setFixedHeight(27)
        powerBox.addWidget(self.frontPower)

        label = QLabel('1st Rear Optical Power')
        powerBox.addWidget(label)
        self.rearPower = QTextEdit()
        self.rearPower.setFixedHeight(27)
        powerBox.addWidget(self.rearPower)

        # Temp 설정
        tempbox1 = QHBoxLayout()
        box.addLayout(tempbox1)

        label = QLabel('1st temp')
        tempbox1.addWidget(label)
        self.firstTemp = QTextEdit()
        self.firstTemp.setFixedHeight(27)
        tempbox1.addWidget(self.firstTemp)

        label = QLabel('2nd temp')
        tempbox1.addWidget(label)
        self.secondTemp = QTextEdit()
        self.secondTemp.setFixedHeight(27)
        tempbox1.addWidget(self.secondTemp)

        label = QLabel('3rd temp')
        tempbox1.addWidget(label)
        self.thirdTemp = QTextEdit()
        self.thirdTemp.setFixedHeight(27)
        tempbox1.addWidget(self.thirdTemp)

        tempbox2 = QHBoxLayout()
        box.addLayout(tempbox2)

        label = QLabel('3rd Plate temp')
        tempbox2.addWidget(label)
        self.thirdPlateTemp = QTextEdit()
        self.thirdPlateTemp.setFixedHeight(27)
        tempbox2.addWidget(self.thirdPlateTemp)

        label = QLabel('CLS')
        tempbox2.addWidget(label)
        self.clsTemp = QTextEdit()
        self.clsTemp.setFixedHeight(27)
        tempbox2.addWidget(self.clsTemp)

        label = QLabel('PUMP')
        tempbox2.addWidget(label)
        self.pumpTemp = QTextEdit()
        self.pumpTemp.setFixedHeight(27)
        tempbox2.addWidget(self.pumpTemp)

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

        hbox = QHBoxLayout()
        box.addLayout(hbox)

        # Header
        self.headerMsg = QTextEdit()
        self.headerMsg.setFixedHeight(30)
        self.headerMsg.setText('41')
        hbox.addWidget(self.headerMsg)
        # Cmd
        self.cmdMsg = QTextEdit()
        self.cmdMsg.setFixedHeight(30)
        self.cmdMsg.setText('01')
        hbox.addWidget(self.cmdMsg)
        # data
        self.dataMsg = QTextEdit()
        self.dataMsg.setFixedHeight(30)
        self.dataMsg.setText('1234')
        hbox.addWidget(self.dataMsg)

        hbox = QHBoxLayout()

        box.addLayout(hbox)
        self.sendBtn = QPushButton('보내기')
        self.sendBtn.setAutoDefault(True)
        self.sendBtn.clicked.connect(self.defaultMsg)

        self.clearBtn = QPushButton('채팅창 지움')
        self.clearBtn.clicked.connect(self.clearMsg)

        hbox.addWidget(self.sendBtn)
        hbox.addWidget(self.clearBtn)
        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(ipbox)
        vbox.addLayout(btbox)
        vbox.addLayout(bitbox)
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
                self.connect = True
            else:
                self.c.stop()
                self.recvmsg.clear()
                self.btn.setText('접속')
                self.btn.setStyleSheet("background-color: lightgray")
                self.connect = False
        else:
            self.c.stop()
            self.recvmsg.clear()
            self.btn.setText('접속')
            self.btn.setStyleSheet("background-color: lightgray")
            self.connect = False

    def updateMsg(self, header, cmd, data):
        if header == '0x41':
            if cmd == '0x7':
                # LD5 amp
                self.ld5AmpRcv.setText(str(round(((int(data)+207.5) / 3792.5), 4)))
            elif cmd == '0x8':
                # 1st Front Optical Power
                self.frontPower.setText(str(round(((int(data)+207.5) / 3792.5), 4)))
            elif cmd == '0x9':
                # 1st Rear Optical Power
                self.rearPower.setText(str(round(((int(data)+207.5) / 3792.5), 4)))
            elif cmd == '0xd':
                # Interlock
                if int(data) & 0b0001 == True:
                    self.interBtn.setStyleSheet("background-color: red")
                else:
                    self.interBtn.setStyleSheet("background-color: lightgray")
            elif cmd == '0xf':
                # LD5 vol
                self.ld5VolRcv.setText(str(round(((int(data)+207.5) / 3792.5), 4)))
            elif cmd == '0x10':
                # LD1 vol
                self.ld1VolRcv.setText(str(round((int(data)*0.0012 -0.0540), 4)))
            elif cmd == '0x11':
                # LD2 vol
                self.ld2VolRcv.setText(str(round((int(data)*0.0012 -0.0332), 4)))
            elif cmd == '0x12':
                # LD3 vol
                self.ld3VolRcv.setText(str(round((int(data)*0.0012 -0.0615), 4)))
            elif cmd == '0x13':
                # LD4 vol
                self.ld4VolRcv.setText(str(round((int(data)*0.0012 -0.0136), 4)))
            elif cmd == '0x14':
                # LD1 amp
                self.ld1AmpRcv.setText(str(round(((int(data)+608.0) / 3822.0), 4)))
            elif cmd == '0x15':
                # LD2 amp
                self.ld2AmpRcv.setText(str(round(((int(data)+132.5) / 3817.5), 4)))
            elif cmd == '0x16':
                # LD3 amp
                self.ld3AmpRcv.setText(str(round(((int(data)-432.5) / 3832.5), 4)))
            elif cmd == '0x17':
                # LD4 amp
                self.ld4AmpRcv.setText(str(round(((int(data)+542.5) / 3807.5), 4)))
            elif cmd == '0x18':
                # 1st temp
                self.firstTemp.setText(str(round(((1/((np.log(int(data)/26214.0) / 3950.0)+(1/298.0))-273.0)*1.1189 - 2.8153),4)))
            elif cmd == '0x19':
                # 2nd temp
                self.secondTemp.setText(str(round(((1/((np.log(int(data)/26214.0) / 3950.0)+(1/298.0))-273.0)*1.2161 - 4.8080), 4)))
            elif cmd == '0x1a':
                # 3rd temp
                self.thirdTemp.setText(str(round(((1/((np.log(int(data)/26214.0) / 3950.0)+(1/298.0))-273.0)*1.4021 - 8.7607), 4)))
            elif cmd == '0x1b':
                # 3rd plate temp
                self.thirdPlateTemp.setText(str(round(((1/((np.log(int(data)/26214.0) / 3950.0)+(1/298.0))-273.0)*1.1804 - 5.5092), 4)))
            elif cmd == '0x1c':
                # CLS temp
                self.clsTemp.setText(str(round(((1/((np.log(int(data)/26214.0) / 3950.0)+(1/298.0))-273.0)*1.1041 - 2.4323), 4)))
            elif cmd == '0x1d':
                # pump temp
                self.pumpTemp.setText(str(round(((1/((np.log(int(data)/26214.0) / 3950.0)+(1/298.0))-273.0)*1.1966 - 4.3200), 4)))

        self.recvmsg.addItem(QListWidgetItem(header))
        self.recvmsg.addItem(QListWidgetItem(cmd))
        self.recvmsg.addItem(QListWidgetItem(data))

    def updateDisconnect(self):
        self.btn.setText('접속')    

    def sendMsg(self, header, cmd, data):
        values = (header, cmd, data)
        fmt = '>B B H'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)

        self.c.send(sendData)

    def defaultMsg(self):
        header = int(self.headerMsg.toPlainText(), 16)
        cmd = int(self.cmdMsg.toPlainText(), 16)
        data = int(self.dataMsg.toPlainText(), 16)
        self.sendMsg(header, cmd, data)
    
    def mainToggle(self):
        if self.connect == True and self.mainStart == False:
            header = 0x41
            cmd = 0x01
            data = 0x0001
            self.sendMsg(header, cmd, data)
            self.mainBtn.setText('Stop')
            self.mainBtn.setStyleSheet("background-color: green")
            self.mainStart = True
        elif self.connect == True and self.mainStart == True:
            header = 0x41
            cmd = 0x01
            data = 0x0000
            self.sendMsg(header, cmd, data)
            if self.connect == True and self.ldStart == True:
                self.ldToggle()
            self.mainBtn.setText('Start')
            self.mainBtn.setStyleSheet("background-color: lightgray")
            self.mainStart = False

    def ldToggle(self):
        if self.connect == True and self.ldStart == False:
            header = 0x41
            cmd = 0x11
            data = 0x0001
            self.sendMsg(header, cmd, data)
            cmd = 0x01
            data = 0x0004
            self.sendMsg(header, cmd, data)
            self.ldBtn.setText('LD Stop')
            self.ldBtn.setStyleSheet("background-color: green")
            self.ldStart = True
        elif self.connect == True and self.ldStart == True:
            header = 0x41
            cmd = 0x11
            data = 0x0000
            self.sendMsg(header, cmd, data)
            self.ld1 = False
            self.ld2 = False
            self.ld3 = False
            self.ld4 = False
            self.ld5 = False
            self.ldBtn.setText('LD Strat')
            self.ldBtn.setStyleSheet("background-color: lightgray")
            self.ld1Btn.setStyleSheet("background-color: lightgray")    
            self.ld2Btn.setStyleSheet("background-color: lightgray")
            self.ld3Btn.setStyleSheet("background-color: lightgray")
            self.ld4Btn.setStyleSheet("background-color: lightgray")
            self.ld5Btn.setStyleSheet("background-color: lightgray")
            self.ldStart = False

    def ld1On(self):
        if self.ldStart == True:
            header = 0x41
            cmd = 0x11
            data = 0x0002
            self.sendMsg(header, cmd, data)
            self.ld1 = True
            self.ld1Btn.setStyleSheet("background-color: green")            

    def ld2On(self):
        if self.ldStart == True:
            header = 0x41
            cmd = 0x11
            data = 0x0004
            self.sendMsg(header, cmd, data)
            self.ld2 = True
            self.ld2Btn.setStyleSheet("background-color: green")

    def ld3On(self):
        if self.ldStart == True:
            header = 0x41
            cmd = 0x11
            data = 0x0008
            self.sendMsg(header, cmd, data)
            self.ld3 = True
            self.ld3Btn.setStyleSheet("background-color: green")

    def ld4On(self):
        if self.ldStart == True:
            header = 0x41
            cmd = 0x11
            data = 0x0010
            self.sendMsg(header, cmd, data)
            self.ld4 = True
            self.ld4Btn.setStyleSheet("background-color: green")

    def ld5On(self):
        if self.ldStart == True:
            header = 0x41
            cmd = 0x01
            data = 0x0010
            self.sendMsg(header, cmd, data)
            self.ld5 = True
            self.ld5Btn.setStyleSheet("background-color: green")

    def ld1AmpSet(self):
        if self.ld1 == True:
            header = 0x41
            cmd = 0x14
            data = float(self.ld1Amp.toPlainText())
            data = np.uint16(3822.0*data - 608)   
            self.sendMsg(header, cmd, data)

    def ld2AmpSet(self):
        if self.ld2 == True:
            header = 0x41
            cmd = 0x15
            data = float(self.ld2Amp.toPlainText())
            data = np.uint16(3817.5 * data - 132.5)   
            self.sendMsg(header, cmd, data)

    def ld3AmpSet(self):
        if self.ld3 == True:
            header = 0x41
            cmd = 0x16
            data = float(self.ld3Amp.toPlainText())
            data = np.uint16(3832.5 * data + 432.5)   
            self.sendMsg(header, cmd, data)

    def ld4AmpSet(self):
        if self.ld4 == True:
            header = 0x41
            cmd = 0x17
            data = float(self.ld4Amp.toPlainText())
            data = np.uint16(3807.5 * data - 207.5)   
            self.sendMsg(header, cmd, data)

    def ld5AmpSet(self):
        if self.ld5 == True:
            header = 0x41
            cmd = 0x03
            data = float(self.ld5Amp.toPlainText())
            data = np.uint16(3792.5 * data - 207.5)   
            self.sendMsg(header, cmd, data)

    def clearMsg(self):
        self.recvmsg.clear()

    def closeEvent(self, e):
        self.c.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())