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
        self.power = False
        self.mainStart = False
        self.ldOnOff = False
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
        # self.ip.setInputMask('127.0.1.1;_')
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

        self.mainbtn = QPushButton('Start')
        self.mainbtn.clicked.connect(self.mainToggle)
        box.addWidget(self.mainbtn)

        self.ldallbtn = QPushButton('LD all On')
        self.ldallbtn.clicked.connect(self.ldToggle)
        box.addWidget(self.ldallbtn)

        self.ldno1btn = QPushButton('LD No1')
        self.ldno1btn.clicked.connect(self.ld1On)
        box.addWidget(self.ldno1btn)

        self.ldno2btn = QPushButton('LD No2')
        self.ldno2btn.clicked.connect(self.ld2On)
        box.addWidget(self.ldno2btn)

        self.ldno3btn = QPushButton('LD No3')
        self.ldno3btn.clicked.connect(self.ld3On)
        box.addWidget(self.ldno3btn)

        self.ldno4btn = QPushButton('LD No4')
        self.ldno4btn.clicked.connect(self.ld4On)
        box.addWidget(self.ldno4btn)

        self.ldno5btn = QPushButton('LD No5')
        self.ldno5btn.clicked.connect(self.ld5On)
        box.addWidget(self.ldno5btn)

        self.interbtn = QPushButton('Interlock')
        box.addWidget(self.interbtn)

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

        self.ld1btn = QPushButton('LD 1')
        self.ld1btn.setAutoDefault(True)
        self.ld1btn.clicked.connect(self.ld1AmpSet)
        ld1box.addWidget(self.ld1btn)
        self.ld1amp = QTextEdit()
        self.ld1amp.setText('0.123')
        self.ld1amp.setFixedHeight(27)
        ld1box.addWidget(self.ld1amp)
        self.ld1volrcv = QTextEdit()
        self.ld1volrcv.setFixedHeight(27)
        ld1box.addWidget(self.ld1volrcv)
        self.ld1amprcv = QTextEdit()
        self.ld1amprcv.setFixedHeight(27)
        ld1box.addWidget(self.ld1amprcv)

        # gb.setLayout(box)

        # LD2 설정
        ld2box = QHBoxLayout()
        box.addLayout(ld2box)

        self.ld2btn = QPushButton('LD 2')
        self.ld2btn.setAutoDefault(True)
        self.ld2btn.clicked.connect(self.ld2AmpSet)
        ld2box.addWidget(self.ld2btn)
        self.ld2amp = QTextEdit()
        self.ld2amp.setText('0.234')
        self.ld2amp.setFixedHeight(27)
        ld2box.addWidget(self.ld2amp)
        self.ld2volrcv = QTextEdit()
        self.ld2volrcv.setFixedHeight(27)
        ld2box.addWidget(self.ld2volrcv)
        self.ld2amprcv = QTextEdit()
        self.ld2amprcv.setFixedHeight(27)
        ld2box.addWidget(self.ld2amprcv)

        # gb.setLayout(box)

        # LD3 설정
        ld3box = QHBoxLayout()
        box.addLayout(ld3box)

        self.ld3btn = QPushButton('LD 3')
        self.ld3btn.setAutoDefault(True)
        self.ld3btn.clicked.connect(self.ld3AmpSet)
        ld3box.addWidget(self.ld3btn)
        self.ld3amp = QTextEdit()
        self.ld3amp.setText('0.345')
        self.ld3amp.setFixedHeight(27)
        ld3box.addWidget(self.ld3amp)
        self.ld3volrcv = QTextEdit()
        self.ld3volrcv.setFixedHeight(27)
        ld3box.addWidget(self.ld3volrcv)
        self.ld3amprcv = QTextEdit()
        self.ld3amprcv.setFixedHeight(27)
        ld3box.addWidget(self.ld3amprcv)

        # gb.setLayout(box)

        # LD4 설정
        ld4box = QHBoxLayout()
        box.addLayout(ld4box)

        self.ld4btn = QPushButton('LD 4')
        self.ld4btn.setAutoDefault(True)
        self.ld4btn.clicked.connect(self.ld4AmpSet)
        ld4box.addWidget(self.ld4btn)
        self.ld4amp = QTextEdit()
        self.ld4amp.setText('0.456')
        self.ld4amp.setFixedHeight(27)
        ld4box.addWidget(self.ld4amp)
        self.ld4volrcv = QTextEdit()
        self.ld4volrcv.setFixedHeight(27)
        ld4box.addWidget(self.ld4volrcv)
        self.ld4amprcv = QTextEdit()
        self.ld4amprcv.setFixedHeight(27)
        ld4box.addWidget(self.ld4amprcv)

        # gb.setLayout(box)

        # LD5 설정
        ld5box = QHBoxLayout()
        box.addLayout(ld5box)

        self.ld5btn = QPushButton('LD 5')
        self.ld5btn.setAutoDefault(True)
        self.ld5btn.clicked.connect(self.ld5AmpSet)
        ld5box.addWidget(self.ld5btn)
        self.ld5amp = QTextEdit()
        self.ld5amp.setText('0.564')
        self.ld5amp.setFixedHeight(27)
        ld5box.addWidget(self.ld5amp)
        self.ld5volrcv = QTextEdit()
        self.ld5volrcv.setFixedHeight(27)
        ld5box.addWidget(self.ld5volrcv)
        self.ld5amprcv = QTextEdit()
        self.ld5amprcv.setFixedHeight(27)
        ld5box.addWidget(self.ld5amprcv)

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
        self.firsttemp = QTextEdit()
        self.firsttemp.setFixedHeight(27)
        tempbox1.addWidget(self.firsttemp)

        label = QLabel('2nd temp')
        tempbox1.addWidget(label)
        self.secondtemp = QTextEdit()
        self.secondtemp.setFixedHeight(27)
        tempbox1.addWidget(self.secondtemp)

        label = QLabel('3rd temp')
        tempbox1.addWidget(label)
        self.thirdtemp = QTextEdit()
        self.thirdtemp.setFixedHeight(27)
        tempbox1.addWidget(self.thirdtemp)

        tempbox2 = QHBoxLayout()
        box.addLayout(tempbox2)

        label = QLabel('3rd Plate temp')
        tempbox2.addWidget(label)
        self.thirdplatetemp = QTextEdit()
        self.thirdplatetemp.setFixedHeight(27)
        tempbox2.addWidget(self.thirdplatetemp)

        label = QLabel('CLS')
        tempbox2.addWidget(label)
        self.clstemp = QTextEdit()
        self.clstemp.setFixedHeight(27)
        tempbox2.addWidget(self.clstemp)

        label = QLabel('PUMP')
        tempbox2.addWidget(label)
        self.pumptemp = QTextEdit()
        self.pumptemp.setFixedHeight(27)
        tempbox2.addWidget(self.pumptemp)

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
        self.sendbtn = QPushButton('보내기')
        self.sendbtn.setAutoDefault(True)
        self.sendbtn.clicked.connect(self.defaultMsg)

        self.clearbtn = QPushButton('채팅창 지움')
        self.clearbtn.clicked.connect(self.clearMsg)

        hbox.addWidget(self.sendbtn)
        hbox.addWidget(self.clearbtn)
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
                self.power = True
            else:
                self.c.stop()
                self.recvmsg.clear()
                self.btn.setText('접속')
                self.btn.setStyleSheet("background-color: lightgray")
                self.power = False
        else:
            self.c.stop()
            self.recvmsg.clear()
            self.btn.setText('접속')
            self.btn.setStyleSheet("background-color: lightgray")
            self.power = False

    def updateMsg(self, header, cmd, data):
        if header == '0x41':
            if cmd == '0x7':
                # LD5 amp
                self.ld5amprcv.setText(str(round(((int(data)+207.5) / 3792.5), 4)))
            elif cmd == '0x8':
                # 1st Front Optical Power
                self.frontPower.setText(str(round(((int(data)+207.5) / 3792.5), 4)))
            elif cmd == '0x9':
                # 1st Rear Optical Power
                self.rearPower.setText(str(round(((int(data)+207.5) / 3792.5), 4)))
            elif cmd == '0xd':
                # Interlock
                if int(data) & 0b0001 == True:
                    self.interbtn.setStyleSheet("background-color: red")
                else:
                    self.interbtn.setStyleSheet("background-color: lightgray")
            elif cmd == '0xf':
                # LD5 vol
                self.ld5volrcv.setText(str(round(((int(data)+207.5) / 3792.5), 4)))
            elif cmd == '0x10':
                # LD1 vol
                self.ld1volrcv.setText(str(round((int(data)*0.0012 -0.0540), 4)))
            elif cmd == '0x11':
                # LD2 vol
                self.ld2volrcv.setText(str(round((int(data)*0.0012 -0.0332), 4)))
            elif cmd == '0x12':
                # LD3 vol
                self.ld3volrcv.setText(str(round((int(data)*0.0012 -0.0615), 4)))
            elif cmd == '0x13':
                # LD4 vol
                self.ld4volrcv.setText(str(round((int(data)*0.0012 -0.0136), 4)))
            elif cmd == '0x14':
                # LD1 amp
                self.ld1amprcv.setText(str(round(((int(data)+608.0) / 3822.0), 4)))
            elif cmd == '0x15':
                # LD2 amp
                self.ld2amprcv.setText(str(round(((int(data)+132.5) / 3817.5), 4)))
            elif cmd == '0x16':
                # LD3 amp
                self.ld3amprcv.setText(str(round(((int(data)-432.5) / 3832.5), 4)))
            elif cmd == '0x17':
                # LD4 amp
                self.ld4amprcv.setText(str(round(((int(data)+542.5) / 3807.5), 4)))
            elif cmd == '0x18':
                # 1st temp
                self.firsttemp.setText(str(round(((1/((np.log(int(data)/26214.0) / 3950.0)+(1/298.0))-273.0)*1.1189 - 2.8153),4)))
            elif cmd == '0x19':
                # 2nd temp
                self.secondtemp.setText(str(round(((1/((np.log(int(data)/26214.0) / 3950.0)+(1/298.0))-273.0)*1.2161 - 4.8080), 4)))
            elif cmd == '0x1a':
                # 3rd temp
                self.thirdtemp.setText(str(round(((1/((np.log(int(data)/26214.0) / 3950.0)+(1/298.0))-273.0)*1.4021 - 8.7607), 4)))
            elif cmd == '0x1b':
                # 3rd plate temp
                self.thirdplatetemp.setText(str(round(((1/((np.log(int(data)/26214.0) / 3950.0)+(1/298.0))-273.0)*1.1804 - 5.5092), 4)))
            elif cmd == '0x1c':
                # CLS temp
                self.clstemp.setText(str(round(((1/((np.log(int(data)/26214.0) / 3950.0)+(1/298.0))-273.0)*1.1041 - 2.4323), 4)))
            elif cmd == '0x1d':
                # pump temp
                self.pumptemp.setText(str(round(((1/((np.log(int(data)/26214.0) / 3950.0)+(1/298.0))-273.0)*1.1966 - 4.3200), 4)))

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
        print(sendData)

        self.c.send(sendData)

    def defaultMsg(self):
        header = int(self.headerMsg.toPlainText(), 16)
        cmd = int(self.cmdMsg.toPlainText(), 16)
        data = int(self.dataMsg.toPlainText(), 16)
        self.sendMsg(header, cmd, data)
    
    def mainToggle(self):
        if self.power == True and self.mainStart == False:
            header = 0x41
            cmd = 0x01
            data = 0x0001
            self.sendMsg(header, cmd, data)
            self.mainbtn.setStyleSheet("background-color: green")
            self.mainStart = True
        elif self.power == True and self.mainStart == True:
            header = 0x41
            cmd = 0x01
            data = 0x0000
            self.sendMsg(header, cmd, data)
            if self.power == True and self.ldOnOff == True:
                self.ldToggle()
            self.mainbtn.setStyleSheet("background-color: lightgray")
            self.mainStart = False

    def ldToggle(self):
        if self.power == True and self.ldOnOff == False:
            header = 0x41
            cmd = 0x11
            data = 0x0001
            self.sendMsg(header, cmd, data)
            cmd = 0x01
            data = 0x0004
            self.sendMsg(header, cmd, data)
            self.ldallbtn.setStyleSheet("background-color: green")
            self.ldOnOff = True
        elif self.power == True and self.ldOnOff == True:
            header = 0x41
            cmd = 0x11
            data = 0x0000
            self.sendMsg(header, cmd, data)
            self.ld1 = False
            self.ld2 = False
            self.ld3 = False
            self.ld4 = False
            self.ld5 = False
            self.ldallbtn.setStyleSheet("background-color: lightgray")
            self.ldno1btn.setStyleSheet("background-color: lightgray")    
            self.ldno2btn.setStyleSheet("background-color: lightgray")
            self.ldno3btn.setStyleSheet("background-color: lightgray")
            self.ldno4btn.setStyleSheet("background-color: lightgray")
            self.ldno5btn.setStyleSheet("background-color: lightgray")
            self.ldOnOff = False

    def ld1On(self):
        if self.ldOnOff == True:
            header = 0x41
            cmd = 0x11
            data = 0x0002
            self.sendMsg(header, cmd, data)
            self.ld1 = True
            self.ldno1btn.setStyleSheet("background-color: green")            

    def ld2On(self):
        if self.ldOnOff == True:
            header = 0x41
            cmd = 0x11
            data = 0x0004
            self.sendMsg(header, cmd, data)
            self.ld2 = True
            self.ldno2btn.setStyleSheet("background-color: green")

    def ld3On(self):
        if self.ldOnOff == True:
            header = 0x41
            cmd = 0x11
            data = 0x0008
            self.sendMsg(header, cmd, data)
            self.ld3 = True
            self.ldno3btn.setStyleSheet("background-color: green")

    def ld4On(self):
        if self.ldOnOff == True:
            header = 0x41
            cmd = 0x11
            data = 0x0010
            self.sendMsg(header, cmd, data)
            self.ld4 = True
            self.ldno4btn.setStyleSheet("background-color: green")

    def ld5On(self):
        if self.ldOnOff == True:
            header = 0x41
            cmd = 0x01
            data = 0x0010
            self.sendMsg(header, cmd, data)
            self.ld5 = True
            self.ldno5btn.setStyleSheet("background-color: green")

    def ld1AmpSet(self):
        if self.ld1 == True:
            header = 0x41
            cmd = 0x14
            data = float(self.ld1amp.toPlainText())
            data = np.uint16(3822.0*data - 608)   
            self.sendMsg(header, cmd, data)

    def ld2AmpSet(self):
        if self.ld2 == True:
            header = 0x41
            cmd = 0x15
            data = float(self.ld2amp.toPlainText())
            data = np.uint16(3817.5 * data - 132.5)   
            self.sendMsg(header, cmd, data)

    def ld3AmpSet(self):
        if self.ld3 == True:
            header = 0x41
            cmd = 0x16
            data = float(self.ld3amp.toPlainText())
            data = np.uint16(3832.5 * data + 432.5)   
            self.sendMsg(header, cmd, data)

    def ld4AmpSet(self):
        if self.ld4 == True:
            header = 0x41
            cmd = 0x17
            data = float(self.ld4amp.toPlainText())
            data = np.uint16(3807.5 * data - 207.5)   
            self.sendMsg(header, cmd, data)

    def ld5AmpSet(self):
        if self.ld5 == True:
            header = 0x41
            cmd = 0x03
            data = float(self.ld5amp.toPlainText())
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