from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import laser_client
import cooler_client
import ser
import struct
import numpy as np
import threading
from struct import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

port = 5000
ip = '127.0.1.1' #'192.168.0.99'
coolerPort = 502
coolerIp = '192.168.0.3'
coolerIp2 = '192.168.0.4'

class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.lc = laser_client.ClientSocket(self)
        self.cc = cooler_client.ClientSocket(self)
        self.ccc = cooler_client.ClientSocket(self)
        self.ser = ser.SerialSocket(self)
        self.lconnect = False
        self.cconnect = False
        self.ccconnect = False
        self.serConnect = False
        self.mainStart = False
        self.ldStart = False
        self.coolerStart = True
        self.ld1 = False
        self.ld2 = False
        self.ld3 = False
        self.ld4 = False
        self.ld5 = False

        self.coolerPower = 0
        self.coolerInTemp = 0
        self.coolerOutTemp = 0
        self.coolBit = 0

        self.initUI()

    def __del__(self):
        self.lc.stop()
        self.cc.stop()
        self.ccc.stop()
        # self.pc.stop()

    def initUI(self):
        self.setWindowTitle('휴대용 레이저 제어 프로그램')

        # 레이저 제어부
        laserBox = QHBoxLayout()

        gb = QGroupBox('레이저 제어부')
        laserBox.addWidget(gb)

        box = QVBoxLayout()

        laserIpBox = QHBoxLayout()
        box.addLayout(laserIpBox)

        label = QLabel('Server IP')
        self.ip = QLineEdit(str(ip))

        laserIpBox.addWidget(label)
        laserIpBox.addWidget(self.ip)

        label = QLabel('Server Port')
        self.port = QLineEdit(str(port))
        laserIpBox.addWidget(label)
        laserIpBox.addWidget(self.port)

        self.btn = QPushButton('접속')
        self.btn.clicked.connect(self.laserConnect)
        laserIpBox.addWidget(self.btn)

        # Enable 버튼 설정
        laserBtBox = QHBoxLayout()
        box.addLayout(laserBtBox)

        self.mainBtn = QPushButton('Start')
        self.mainBtn.clicked.connect(self.mainToggle)
        laserBtBox.addWidget(self.mainBtn)

        self.ldBtn = QPushButton('LD Start')
        self.ldBtn.clicked.connect(self.ldToggle)
        laserBtBox.addWidget(self.ldBtn)

        self.ld1Btn = QPushButton('LD No1')
        self.ld1Btn.clicked.connect(self.ld1On)
        laserBtBox.addWidget(self.ld1Btn)

        self.ld2Btn = QPushButton('LD No2')
        self.ld2Btn.clicked.connect(self.ld2On)
        laserBtBox.addWidget(self.ld2Btn)

        self.ld3Btn = QPushButton('LD No3')
        self.ld3Btn.clicked.connect(self.ld3On)
        laserBtBox.addWidget(self.ld3Btn)

        self.ld4Btn = QPushButton('LD No4')
        self.ld4Btn.clicked.connect(self.ld4On)
        laserBtBox.addWidget(self.ld4Btn)

        self.ld5Btn = QPushButton('LD No5')
        self.ld5Btn.clicked.connect(self.ld5On)
        laserBtBox.addWidget(self.ld5Btn)

        self.interBtn = QPushButton('Interlock')
        self.interBtn.setEnabled(False)
        laserBtBox.addWidget(self.interBtn)

        # 라벨
        laserLabelBox = QHBoxLayout()
        box.addLayout(laserLabelBox)

        label = QLabel('LD No.')
        laserLabelBox.addWidget(label)
        label = QLabel('Amp Set')
        laserLabelBox.addWidget(label)
        label = QLabel('Voltage')
        laserLabelBox.addWidget(label)
        label = QLabel('Amp')
        laserLabelBox.addWidget(label)

        # LD1 설정
        ld1Box = QHBoxLayout()
        box.addLayout(ld1Box)

        self.ld1SetBtn = QPushButton('LD 1')
        self.ld1SetBtn.setAutoDefault(True)
        self.ld1SetBtn.clicked.connect(self.ld1AmpSet)
        ld1Box.addWidget(self.ld1SetBtn)
        self.ld1Amp = QTextEdit()
        self.ld1Amp.setText('0.123')
        self.ld1Amp.setFixedHeight(27)
        ld1Box.addWidget(self.ld1Amp)
        # self.ld1VolRcv = QTextEdit()
        # self.ld1VolRcv.setFixedHeight(27)
        # ld1Box.addWidget(self.ld1VolRcv)
        self.ld1AmpRcv = QTextEdit()
        self.ld1AmpRcv.setFixedHeight(27)
        ld1Box.addWidget(self.ld1AmpRcv)

        # LD2 설정
        # ld2Box = QHBoxLayout()
        # box.addLayout(ld2Box)

        self.ld2SetBtn = QPushButton('LD 2')
        self.ld2SetBtn.setAutoDefault(True)
        self.ld2SetBtn.clicked.connect(self.ld2AmpSet)
        ld1Box.addWidget(self.ld2SetBtn)
        self.ld2Amp = QTextEdit()
        self.ld2Amp.setText('0.234')
        self.ld2Amp.setFixedHeight(27)
        ld1Box.addWidget(self.ld2Amp)
        # self.ld2VolRcv = QTextEdit()
        # self.ld2VolRcv.setFixedHeight(27)
        # ld2Box.addWidget(self.ld2VolRcv)
        self.ld2AmpRcv = QTextEdit()
        self.ld2AmpRcv.setFixedHeight(27)
        ld1Box.addWidget(self.ld2AmpRcv)

        # # LD3 설정
        # ld3Box = QHBoxLayout()
        # box.addLayout(ld3Box)

        self.ld3SetBtn = QPushButton('LD 3')
        self.ld3SetBtn.setAutoDefault(True)
        self.ld3SetBtn.clicked.connect(self.ld3AmpSet)
        ld1Box.addWidget(self.ld3SetBtn)
        self.ld3Amp = QTextEdit()
        self.ld3Amp.setText('0.345')
        self.ld3Amp.setFixedHeight(27)
        ld1Box.addWidget(self.ld3Amp)
        # self.ld3VolRcv = QTextEdit()
        # self.ld3VolRcv.setFixedHeight(27)
        # ld3Box.addWidget(self.ld3VolRcv)
        self.ld3AmpRcv = QTextEdit()
        self.ld3AmpRcv.setFixedHeight(27)
        ld1Box.addWidget(self.ld3AmpRcv)

        # LD4 설정
        # ld4Box = QHBoxLayout()
        # box.addLayout(ld4Box)

        self.ld4SetBtn = QPushButton('LD 4')
        self.ld4SetBtn.setAutoDefault(True)
        self.ld4SetBtn.clicked.connect(self.ld4AmpSet)
        ld1Box.addWidget(self.ld4SetBtn)
        self.ld4Amp = QTextEdit()
        self.ld4Amp.setText('0.456')
        self.ld4Amp.setFixedHeight(27)
        ld1Box.addWidget(self.ld4Amp)
        # self.ld4VolRcv = QTextEdit()
        # self.ld4VolRcv.setFixedHeight(27)
        # ld4Box.addWidget(self.ld4VolRcv)
        self.ld4AmpRcv = QTextEdit()
        self.ld4AmpRcv.setFixedHeight(27)
        ld1Box.addWidget(self.ld4AmpRcv)

        # LD5 설정
        # ld5Box = QHBoxLayout()
        # box.addLayout(ld5Box)

        self.ld5SetBtn = QPushButton('LD 5')
        self.ld5SetBtn.setAutoDefault(True)
        self.ld5SetBtn.clicked.connect(self.ld5AmpSet)
        ld1Box.addWidget(self.ld5SetBtn)
        self.ld5Amp = QTextEdit()
        self.ld5Amp.setText('0.564')
        self.ld5Amp.setFixedHeight(27)
        ld1Box.addWidget(self.ld5Amp)
        # self.ld5VolRcv = QTextEdit()
        # self.ld5VolRcv.setFixedHeight(27)
        # ld5Box.addWidget(self.ld5VolRcv)
        self.ld5AmpRcv = QTextEdit()
        self.ld5AmpRcv.setFixedHeight(27)
        ld1Box.addWidget(self.ld5AmpRcv)

        # 레이저 BIT 설정
        laserBitBox = QHBoxLayout()
        box.addLayout(laserBitBox)

        label = QLabel('1단 프론트')
        laserBitBox.addWidget(label)
        self.frontPower = QTextEdit()
        self.frontPower.setFixedHeight(27)
        laserBitBox.addWidget(self.frontPower)

        label = QLabel('1단 리어')
        laserBitBox.addWidget(label)
        self.rearPower = QTextEdit()
        self.rearPower.setFixedHeight(27)
        laserBitBox.addWidget(self.rearPower)

        label = QLabel('1단 온도')
        laserBitBox.addWidget(label)
        self.firstTemp = QTextEdit()
        self.firstTemp.setFixedHeight(27)
        laserBitBox.addWidget(self.firstTemp)

        label = QLabel('2단 온도')
        laserBitBox.addWidget(label)
        self.secondTemp = QTextEdit()
        self.secondTemp.setFixedHeight(27)
        laserBitBox.addWidget(self.secondTemp)

        label = QLabel('3단 온도')
        laserBitBox.addWidget(label)
        self.thirdTemp = QTextEdit()
        self.thirdTemp.setFixedHeight(27)
        laserBitBox.addWidget(self.thirdTemp)

        label = QLabel('3단 플레이트')
        laserBitBox.addWidget(label)
        self.thirdPlateTemp = QTextEdit()
        self.thirdPlateTemp.setFixedHeight(27)
        laserBitBox.addWidget(self.thirdPlateTemp)

        label = QLabel('CLS')
        laserBitBox.addWidget(label)
        self.clsTemp = QTextEdit()
        self.clsTemp.setFixedHeight(27)
        laserBitBox.addWidget(self.clsTemp)

        label = QLabel('펌프')
        laserBitBox.addWidget(label)
        self.pumpTemp = QTextEdit()
        self.pumpTemp.setFixedHeight(27)
        laserBitBox.addWidget(self.pumpTemp)

        gb.setLayout(box)

        # 냉각장치 제어부
        coolerBox = QVBoxLayout()

        gb = QGroupBox('냉각장치 제어부')
        coolerBox.addWidget(gb)

        box = QVBoxLayout()

        coolerIpBox = QHBoxLayout()
        box.addLayout(coolerIpBox)

        label = QLabel('냉각장치 모니터링 IP')
        self.c_ip1 = QLineEdit(str(coolerIp))      # coolerIp

        coolerIpBox.addWidget(label)
        coolerIpBox.addWidget(self.c_ip1)

        label = QLabel('냉각장치 제어 IP')
        self.c_ip2 = QLineEdit(str(coolerIp2))      # coolerIp

        coolerIpBox.addWidget(label)
        coolerIpBox.addWidget(self.c_ip2)

        label = QLabel('Port')
        self.c_port = QLineEdit(str(coolerPort))  # coolerPort
        coolerIpBox.addWidget(label)
        coolerIpBox.addWidget(self.c_port)

        self.c_btn = QPushButton('접속')
        self.c_btn.clicked.connect(self.coolerConnect)
        coolerIpBox.addWidget(self.c_btn)        
      
        # 냉각장치 BIT
        coolerBitBox = QHBoxLayout()
        box.addLayout(coolerBitBox)

        self.cPowerBtn = QPushButton('전원')
        self.cPowerBtn.clicked.connect(self.cPower)
        coolerBitBox.addWidget(self.cPowerBtn)

        self.tempMonitor = QPushButton('온도 모니터링')
        self.tempMonitor.setAutoDefault(True)
        self.tempMonitor.clicked.connect(self.coolerTemp)
        coolerBitBox.addWidget(self.tempMonitor)        

        label = QLabel('압축기 입구')
        coolerBitBox.addWidget(label)

        self.compIn = QTextEdit()
        self.compIn.setText('0.123')
        self.compIn.setFixedHeight(27)
        coolerBitBox.addWidget(self.compIn)

        label = QLabel('압축기 출구')
        coolerBitBox.addWidget(label)

        self.compOut = QTextEdit()
        self.compOut.setText('0.123')
        self.compOut.setFixedHeight(27)
        coolerBitBox.addWidget(self.compOut)

        self.ibitBtn = QPushButton('IBIT')
        self.ibitBtn.setAutoDefault(True)
        self.ibitBtn.clicked.connect(self.coolerBit)
        coolerBitBox.addWidget(self.ibitBtn)

        label = QLabel('압축기1 IBIT')
        coolerBitBox.addWidget(label)        
        
        self.ibit1 = QTextEdit()
        self.ibit1.setText('정상')
        self.ibit1.setFixedHeight(27)
        coolerBitBox.addWidget(self.ibit1)

        label = QLabel('압축기2 IBIT')
        coolerBitBox.addWidget(label) 

        self.ibit2 = QTextEdit()
        self.ibit2.setText('정상')
        self.ibit2.setFixedHeight(27)
        coolerBitBox.addWidget(self.ibit2)

        gb.setLayout(box)

        # 전원 제어부
        powerBox = QHBoxLayout()

        gb = QGroupBox('전원 제어부')
        powerBox.addWidget(gb)

        box = QVBoxLayout()

        # 전원 BIT 라벨
        powerBitLabelBox = QHBoxLayout()
        box.addLayout(powerBitLabelBox)

        label = QLabel('접속')
        powerBitLabelBox.addWidget(label)
        label = QLabel('최고 전압(mV)')
        powerBitLabelBox.addWidget(label)
        label = QLabel('최저 전압(mV)')
        powerBitLabelBox.addWidget(label)
        label = QLabel('최고 온도(℃)')
        powerBitLabelBox.addWidget(label)
        label = QLabel('최저 온도(℃)')
        powerBitLabelBox.addWidget(label)
        label = QLabel('충전 잔량(%)')
        powerBitLabelBox.addWidget(label)
        label = QLabel('잔류 전류(AH)')
        powerBitLabelBox.addWidget(label)
        label = QLabel('방전 시간(min)')
        powerBitLabelBox.addWidget(label)

        # 전원 BIT
        powerBitBox = QHBoxLayout()
        box.addLayout(powerBitBox)

        self.p_Btn = QPushButton('접속')
        self.p_Btn.setAutoDefault(True)
        self.p_Btn.clicked.connect(self.powerConnect)
        powerBitBox.addWidget(self.p_Btn)

        self.max_volt = QTextEdit()
        self.max_volt.setText('3.999')
        self.max_volt.setFixedHeight(27)
        powerBitBox.addWidget(self.max_volt)

        self.min_volt = QTextEdit()
        self.min_volt.setText('3.799')
        self.min_volt.setFixedHeight(27)
        powerBitBox.addWidget(self.min_volt)

        self.max_temp = QTextEdit()
        self.max_temp.setText('21.0')
        self.max_temp.setFixedHeight(27)
        powerBitBox.addWidget(self.max_temp)

        self.min_temp = QTextEdit()
        self.min_temp.setText('20.5')
        self.min_temp.setFixedHeight(27)
        powerBitBox.addWidget(self.min_temp)

        self.s_o_charge = QTextEdit()
        self.s_o_charge.setText('99.99')
        self.s_o_charge.setFixedHeight(27)
        powerBitBox.addWidget(self.s_o_charge)

        self.a_capacity = QTextEdit()
        self.a_capacity.setText('5.0')
        self.a_capacity.setFixedHeight(27)
        powerBitBox.addWidget(self.a_capacity)

        self.t_t_discharge = QTextEdit()
        self.t_t_discharge.setText('99')
        self.t_t_discharge.setFixedHeight(27)
        powerBitBox.addWidget(self.t_t_discharge)

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
        self.dataMsg.setText('1234')
        messageBox.addWidget(self.dataMsg)
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
        vbox.addLayout(laserBox)
        vbox.addLayout(coolerBox)
        vbox.addLayout(powerBox)
        vbox.addLayout(infobox)
        self.setLayout(vbox)

        self.show()

    def laserConnect(self):
        if self.lc.bConnect == False:
            ip = self.ip.text()
            port = self.port.text()
            if self.lc.connectServer(ip, int(port)):
                self.btn.setStyleSheet("background-color: green")
                self.btn.setText('접속 종료')
                self.lconnect = True
            else:
                self.lc.stop()
                self.recvmsg.clear()
                self.btn.setText('접속')
                self.btn.setStyleSheet("background-color: lightgray")
                self.lconnect = False
        else:
            self.lc.stop()
            self.recvmsg.clear()
            self.btn.setText('접속')
            self.btn.setStyleSheet("background-color: lightgray")
            self.lconnect = False

    def coolerConnect(self):
        if self.cc.bConnect == False:
            ip = self.c_ip.text()
            port = self.c_port.text()
            if self.cc.connectServer(ip, int(port)):                
                self.cconnect = True
            else:
                self.cc.stop()
                self.recvmsg.clear()                
                self.cconnect = False
        else:
            self.cc.stop()
            self.recvmsg.clear()
            self.cconnect = False

        if self.ccc.bConnect == False:
            ip = '192.168.0.4'
            port = self.c_port.text()
            if self.ccc.connectServer(ip, int(port)):
                self.ccconnect = True
            else:
                self.ccc.stop()
                self.ccconnect = False
        else:
            self.ccc.stop()
            self.ccconnect = False

        if self.cc.bConnect == True and self.ccc.bConnect == True:
            self.c_btn.setStyleSheet("background-color: green")
            self.c_btn.setText('접속 종료')
        else:
            self.c_btn.setText('접속')
            self.c_btn.setStyleSheet("background-color: lightgray")

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

    def updateLaser(self, ld1amp, ld2amp, ld3amp, ld4amp, ld5amp, temp1, temp2, temp3, temp3plate, tempcls, temppump, frontpower, rearpower, mdstatus):
        self.ld1AmpRcv.setText(str(round((ld1amp+608.0) / 3822.0, 4)))
        self.ld2AmpRcv.setText(str(round((ld2amp+132.5) / 3817.5, 4)))
        self.ld3AmpRcv.setText(str(round((ld3amp-432.5) / 3832.5, 4)))
        self.ld4AmpRcv.setText(str(round((ld4amp+542.5) / 3807.5, 4)))
        self.ld5AmpRcv.setText(str(round((ld5amp+207.5) / 3792.5, 4)))
        if temp1 != 0:
            self.firstTemp.setText(str(round(((1/((np.log(temp1/26214.0) / 3950.0)+(1/298.0))-273.0)*1.1189 - 2.8153),4)))
        if temp2 != 0:
            self.secondTemp.setText(str(round(((1/((np.log(temp2/26214.0) / 3950.0)+(1/298.0))-273.0)*1.2161 - 4.8080), 4)))
        if temp3 != 0:
            self.thirdTemp.setText(str(round(((1/((np.log(temp3/26214.0) / 3950.0)+(1/298.0))-273.0)*1.4021 - 8.7607), 4)))
        if temp3plate != 0:
            self.thirdPlateTemp.setText(str(round(((1/((np.log(temp3plate/26214.0) / 3950.0)+(1/298.0))-273.0)*1.1804 - 5.5092), 4)))
        if tempcls != 0:
            self.clsTemp.setText(str(round(((1/((np.log(tempcls/26214.0) / 3950.0)+(1/298.0))-273.0)*1.1041 - 2.4323), 4)))
        if temppump != 0:
            self.pumpTemp.setText(str(round(((1/((np.log(temppump/26214.0) / 3950.0)+(1/298.0))-273.0)*1.1966 - 4.3200), 4)))
        self.frontPower.setText(str(round(((frontpower+207.5) / 3792.5), 4)))
        self.rearPower.setText(str(round(((rearpower+207.5) / 3792.5), 4)))
        # Interlock
        if mdstatus & 0b0001 == True:
            self.interBtn.setStyleSheet("background-color: red")
        else:
            self.interBtn.setStyleSheet("background-color: lightgray")

        self.recvmsg.addItem("[Laser]: " + str(hex(ld1amp)) + " /" + str(hex(ld2amp)) + " /" + str(hex(ld3amp)) + " /" + str(hex(ld4amp)) + " /" + str(hex(ld5amp))\
             + " /" + str(hex(temp1)) + " /" + str(hex(temp2)) + " /" + str(hex(temp3)) + " /" + str(hex(temp3plate)) + " /" + str(hex(tempcls)) + " /" + str(hex(temppump))\
                  + " /" + str(hex(frontpower)) + " /" + str(hex(rearpower)) + " /" + str(hex(mdstatus)))

        # self.ld1VolRcv.setText(str(round(ld1volt*0.0012 -0.0540, 4)))
        # self.ld2VolRcv.setText(str(round(ld2volt*0.0012 -0.0332, 4)))
        # self.ld3VolRcv.setText(str(round(ld3volt*0.0012 -0.0615, 4)))
        # self.ld4VolRcv.setText(str(round(ld4volt*0.0012 -0.0136, 4)))
        # self.ld5VolRcv.setText(str(round((ld5volt+207.5) / 3792.5, 4)))

        
    def updateCooler(self, func, val1, val2):
        if func == 5:
            if val1 == 65280:
                self.cPowerBtn.setStyleSheet("background-color: green")
            elif val1 == 0:
                self.cPowerBtn.setStyleSheet("background-color: lightgray")
            else:
                self.cPowerBtn.setStyleSheet("background-color: red")
                
        elif func == 4:
            coolerInTemp = (val1/65535)*500 - 100
            coolerOutTemp = (val2/65535)*500 - 100
            self.compIn.setText(str(round(coolerInTemp, 4)))
            self.compOut.setText(str(round(coolerOutTemp, 4)))

        elif func == 1:
            if val1 == 0:
                self.ibit.setText('정상')
            elif val1 == 0:
                self.ibit.setText('고장')     
            else:
                self.ibit.setText('Unknown')

    def updatePower(self, max_v, min_v, max_t, min_t, charge, capacity, discharge):
        print(max_v, min_v, max_t, min_t, charge, capacity, discharge)
        self.max_volt.setText(str(max_v/1000))
        self.min_volt.setText(str(min_v/1000))
        self.max_temp.setText(str(max_t/10))
        self.min_temp.setText(str(min_t/10))
        self.s_o_charge.setText(str(charge/10))
        self.a_capacity.setText(str(capacity/10))
        self.t_t_discharge.setText(str(discharge))

    def laserDisconnect(self):
        self.btn.setText('접속')    

    def coolerDisconnect(self):
        self.c_btn.setText('접속')  

    def powerDisconnect(self):
        self.p_btn.setText('접속')  

    def sendLaser(self, header, cmd, data):
        values = (header, cmd, data)
        fmt = '>B B H'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)

        self.lc.send(sendData)

    def sendLaser2(self, header, cmd):
        values = (header, cmd)
        fmt = '>B B'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)

        self.lc.send(sendData)
    
    def sendCooler(self, header, cmd, addr, data):
        trans = 0
        proto = 0
        length = 6
        values = (trans, proto, length, header, cmd, addr, data)
        fmt = '>H H H B B H H'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)

        self.cc.send(sendData)

    def sendcCooler(self, header, cmd, addr, data):
        trans = 0
        proto = 0
        length = 6
        values = (trans, proto, length, header, cmd, addr, data)
        fmt = '>H H H B B H H'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)

        self.ccc.send(sendData)

    def defaultMsg(self):
        header = int(self.headerMsg.toPlainText(), 16)
        cmd = int(self.cmdMsg.toPlainText(), 16)
        data = int(self.dataMsg.toPlainText(), 16)
        self.sendLaser(header, cmd, data)
    
    def mainToggle(self):
        if self.lconnect == True and self.mainStart == False:
            header = 0x29
            cmd = 0x12
            data = 0x0100
            self.sendLaser(header, cmd, data)
            self.mainBtn.setText('Stop')
            self.mainBtn.setStyleSheet("background-color: green")
            self.mainStart = True
        elif self.lconnect == True and self.mainStart == True:
            header = 0x29
            cmd = 0x01
            data = 0x0000
            self.sendLaser(header, cmd, data)
            if self.lconnect == True and self.ldStart == True:
                self.ldToggle()
            self.mainBtn.setText('Start')
            self.mainBtn.setStyleSheet("background-color: lightgray")
            self.mainStart = False

    def ldToggle(self):
        if self.lconnect == True and self.ldStart == False:
            header = 0x29
            cmd = 0x01
            data = 0x0500
            self.sendLaser(header, cmd, data)
            # sleep(0.1)
            # cmd = 0x11
            # data = 0x0100
            # self.sendLaser(header, cmd, data)
            self.ldBtn.setText('LD Stop')
            self.ldBtn.setStyleSheet("background-color: green")
            self.ldStart = True
        elif self.lconnect == True and self.ldStart == True:
            header = 0x29
            cmd = 0x11
            data = 0x0100
            self.sendLaser(header, cmd, data)
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
            # self.ldStart = False

    def ld1On(self):
        if self.ldStart == True:
            header = 0x41
            cmd = 0x11
            data = 0x0002
            self.sendLaser(header, cmd, data)
            self.ld1 = True
            self.ld1Btn.setStyleSheet("background-color: green")            

    def ld2On(self):
        # if self.ldStart == True:
        header = 0x28
        cmd = 0x21
        # data = 0x0004
        self.sendLaser2(header, cmd)
        self.ld2 = True
        self.ld2Btn.setStyleSheet("background-color: green")

    def ld3On(self):
        if self.ldStart == True:
            header = 0x41
            cmd = 0x11
            data = 0x0008
            self.sendLaser(header, cmd, data)
            self.ld3 = True
            self.ld3Btn.setStyleSheet("background-color: green")

    def ld4On(self):
        if self.ldStart == True:
            header = 0x41
            cmd = 0x11
            data = 0x0010
            self.sendLaser(header, cmd, data)
            self.ld4 = True
            self.ld4Btn.setStyleSheet("background-color: green")

    def ld5On(self):
        if self.ldStart == True:
            header = 0x41
            cmd = 0x01
            data = 0x0010
            self.sendLaser(header, cmd, data)
            self.ld5 = True
            self.ld5Btn.setStyleSheet("background-color: green")

    def ld1AmpSet(self):
        # if self.ld1 == True:
        header = 0x29
        cmd = 0x14
        # data = float(self.ld1Amp.toPlainText())
        # data = np.uint16(3822.0*data - 608)  
        data = 0x0000 
        self.sendLaser(header, cmd, data)

    def ld2AmpSet(self):
        # if self.ld2 == True:
        header = 0x29
        cmd = 0x15
        # data = float(self.ld2Amp.toPlainText())
        # data = np.uint16(3817.5 * data - 132.5)   
        data = 0x0000
        self.sendLaser(header, cmd, data)

    def ld3AmpSet(self):
        # if self.ld3 == True:
        header = 0x29
        cmd = 0x16
        # data = float(self.ld3Amp.toPlainText())
        # data = np.uint16(3832.5 * data + 432.5)
        data = 0x0000   
        self.sendLaser(header, cmd, data)

    def ld4AmpSet(self):
        # if self.ld4 == True:
        header = 0x29
        cmd = 0x17
        # data = float(self.ld4Amp.toPlainText())
        # data = np.uint16(3807.5 * data - 207.5)   
        data = 0x0000
        self.sendLaser(header, cmd, data)

    def ld5AmpSet(self):
        # if self.ld5 == True:
        header = 0x29
        cmd = 0x03
        # data = float(self.ld5Amp.toPlainText())
        # data = np.uint16(3792.5 * data - 207.5)   
        data = 0x0000
        self.sendLaser(header, cmd, data)
    
    def cPower(self):
        header = 1
        cmd = 5

        addr = 0x0017
        if self.coolerStart == False:
            data = 0xFF00
            self.coolerStart = True
            # self.coolerBit()       
            # self.coolerTemp()     
        else:
            data = 0
            self.coolerStart = False
            # self.t1.cancel()
            # self.t2.cancel()
        self.sendcCooler(header, cmd, addr, data)        

    def coolerTemp(self):
        header = 1
        cmd = 4
        addr = 1
        data = 3
        self.sendCooler(header, cmd, addr, data)    
        # self.t1 = threading.Timer(1, self.coolerTemp)
        # self.t1.deamon = True
        # self.t1.start()

    def coolerBit(self):
        header = 1
        cmd = 1
        addr = 0x0001
        data = 0x0008
        self.sendcCooler(header, cmd, addr, data)   
        # self.t2 = threading.Timer(1, self.coolerBit)
        # self.t2.deamon = True
        # self.t2.start()

    def clearMsg(self):
        self.recvmsg.clear()

    def closeEvent(self, e):
        self.lc.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())