from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import ser
import chiller
import struct
import numpy as np
import threading
from time import sleep
from struct import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.ser = ser.SerialSocket(self)
        self.pilotFlag=False
        self.chiller = chiller.SerialSocket(self)

        self.initUI()

    # def __del__(self):
        # self.ser.stop()

    def initUI(self):
        self.setWindowTitle('FeiboLaser')

        # 레이저 제어부
        laserBox = QHBoxLayout()

        gb = QGroupBox('Laser Control')
        laserBox.addWidget(gb)

        box = QVBoxLayout()

        laserbtnBox = QHBoxLayout()
        box.addLayout(laserbtnBox)

        self.laserCntBtn = QPushButton('Connect')
        self.laserCntBtn.setFixedWidth(148)
        self.laserCntBtn.clicked.connect(self.laserConnect)
        laserbtnBox.addWidget(self.laserCntBtn)

        self.statusReqBtn = QPushButton('Status')
        self.statusReqBtn.setFixedWidth(148)
        self.statusReqBtn.clicked.connect(self.status)
        laserbtnBox.addWidget(self.statusReqBtn)

        self.dsnReqBtn = QPushButton('DSN')
        self.dsnReqBtn.setFixedWidth(148)
        self.dsnReqBtn.clicked.connect(self.dsn)
        laserbtnBox.addWidget(self.dsnReqBtn)

        self.opmdReqBtn = QPushButton('OPMD')
        self.opmdReqBtn.setFixedWidth(148)
        self.opmdReqBtn.clicked.connect(self.opmdReq)
        laserbtnBox.addWidget(self.opmdReqBtn)

        self.limitReqBtn = QPushButton('Limit')
        self.limitReqBtn.setFixedWidth(148)
        self.limitReqBtn.clicked.connect(self.limit)
        laserbtnBox.addWidget(self.limitReqBtn)

        self.tempReqBtn = QPushButton('Temp')
        self.tempReqBtn.setFixedWidth(148)
        self.tempReqBtn.clicked.connect(self.temp)
        laserbtnBox.addWidget(self.tempReqBtn)

        self.pdReqBtn = QPushButton('PD')
        self.pdReqBtn.setFixedWidth(148)
        self.pdReqBtn.clicked.connect(self.pd)
        laserbtnBox.addWidget(self.pdReqBtn)     

        label = QLabel(' ')
        laserbtnBox.addWidget(label)

        # 라벨
        labelBox = QHBoxLayout()
        box.addLayout(labelBox)

        label = QLabel('Set Value')
        labelBox.addWidget(label)

        # 
        controlBox = QHBoxLayout()
        box.addLayout(controlBox)
        
        self.enableEdit = QTextEdit()
        self.enableEdit.setText('100')
        self.enableEdit.setFixedHeight(27)
        self.enableEdit.setFixedWidth(148)
        controlBox.addWidget(self.enableEdit)
        self.enableBtn = QPushButton('ENABLE')
        self.enableBtn.setAutoDefault(True)
        self.enableBtn.setFixedWidth(148)
        self.enableBtn.clicked.connect(self.enable)
        controlBox.addWidget(self.enableBtn)

        self.pilotBtn = QPushButton('Pilot On')
        self.pilotBtn.setAutoDefault(True)
        self.pilotBtn.setFixedWidth(148)
        self.pilotBtn.clicked.connect(self.pilot)
        controlBox.addWidget(self.pilotBtn)

        self.opmdBtn = QPushButton('OPMD')
        self.opmdBtn.setAutoDefault(True)
        self.opmdBtn.setFixedWidth(148)
        self.opmdBtn.clicked.connect(self.opmd)
        controlBox.addWidget(self.opmdBtn)

        self.setModeBtn = QPushButton('Set Mode')
        self.setModeBtn.setAutoDefault(True)
        self.setModeBtn.setFixedWidth(148)
        self.setModeBtn.clicked.connect(self.setMode)
        controlBox.addWidget(self.setModeBtn)

        self.outputEdit = QTextEdit()
        self.outputEdit.setText('100')
        self.outputEdit.setFixedHeight(27)
        self.outputEdit.setFixedWidth(148)
        controlBox.addWidget(self.outputEdit)
        self.outputBtn = QPushButton('Output')
        self.outputBtn.setAutoDefault(True)
        self.outputBtn.setFixedWidth(148)
        self.outputBtn.clicked.connect(self.output)
        controlBox.addWidget(self.outputBtn)
        label = QLabel(' ')
        controlBox.addWidget(label)
        
        # 라벨
        bitLabelBox = QHBoxLayout()
        box.addLayout(bitLabelBox)

        label = QLabel('BIT')
        bitLabelBox.addWidget(label)

        # 레이저 BIT 설정
        laserBit1Box = QHBoxLayout()
        box.addLayout(laserBit1Box)

        self.t1LowBtn = QPushButton('T1 low')
        laserBit1Box.addWidget(self.t1LowBtn)
        self.t2LowBtn = QPushButton('T2 low')
        laserBit1Box.addWidget(self.t2LowBtn)
        self.t3LowBtn = QPushButton('T3 low')
        laserBit1Box.addWidget(self.t3LowBtn)
        self.t4LowBtn = QPushButton('T4 low')
        laserBit1Box.addWidget(self.t4LowBtn)
        self.t5LowBtn = QPushButton('T5 low')
        laserBit1Box.addWidget(self.t5LowBtn)
        self.t6LowBtn = QPushButton('T6 low')
        laserBit1Box.addWidget(self.t6LowBtn)
        self.t7LowBtn = QPushButton('T7 low')
        laserBit1Box.addWidget(self.t7LowBtn)
        self.t8LowBtn = QPushButton('T8 low')
        laserBit1Box.addWidget(self.t8LowBtn)
        self.t9LowBtn = QPushButton('T9 low')
        laserBit1Box.addWidget(self.t9LowBtn)
        self.t10LowBtn = QPushButton('T10 low')
        laserBit1Box.addWidget(self.t10LowBtn)
        self.t11LowBtn = QPushButton('T11 low')
        laserBit1Box.addWidget(self.t11LowBtn)
        self.t12LowBtn = QPushButton('T12 low')
        laserBit1Box.addWidget(self.t12LowBtn)
        
        # 레이저 BIT 설정
        laserBit2Box = QHBoxLayout()
        box.addLayout(laserBit2Box)

        self.t1HighBtn = QPushButton('T1 high')
        laserBit2Box.addWidget(self.t1HighBtn)
        self.t2HighBtn = QPushButton('T2 high')
        laserBit2Box.addWidget(self.t2HighBtn)
        self.t3HighBtn = QPushButton('T3 high')
        laserBit2Box.addWidget(self.t3HighBtn)
        self.t4HighBtn = QPushButton('T4 high')
        laserBit2Box.addWidget(self.t4HighBtn)
        self.t5HighBtn = QPushButton('T5 high')
        laserBit2Box.addWidget(self.t5HighBtn)
        self.t6HighBtn = QPushButton('T6 high')
        laserBit2Box.addWidget(self.t6HighBtn)
        self.t7HighBtn = QPushButton('T7 high')
        laserBit2Box.addWidget(self.t7HighBtn)
        self.t8HighBtn = QPushButton('T8 high')
        laserBit2Box.addWidget(self.t8HighBtn)
        self.t9HighBtn = QPushButton('T9 high')
        laserBit2Box.addWidget(self.t9HighBtn)
        self.t10HighBtn = QPushButton('T10 high')
        laserBit2Box.addWidget(self.t10HighBtn)
        self.t11HighBtn = QPushButton('T11 high')
        laserBit2Box.addWidget(self.t11HighBtn)
        self.t12HighBtn = QPushButton('T12 high')
        laserBit2Box.addWidget(self.t12HighBtn)
        
        # 레이저 BIT 설정
        laserBit3Box = QHBoxLayout()
        box.addLayout(laserBit3Box)
        
        self.pd1LowBtn = QPushButton('PD1 low')
        self.pd1LowBtn.setFixedWidth(148)
        laserBit3Box.addWidget(self.pd1LowBtn)
        self.pd2LowBtn = QPushButton('PD2 low')
        self.pd2LowBtn.setFixedWidth(148)
        laserBit3Box.addWidget(self.pd2LowBtn)
        self.pd1HighBtn = QPushButton('PD1 High')
        self.pd1HighBtn.setFixedWidth(148)
        laserBit3Box.addWidget(self.pd1HighBtn)
        self.pd2HighBtn = QPushButton('PD2 High')
        self.pd2HighBtn.setFixedWidth(148)
        laserBit3Box.addWidget(self.pd2HighBtn)
        self.wcuErrBtn = QPushButton('WCU_ERR')
        self.wcuErrBtn.setFixedWidth(148)
        laserBit3Box.addWidget(self.wcuErrBtn)
        self.fiberBrkBtn = QPushButton('FIBER_BROKEN')
        self.fiberBrkBtn.setFixedWidth(148)
        laserBit3Box.addWidget(self.fiberBrkBtn)
        self.dewPointBtn = QPushButton('DEW_POINT')
        self.dewPointBtn.setFixedWidth(148)
        laserBit3Box.addWidget(self.dewPointBtn)
        self.gateStaBtn = QPushButton('GATE_STA')
        self.gateStaBtn.setFixedWidth(148)
        laserBit3Box.addWidget(self.gateStaBtn)
        self.tecBtn = QPushButton('TEC')
        self.tecBtn.setFixedWidth(148)
        laserBit3Box.addWidget(self.tecBtn)
        self.tecErrBtn = QPushButton('TEC_ERR')
        self.tecErrBtn.setFixedWidth(148)
        laserBit3Box.addWidget(self.tecErrBtn)

        label = QLabel(' ')
        laserBit3Box.addWidget(label)

        # 레이저 BIT 설정
        laserBit4Box = QHBoxLayout()
        box.addLayout(laserBit4Box)
        
        self.pilotEnBtn = QPushButton('PILOT_EN')
        self.pilotEnBtn.setFixedWidth(148)
        laserBit4Box.addWidget(self.pilotEnBtn)
        self.interlockBtn = QPushButton('INTERLOCK')
        self.interlockBtn.setFixedWidth(148)
        laserBit4Box.addWidget(self.interlockBtn)
        self.standbyBtn = QPushButton('STANDBY')
        self.standbyBtn.setFixedWidth(148)
        laserBit4Box.addWidget(self.standbyBtn)
        self.globalEnBtn = QPushButton('GLOBAL_EN')
        self.globalEnBtn.setFixedWidth(148)
        laserBit4Box.addWidget(self.globalEnBtn)
        self.frEnBtn = QPushButton('FR_EN')
        self.frEnBtn.setFixedWidth(148)
        laserBit4Box.addWidget(self.frEnBtn)
        self.frEmBtn = QPushButton('FR_EM')
        self.frEmBtn.setFixedWidth(148)
        laserBit4Box.addWidget(self.frEmBtn)
        self.frFaultBtn = QPushButton('FR_FAULT')
        self.frFaultBtn.setFixedWidth(148)
        laserBit4Box.addWidget(self.frFaultBtn)
        self.frWarnBtn = QPushButton('FR_WARNING')
        self.frWarnBtn.setFixedWidth(148)
        laserBit4Box.addWidget(self.frWarnBtn)
        self.expiredBtn = QPushButton('EXPIRED')
        self.expiredBtn.setFixedWidth(148)
        laserBit4Box.addWidget(self.expiredBtn)

        label = QLabel(' ')
        laserBit4Box.addWidget(label)

        # 라벨
        rcvLabelBox = QHBoxLayout()
        box.addLayout(rcvLabelBox)

        label = QLabel('Receive')
        rcvLabelBox.addWidget(label)

        rcv1Box = QHBoxLayout()
        box.addLayout(rcv1Box)

        label = QLabel('DSN Rcv')
        label.setFixedWidth(148)
        rcv1Box.addWidget(label)
        self.dsnRcvEdit = QTextEdit()
        self.dsnRcvEdit.setFixedHeight(27)
        self.dsnRcvEdit.setFixedWidth(148)
        rcv1Box.addWidget(self.dsnRcvEdit)

        label = QLabel('OPMD Rcv')
        label.setFixedWidth(148)
        rcv1Box.addWidget(label)
        self.opmdRcvEdit = QTextEdit()
        self.opmdRcvEdit.setFixedHeight(27)
        self.opmdRcvEdit.setFixedWidth(148)
        rcv1Box.addWidget(self.opmdRcvEdit)

        label = QLabel('IMAX_CW Rcv')
        label.setFixedWidth(148)
        rcv1Box.addWidget(label)
        self.imaxCwRcvEdit = QTextEdit()
        self.imaxCwRcvEdit.setFixedHeight(27)
        self.imaxCwRcvEdit.setFixedWidth(148)
        rcv1Box.addWidget(self.imaxCwRcvEdit)

        label = QLabel('PMAX_CW Rcv')
        label.setFixedWidth(148)
        rcv1Box.addWidget(label)
        self.pmaxCwRcvEdit = QTextEdit()
        self.pmaxCwRcvEdit.setFixedHeight(27)
        self.pmaxCwRcvEdit.setFixedWidth(148)
        rcv1Box.addWidget(self.pmaxCwRcvEdit)

        label = QLabel('PSET Rcv')
        label.setFixedWidth(148)
        rcv1Box.addWidget(label)
        self.psetRcvEdit = QTextEdit()
        self.psetRcvEdit.setFixedHeight(27)
        self.psetRcvEdit.setFixedWidth(148)
        rcv1Box.addWidget(self.psetRcvEdit)

        label = QLabel('M_IMAX_CW Rcv')
        label.setFixedWidth(148)
        rcv1Box.addWidget(label)
        self.m_imaxCwRcvEdit = QTextEdit()
        self.m_imaxCwRcvEdit.setFixedHeight(27)
        self.m_imaxCwRcvEdit.setFixedWidth(148)
        rcv1Box.addWidget(self.m_imaxCwRcvEdit)    

        rcv2Box = QHBoxLayout()
        box.addLayout(rcv2Box)

        label = QLabel('M_PMAX_CW Rcv')
        label.setFixedWidth(148)
        rcv2Box.addWidget(label)
        self.m_pmaxCwRcvEdit = QTextEdit()
        self.m_pmaxCwRcvEdit.setFixedHeight(27)
        self.m_pmaxCwRcvEdit.setFixedWidth(148)
        rcv2Box.addWidget(self.m_pmaxCwRcvEdit)    

        label = QLabel('T1 Rcv')
        label.setFixedWidth(148)
        rcv2Box.addWidget(label)
        self.t1RcvEdit = QTextEdit()
        self.t1RcvEdit.setFixedHeight(27)
        self.t1RcvEdit.setFixedWidth(148)
        rcv2Box.addWidget(self.t1RcvEdit)

        label = QLabel('T2 Rcv')
        label.setFixedWidth(148)
        rcv2Box.addWidget(label)
        self.t2RcvEdit = QTextEdit()
        self.t2RcvEdit.setFixedHeight(27)
        self.t2RcvEdit.setFixedWidth(148)
        rcv2Box.addWidget(self.t2RcvEdit)

        label = QLabel('T3 Rcv')
        label.setFixedWidth(148)
        rcv2Box.addWidget(label)
        self.t3RcvEdit = QTextEdit()
        self.t3RcvEdit.setFixedHeight(27)
        self.t3RcvEdit.setFixedWidth(148)
        rcv2Box.addWidget(self.t3RcvEdit)

        label = QLabel('T4 Rcv')
        label.setFixedWidth(148)
        rcv2Box.addWidget(label)
        self.t4RcvEdit = QTextEdit()
        self.t4RcvEdit.setFixedHeight(27)
        self.t4RcvEdit.setFixedWidth(148)
        rcv2Box.addWidget(self.t4RcvEdit)

        label = QLabel('T5 Rcv')
        label.setFixedWidth(148)
        rcv2Box.addWidget(label)
        self.t5RcvEdit = QTextEdit()
        self.t5RcvEdit.setFixedHeight(27)
        self.t5RcvEdit.setFixedWidth(148)
        rcv2Box.addWidget(self.t5RcvEdit)        

        rcv3Box = QHBoxLayout()
        box.addLayout(rcv3Box)

        label = QLabel('T6 Rcv')
        label.setFixedWidth(148)
        rcv3Box.addWidget(label)
        self.t6RcvEdit = QTextEdit()
        self.t6RcvEdit.setFixedHeight(27)
        self.t6RcvEdit.setFixedWidth(148)
        rcv3Box.addWidget(self.t6RcvEdit)

        label = QLabel('T7 Rcv')
        label.setFixedWidth(148)
        rcv3Box.addWidget(label)
        self.t7RcvEdit = QTextEdit()
        self.t7RcvEdit.setFixedHeight(27)
        self.t7RcvEdit.setFixedWidth(148)
        rcv3Box.addWidget(self.t7RcvEdit)

        label = QLabel('T8 Rcv')
        label.setFixedWidth(148)
        rcv3Box.addWidget(label)
        self.t8RcvEdit = QTextEdit()
        self.t8RcvEdit.setFixedHeight(27)
        self.t8RcvEdit.setFixedWidth(148)
        rcv3Box.addWidget(self.t8RcvEdit)

        label = QLabel('T9 Rcv')
        label.setFixedWidth(148)
        rcv3Box.addWidget(label)
        self.t9RcvEdit = QTextEdit()
        self.t9RcvEdit.setFixedHeight(27)
        self.t9RcvEdit.setFixedWidth(148)
        rcv3Box.addWidget(self.t9RcvEdit)

        label = QLabel('T10 Rcv')
        label.setFixedWidth(148)
        rcv3Box.addWidget(label)
        self.t10RcvEdit = QTextEdit()
        self.t10RcvEdit.setFixedHeight(27)
        self.t10RcvEdit.setFixedWidth(148)
        rcv3Box.addWidget(self.t10RcvEdit)

        label = QLabel('T11 Rcv')
        label.setFixedWidth(148)
        rcv3Box.addWidget(label)
        self.t11RcvEdit = QTextEdit()
        self.t11RcvEdit.setFixedHeight(27)
        self.t11RcvEdit.setFixedWidth(148)
        rcv3Box.addWidget(self.t11RcvEdit)

        rcv4Box = QHBoxLayout()
        box.addLayout(rcv4Box)

        label = QLabel('ENV_TEMP Rcv')
        label.setFixedWidth(148)
        rcv4Box.addWidget(label)
        self.envTempRcvEdit = QTextEdit()
        self.envTempRcvEdit.setFixedHeight(27)
        rcv4Box.addWidget(self.envTempRcvEdit)

        label = QLabel('ENV_HUMID Rcv')
        label.setFixedWidth(148)
        rcv4Box.addWidget(label)
        self.envHumidRcvEdit = QTextEdit()
        self.envHumidRcvEdit.setFixedHeight(27)
        rcv4Box.addWidget(self.envHumidRcvEdit)

        label = QLabel('ENV_DEW Rcv')
        label.setFixedWidth(148)
        rcv4Box.addWidget(label)
        self.envDewRcvEdit = QTextEdit()
        self.envDewRcvEdit.setFixedHeight(27)
        rcv4Box.addWidget(self.envDewRcvEdit)

        label = QLabel('PD1 Rcv')
        label.setFixedWidth(148)
        rcv4Box.addWidget(label)
        self.pd1RcvEdit = QTextEdit()
        self.pd1RcvEdit.setFixedHeight(27)
        rcv4Box.addWidget(self.pd1RcvEdit)

        label = QLabel('PD2 Rcv')
        label.setFixedWidth(148)
        rcv4Box.addWidget(label)
        self.pd2RcvEdit = QTextEdit()
        self.pd2RcvEdit.setFixedHeight(27)
        rcv4Box.addWidget(self.pd2RcvEdit)

        label = QLabel('PDPOW Rcv')
        label.setFixedWidth(148)
        rcv4Box.addWidget(label)
        self.pdpowRcvEdit = QTextEdit()
        self.pdpowRcvEdit.setFixedHeight(27)
        rcv4Box.addWidget(self.pdpowRcvEdit)

        gb.setLayout(box)

        # 냉각장치 제어부
        chillerBox = QHBoxLayout()

        gb = QGroupBox('Chiller Control')
        chillerBox.addWidget(gb)

        box = QVBoxLayout()

        tempSetBox = QHBoxLayout()
        box.addLayout(tempSetBox)

        self.chillerCntBtn = QPushButton('Connect')
        self.chillerCntBtn.setFixedWidth(148)
        self.chillerCntBtn.clicked.connect(self.chillerConnect)
        tempSetBox.addWidget(self.chillerCntBtn)

        self.cStartEdit = QTextEdit()
        self.cStartEdit.setFixedHeight(27)
        self.cStartEdit.setFixedWidth(148)
        tempSetBox.addWidget(self.cStartEdit)
        self.cStartBtn = QPushButton('START')
        self.cStartBtn.setAutoDefault(True)
        self.cStartBtn.setFixedWidth(148)
        # self.cStartBtn.clicked.connect(self.enable)
        tempSetBox.addWidget(self.cStartBtn)
        label = QLabel(' ')
        tempSetBox.addWidget(label)

        chillerControlBox = QHBoxLayout()
        box.addLayout(chillerControlBox)

        self.cBitBtn = QPushButton('BIT')
        self.cBitBtn.setAutoDefault(True)
        self.cBitBtn.setFixedWidth(148)
        # self.cBitBtn.clicked.connect(self.enable)
        chillerControlBox.addWidget(self.cBitBtn)

        self.targetTempSetEdit = QTextEdit()
        self.targetTempSetEdit.setFixedHeight(27)
        self.targetTempSetEdit.setFixedWidth(148)
        chillerControlBox.addWidget(self.targetTempSetEdit)
        self.tragetTempSetBtn = QPushButton('Target Temp Set')
        self.tragetTempSetBtn.setAutoDefault(True)
        self.tragetTempSetBtn.setFixedWidth(148)
        # self.tragetTempSetBtn.clicked.connect(self.enable)
        chillerControlBox.addWidget(self.tragetTempSetBtn)

        self.highTemp1SetEdit = QTextEdit()
        self.highTemp1SetEdit.setFixedHeight(27)
        self.highTemp1SetEdit.setFixedWidth(148)
        chillerControlBox.addWidget(self.highTemp1SetEdit)
        self.highTemp1SetBtn = QPushButton('High Temp 1 Set')
        self.highTemp1SetBtn.setAutoDefault(True)
        self.highTemp1SetBtn.setFixedWidth(148)
        # self.highTemp1SetBtn.clicked.connect(self.enable)
        chillerControlBox.addWidget(self.highTemp1SetBtn)

        self.highTemp2SetEdit = QTextEdit()
        self.highTemp2SetEdit.setFixedHeight(27)
        self.highTemp2SetEdit.setFixedWidth(148)
        chillerControlBox.addWidget(self.highTemp2SetEdit)
        self.highTemp2SetBtn = QPushButton('High Temp 2 Set')
        self.highTemp2SetBtn.setAutoDefault(True)
        self.highTemp2SetBtn.setFixedWidth(148)
        # self.highTemp2SetBtn.clicked.connect(self.enable)
        chillerControlBox.addWidget(self.highTemp2SetBtn)

        self.lowTemp1SetEdit = QTextEdit()
        self.lowTemp1SetEdit.setFixedHeight(27)
        self.lowTemp1SetEdit.setFixedWidth(148)
        chillerControlBox.addWidget(self.lowTemp1SetEdit)
        self.lowTemp1SetBtn = QPushButton('Low Temp 1 Set')
        self.lowTemp1SetBtn.setAutoDefault(True)
        self.lowTemp1SetBtn.setFixedWidth(148)
        # self.lowTemp1SetBtn.clicked.connect(self.enable)
        chillerControlBox.addWidget(self.lowTemp1SetBtn)

        self.lowTemp2SetEdit = QTextEdit()
        self.lowTemp2SetEdit.setFixedHeight(27)
        self.lowTemp2SetEdit.setFixedWidth(148)
        chillerControlBox.addWidget(self.lowTemp2SetEdit)
        self.lowTemp2SetBtn = QPushButton('Low Temp 2 Set')
        self.lowTemp2SetBtn.setAutoDefault(True)
        self.lowTemp2SetBtn.setFixedWidth(148)
        # self.lowTemp2SetBtn.clicked.connect(self.enable)
        chillerControlBox.addWidget(self.lowTemp2SetBtn)

        label = QLabel(' ')
        chillerControlBox.addWidget(label)

        tempRcvBox = QHBoxLayout()
        box.addLayout(tempRcvBox)

        self.tragetTempBtn = QPushButton('Target Temp Rcv')
        self.tragetTempBtn.setAutoDefault(True)
        self.tragetTempBtn.setFixedWidth(148)
        # self.tragetTempBtn.clicked.connect(self.enable)
        tempRcvBox.addWidget(self.tragetTempBtn)
        self.targetTempRcvEdit = QTextEdit()
        self.targetTempRcvEdit.setFixedHeight(27)
        self.targetTempRcvEdit.setFixedWidth(148)
        tempRcvBox.addWidget(self.targetTempRcvEdit)

        self.highTemp1Btn = QPushButton('High Temp 1 Rcv')
        self.highTemp1Btn.setAutoDefault(True)
        self.highTemp1Btn.setFixedWidth(148)
        # self.highTemp1Btn.clicked.connect(self.enable)
        tempRcvBox.addWidget(self.highTemp1Btn)
        self.highTemp1RcvEdit = QTextEdit()
        self.highTemp1RcvEdit.setFixedHeight(27)
        self.highTemp1RcvEdit.setFixedWidth(148)
        tempRcvBox.addWidget(self.highTemp1RcvEdit)

        self.highTemp2Btn = QPushButton('High Temp 1 Rcv')
        self.highTemp2Btn.setAutoDefault(True)
        self.highTemp2Btn.setFixedWidth(148)
        # self.highTemp2Btn.clicked.connect(self.enable)
        tempRcvBox.addWidget(self.highTemp2Btn)
        self.highTemp2RcvEdit = QTextEdit()
        self.highTemp2RcvEdit.setFixedHeight(27)
        self.highTemp2RcvEdit.setFixedWidth(148)
        tempRcvBox.addWidget(self.highTemp2RcvEdit)

        self.lowTemp1Btn = QPushButton('Low Temp 1 Rcv')
        self.lowTemp1Btn.setAutoDefault(True)
        self.lowTemp1Btn.setFixedWidth(148)
        # self.lowTemp1Btn.clicked.connect(self.enable)
        tempRcvBox.addWidget(self.lowTemp1Btn)
        self.lowTemp1RcvEdit = QTextEdit()
        self.lowTemp1RcvEdit.setFixedHeight(27)
        self.lowTemp1RcvEdit.setFixedWidth(148)
        tempRcvBox.addWidget(self.lowTemp1RcvEdit)

        self.lowTemp2Btn = QPushButton('Low Temp 2 Rcv')
        self.lowTemp2Btn.setAutoDefault(True)
        self.lowTemp2Btn.setFixedWidth(148)
        # self.lowTemp2Btn.clicked.connect(self.enable)
        tempRcvBox.addWidget(self.lowTemp2Btn)
        self.lowTemp2RcvEdit = QTextEdit()
        self.lowTemp2RcvEdit.setFixedHeight(27)
        self.lowTemp2RcvEdit.setFixedWidth(148)
        tempRcvBox.addWidget(self.lowTemp2RcvEdit)
        label = QLabel(' ')
        tempRcvBox.addWidget(label)

        realTempRcvBox = QHBoxLayout()
        box.addLayout(realTempRcvBox)

        self.ch0TempBtn = QPushButton('CH0 Temp Rcv')
        self.ch0TempBtn.setAutoDefault(True)
        self.ch0TempBtn.setFixedWidth(148)
        # self.ch0TempBtn.clicked.connect(self.enable)
        realTempRcvBox.addWidget(self.ch0TempBtn)
        self.ch0TempRcvEdit = QTextEdit()
        self.ch0TempRcvEdit.setFixedHeight(27)
        self.ch0TempRcvEdit.setFixedWidth(148)
        realTempRcvBox.addWidget(self.ch0TempRcvEdit)

        self.ch1TempBtn = QPushButton('CH1 Temp Rcv')
        self.ch1TempBtn.setAutoDefault(True)
        self.ch1TempBtn.setFixedWidth(148)
        # self.ch1TempBtn.clicked.connect(self.enable)
        realTempRcvBox.addWidget(self.ch1TempBtn)
        self.ch1TempRcvEdit = QTextEdit()
        self.ch1TempRcvEdit.setFixedHeight(27)
        self.ch1TempRcvEdit.setFixedWidth(148)
        realTempRcvBox.addWidget(self.ch1TempRcvEdit)

        self.flowBtn = QPushButton('Flow Rcv')
        self.flowBtn.setAutoDefault(True)
        self.flowBtn.setFixedWidth(148)
        # self.flowBtn.clicked.connect(self.enable)
        realTempRcvBox.addWidget(self.flowBtn)
        self.flowRcvEdit = QTextEdit()
        self.flowRcvEdit.setFixedHeight(27)
        self.flowRcvEdit.setFixedWidth(148)
        realTempRcvBox.addWidget(self.flowRcvEdit)

        self.pidBtn = QPushButton('PID Rcv')
        self.pidBtn.setAutoDefault(True)
        self.pidBtn.setFixedWidth(148)
        # self.pidBtn.clicked.connect(self.enable)
        realTempRcvBox.addWidget(self.pidBtn)
        self.pidRcvEdit = QTextEdit()
        self.pidRcvEdit.setFixedHeight(27)
        self.pidRcvEdit.setFixedWidth(148)
        realTempRcvBox.addWidget(self.pidRcvEdit)
        label = QLabel(' ')
        realTempRcvBox.addWidget(label)

        # 레이저 BIT 설정
        cStsBox = QHBoxLayout()
        box.addLayout(cStsBox)

        self.cStanbyBtn = QPushButton('STANDBY')
        self.cStanbyBtn.setFixedWidth(148)
        cStsBox.addWidget(self.cStanbyBtn)
        self.cStartCheckBtn = QPushButton('START CHECK')
        self.cStartCheckBtn.setFixedWidth(148)
        cStsBox.addWidget(self.cStartCheckBtn)
        self.cPumpStartBtn = QPushButton('PUMP START')
        self.cPumpStartBtn.setFixedWidth(148)
        cStsBox.addWidget(self.cPumpStartBtn)
        self.cPumpDelayBtn = QPushButton('PUMP DELAY')
        self.cPumpDelayBtn.setFixedWidth(148)
        cStsBox.addWidget(self.cPumpDelayBtn)
        self.cPrepStartBtn = QPushButton('PREP START')
        self.cPrepStartBtn.setFixedWidth(148)
        cStsBox.addWidget(self.cPrepStartBtn)
        self.cPrepDelayBtn = QPushButton('PREP DELAY')
        self.cPrepDelayBtn.setFixedWidth(148)
        cStsBox.addWidget(self.cPrepDelayBtn)
        self.cReadyStartBtn = QPushButton('READY START')
        self.cReadyStartBtn.setFixedWidth(148)
        cStsBox.addWidget(self.cReadyStartBtn)
        self.cReadyDelayBtn = QPushButton('READY DELAY')
        self.cReadyDelayBtn.setFixedWidth(148)
        cStsBox.addWidget(self.cReadyDelayBtn)
        self.cRunBtn = QPushButton('RUN')
        self.cRunBtn.setFixedWidth(148)
        cStsBox.addWidget(self.cRunBtn)
        self.cStopBtn = QPushButton('STOP')
        self.cStopBtn.setFixedWidth(148)
        cStsBox.addWidget(self.cStopBtn)
        self.cStopDelayBtn = QPushButton('STOP DELAY')
        self.cStopDelayBtn.setFixedWidth(148)
        cStsBox.addWidget(self.cStopDelayBtn)
        label = QLabel(' ')
        cStsBox.addWidget(label)

        # 레이저 BIT 설정
        cErr1Box = QHBoxLayout()
        box.addLayout(cErr1Box)

        self.cOverHeatBtn = QPushButton('OVER HEAT')
        cErr1Box.addWidget(self.cOverHeatBtn)
        self.cOverCurBtn = QPushButton('OVER CURRENT')
        cErr1Box.addWidget(self.cOverCurBtn)
        self.cLowPresBtn = QPushButton('Low PRESSURE')
        cErr1Box.addWidget(self.cLowPresBtn)
        self.cHighPresBtn = QPushButton('HIGH PRESSURE')
        cErr1Box.addWidget(self.cHighPresBtn)
        self.cFMSBtn = QPushButton('FLOW METER SENSOR')
        cErr1Box.addWidget(self.cFMSBtn)
        self.cFSSBtn = QPushButton('FLOW SWITCH SENSOR')
        cErr1Box.addWidget(self.cFSSBtn)
        self.cFlowMeterBtn = QPushButton('FLOW METER')
        cErr1Box.addWidget(self.cFlowMeterBtn)
        self.cFlowSwitchBtn = QPushButton('FLOW SWITCH')
        cErr1Box.addWidget(self.cFlowSwitchBtn)
        self.cTSBtn = QPushButton('TEMP SENSOR')
        cErr1Box.addWidget(self.cTSBtn)
        self.cLSBtn = QPushButton('LEVEL SENSOR')
        cErr1Box.addWidget(self.cLSBtn)
        self.cLL2Btn = QPushButton('LOW LEVEL 2')
        cErr1Box.addWidget(self.cLL2Btn)
        self.cLL1Btn = QPushButton('LOW LEVEL 1')
        cErr1Box.addWidget(self.cLL1Btn)

        cErr2Box = QHBoxLayout()
        box.addLayout(cErr2Box)

        self.cLT2Btn = QPushButton('LOW TEMP 2')
        self.cLT2Btn.setFixedWidth(148)
        cErr2Box.addWidget(self.cLT2Btn)
        self.cLT1Btn = QPushButton('LOW TEMP1')
        self.cLT1Btn.setFixedWidth(148)
        cErr2Box.addWidget(self.cLT1Btn)
        self.cHT2Btn = QPushButton('HIGH TEMP2')
        self.cHT2Btn.setFixedWidth(148)
        cErr2Box.addWidget(self.cHT2Btn)
        self.cHT1Btn = QPushButton('HIGH TEMP1')
        self.cHT1Btn.setFixedWidth(148)
        cErr2Box.addWidget(self.cHT1Btn)
        label = QLabel(' ')
        cErr2Box.addWidget(label)

        chillerRcvBox = QHBoxLayout()
        box.addLayout(chillerRcvBox)

        self.chillerCmdRcvEdit = QTextEdit()
        self.chillerCmdRcvEdit.setFixedHeight(27)
        self.chillerCmdRcvEdit.setFixedWidth(148)
        chillerRcvBox.addWidget(self.chillerCmdRcvEdit)

        self.chillerScRcvEdit = QTextEdit()
        self.chillerScRcvEdit.setFixedHeight(27)
        self.chillerScRcvEdit.setFixedWidth(148)
        chillerRcvBox.addWidget(self.chillerScRcvEdit)

        self.chillerLengthRcvEdit = QTextEdit()
        self.chillerLengthRcvEdit.setFixedHeight(27)
        self.chillerLengthRcvEdit.setFixedWidth(148)
        chillerRcvBox.addWidget(self.chillerLengthRcvEdit)

        self.chillerDataRcvEdit = QTextEdit()
        self.chillerDataRcvEdit.setFixedHeight(27)
        self.chillerDataRcvEdit.setFixedWidth(148)
        chillerRcvBox.addWidget(self.chillerDataRcvEdit)

        label = QLabel(' ')
        chillerRcvBox.addWidget(label)

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

        # Cmd
        self.cmdMsg = QTextEdit()
        self.cmdMsg.setFixedHeight(30)
        self.cmdMsg.setText('STATUS=')
        messageBox.addWidget(self.cmdMsg)
        # data
        self.dataMsg = QTextEdit()
        self.dataMsg.setFixedHeight(30)
        self.dataMsg.setText('ffffffffffffffff')
        messageBox.addWidget(self.dataMsg)
        # 전송
        self.sendBtn = QPushButton('보내기')
        self.sendBtn.setAutoDefault(True)
        self.sendBtn.clicked.connect(self.defaultMsg)
        messageBox.addWidget(self.sendBtn)
        # Cmd
        self.chillerCmd = QTextEdit()
        self.chillerCmd.setFixedHeight(30)
        self.chillerCmd.setText('040')
        messageBox.addWidget(self.chillerCmd)
        # Sc
        self.chillerSc = QTextEdit()
        self.chillerSc.setFixedHeight(30)
        self.chillerSc.setText('1')
        messageBox.addWidget(self.chillerSc)
        # Length
        self.chillerLength = QTextEdit()
        self.chillerLength.setFixedHeight(30)
        self.chillerLength.setText('05')
        messageBox.addWidget(self.chillerLength)
        # data
        self.chillerData = QTextEdit()
        self.chillerData.setFixedHeight(30)
        self.chillerData.setText('+20.0')
        messageBox.addWidget(self.chillerData)
        # 전송
        self.chillerSendBtn = QPushButton('보내기')
        self.chillerSendBtn.setAutoDefault(True)
        self.chillerSendBtn.clicked.connect(self.defaultChiller)
        messageBox.addWidget(self.chillerSendBtn)
        # 채팅창 삭제
        self.clearBtn = QPushButton('채팅창 지움')
        self.clearBtn.clicked.connect(self.clearMsg)
        messageBox.addWidget(self.clearBtn)

        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(laserBox)
        vbox.addLayout(chillerBox)
        vbox.addLayout(infobox)
        self.setLayout(vbox)

        self.show()

    def laserConnect(self):
        if self.ser.bConnect == False:
            if self.ser.connect():
                self.laserCntBtn.setStyleSheet("background-color: green")
                self.laserCntBtn.setText('Connected')
            else:
                self.ser.stop()
                self.recvmsg.clear()
                self.laserCntBtn.setText('Connect')
                self.laserCntBtn.setStyleSheet("background-color: lightgray")
        else:
            self.ser.stop()
            self.recvmsg.clear()
            self.laserCntBtn.setText('Connect')
            self.laserCntBtn.setStyleSheet("background-color: lightgray")

    def updateLaser(self, cmd, data):
        # print(cmd, data)
        if cmd == 'STATUS':
            if int(data[0], 16)&1 == 1:
                self.t1LowBtn.setStyleSheet("background-color: red")
            else:
                self.t1LowBtn.setStyleSheet("background-color: lightgray")
            if int(data[0], 16)&2 == 2:
                self.t2LowBtn.setStyleSheet("background-color: red")
            else:
                self.t2LowBtn.setStyleSheet("background-color: lightgray")
            if int(data[0], 16)&4 == 4:
                self.t3LowBtn.setStyleSheet("background-color: red")
            else:
                self.t3LowBtn.setStyleSheet("background-color: lightgray")           
            if int(data[0], 16)&8 == 8:
                self.t4LowBtn.setStyleSheet("background-color: red")
            else:
                self.t4LowBtn.setStyleSheet("background-color: lightgray")
            if int(data[1], 16)&1 == 1:
                self.t5LowBtn.setStyleSheet("background-color: red")
            else:
                self.t5LowBtn.setStyleSheet("background-color: lightgray")
            if int(data[1], 16)&2 == 2:
                self.t6LowBtn.setStyleSheet("background-color: red")
            else:
                self.t6LowBtn.setStyleSheet("background-color: lightgray")
            if int(data[1], 16)&4 == 4:
                self.t7LowBtn.setStyleSheet("background-color: red")
            else:
                self.t7LowBtn.setStyleSheet("background-color: lightgray")           
            if int(data[1], 16)&8 == 8:
                self.t8LowBtn.setStyleSheet("background-color: red")
            else:
                self.t8LowBtn.setStyleSheet("background-color: lightgray")
            if int(data[2], 16)&1 == 1:
                self.t9HighBtn.setStyleSheet("background-color: red")
            else:
                self.t9HighBtn.setStyleSheet("background-color: lightgray")
            if int(data[2], 16)&2 == 2:
                self.t10HighBtn.setStyleSheet("background-color: red")
            else:
                self.t10HighBtn.setStyleSheet("background-color: lightgray")
            if int(data[2], 16)&4 == 4:
                self.t11HighBtn.setStyleSheet("background-color: red")
            else:
                self.t11HighBtn.setStyleSheet("background-color: lightgray")          
            if int(data[2], 16)&8 == 8:
                self.t12HighBtn.setStyleSheet("background-color: red")
            else:
                self.t12HighBtn.setStyleSheet("background-color: lightgray")
            if int(data[3], 16)&1 == 1:
                self.t9LowBtn.setStyleSheet("background-color: red")
            else:
                self.t9LowBtn.setStyleSheet("background-color: lightgray")
            if int(data[3], 16)&2 == 2:
                self.t10LowBtn.setStyleSheet("background-color: red")
            else:
                self.t10LowBtn.setStyleSheet("background-color: lightgray")
            if int(data[3], 16)&4 == 4:
                self.t11LowBtn.setStyleSheet("background-color: red")
            else:
                self.t11LowBtn.setStyleSheet("background-color: lightgray")          
            if int(data[3], 16)&8 == 8:
                self.t12LowBtn.setStyleSheet("background-color: red")
            else:
                self.t12LowBtn.setStyleSheet("background-color: lightgray")
            if int(data[4], 16)&1 == 1:
                self.pd1HighBtn.setStyleSheet("background-color: red")
            else:
                self.pd1HighBtn.setStyleSheet("background-color: lightgray")
            if int(data[4], 16)&2 == 2:
                self.pd2HighBtn.setStyleSheet("background-color: red")
            else:
                self.pd2HighBtn.setStyleSheet("background-color: lightgray")
            if int(data[5], 16)&1 == 1:
                self.pd1LowBtn.setStyleSheet("background-color: red")
            else:
                self.pd1LowBtn.setStyleSheet("background-color: lightgray")
            if int(data[5], 16)&2 == 2:
                self.pd2LowBtn.setStyleSheet("background-color: red")
            else:
                self.pd2LowBtn.setStyleSheet("background-color: lightgray")
            if int(data[6], 16)&1 == 1:
                self.wcuErrBtn.setStyleSheet("background-color: red")
            else:
                self.wcuErrBtn.setStyleSheet("background-color: lightgray")
            if int(data[6], 16)&8 == 8:
                self.fiberBrkBtn.setStyleSheet("background-color: red")
            else:
                self.fiberBrkBtn.setStyleSheet("background-color: lightgray")
            if int(data[7], 16)&1 == 1:
                self.dewPointBtn.setStyleSheet("background-color: red")
            else:
                self.dewPointBtn.setStyleSheet("background-color: lightgray")
            if int(data[7], 16)&2 == 2:
                self.gateStaBtn.setStyleSheet("background-color: green")
            else:
                self.gateStaBtn.setStyleSheet("background-color: lightgray")
            if int(data[7], 16)&4 == 4:
                self.tecBtn.setStyleSheet("background-color: green")
            else:
                self.tecBtn.setStyleSheet("background-color: lightgray")         
            if int(data[7], 16)&8 == 8:
                self.tecErrBtn.setStyleSheet("background-color: red")
            else:
                self.tecErrBtn.setStyleSheet("background-color: lightgray")   
            if int(data[10], 16)&1 == 1:
                self.t1HighBtn.setStyleSheet("background-color: red")
            else:
                self.t1HighBtn.setStyleSheet("background-color: lightgray")
            if int(data[10], 16)&2 == 2:
                self.t2HighBtn.setStyleSheet("background-color: red")
            else:
                self.t2HighBtn.setStyleSheet("background-color: lightgray")
            if int(data[10], 16)&4 == 4:
                self.t3HighBtn.setStyleSheet("background-color: red")
            else:
                self.t3HighBtn.setStyleSheet("background-color: lightgray")           
            if int(data[10], 16)&8 == 8:
                self.t4HighBtn.setStyleSheet("background-color: red")
            else:
                self.t4HighBtn.setStyleSheet("background-color: lightgray")
            if int(data[11], 16)&1 == 1:
                self.t5HighBtn.setStyleSheet("background-color: red")
            else:
                self.t5HighBtn.setStyleSheet("background-color: lightgray")
            if int(data[11], 16)&2 == 2:
                self.t6HighBtn.setStyleSheet("background-color: red")
            else:
                self.t6HighBtn.setStyleSheet("background-color: lightgray")
            if int(data[11], 16)&4 == 4:
                self.t7HighBtn.setStyleSheet("background-color: red")
            else:
                self.t7HighBtn.setStyleSheet("background-color: lightgray")           
            if int(data[11], 16)&8 == 8:
                self.t8HighBtn.setStyleSheet("background-color: red")
            else:
                self.t8HighBtn.setStyleSheet("background-color: lightgray")
            if int(data[13], 16)&1 == 1:
                self.pilotEnBtn.setStyleSheet("background-color: green")
            else:
                self.pilotEnBtn.setStyleSheet("background-color: lightgray")
            if int(data[13], 16)&2 == 2:
                self.interlockBtn.setStyleSheet("background-color: red")
            else:
                self.interlockBtn.setStyleSheet("background-color: lightgray")
            if int(data[13], 16)&4 == 4:
                self.standbyBtn.setStyleSheet("background-color: green")
            else:
                self.standbyBtn.setStyleSheet("background-color: lightgray")  
            if int(data[14], 16)&1 == 1:
                self.globalEnBtn.setStyleSheet("background-color: green")
            else:
                self.globalEnBtn.setStyleSheet("background-color: lightgray")
            if int(data[14], 16)&2 == 2:
                self.frEnBtn.setStyleSheet("background-color: red")
            else:
                self.frEnBtn.setStyleSheet("background-color: lightgray")
            if int(data[14], 16)&4 == 4:
                self.frEmBtn.setStyleSheet("background-color: red")
            else:
                self.frEmBtn.setStyleSheet("background-color: lightgray")         
            if int(data[14], 16)&8 == 8:
                self.frFaultBtn.setStyleSheet("background-color: red")
            else:
                self.frFaultBtn.setStyleSheet("background-color: lightgray") 
            if int(data[15], 16)&1 == 1:
                self.frWarnBtn.setStyleSheet("background-color: red")
            else:
                self.frWarnBtn.setStyleSheet("background-color: lightgray") 
            if int(data[15], 16)&8 == 8:
                self.expiredBtn.setStyleSheet("background-color: red")
            else:
                self.expiredBtn.setStyleSheet("background-color: lightgray") 

        elif cmd == 'DSN':
            self.dsnRcvEdit.setText(data)
        elif cmd == 'OPMD':
            self.opmdRcvEdit.setText(data)
        elif cmd == 'IMAX_CW':
            imax_cw = int(data,16)/100
            self.imaxCwRcvEdit.setText(str(imax_cw))
        elif cmd == 'PMAX_CW':
            pmax_cw = int(data,16)/10
            self.pmaxCwRcvEdit.setText(str(pmax_cw))
        elif cmd == 'ISET':
            iset = int(data,16)/100
            self.psetRcvEdit.setText(str(iset))
        elif cmd == 'TOFW':
            t9, t10, t11 = data.split(',')
            t9 = int(t9,16)/10
            self.t9RcvEdit.setText(str(t9))
            t10 = int(t10,16)/10
            self.t10RcvEdit.setText(str(t10))
            t11 = int(t11,16)/10
            self.t11RcvEdit.setText(str(t11))
        elif cmd == 'TMONRT':
            t1, t2, t3, t4, t5, t6, t7, t8 = data.split(',')
            t1 = int(t1,16)/10
            self.t1RcvEdit.setText(str(t1))
            t2 = int(t2,16)/10
            self.t2RcvEdit.setText(str(t2))
            t3 = int(t3,16)/10
            self.t3RcvEdit.setText(str(t3))
            t4 = int(t4,16)/10
            self.t4RcvEdit.setText(str(t4))
            t5 = int(t5,16)/10
            self.t5RcvEdit.setText(str(t5))
            t6 = int(t6,16)/10
            self.t6RcvEdit.setText(str(t6))
            t7 = int(t7,16)/10
            self.t7RcvEdit.setText(str(t7))
            t8 = int(t8,16)/10
            self.t8RcvEdit.setText(str(t8))
        elif cmd == 'ENVC':
            temp, humid, dew = data.split(',')
            temp = int(temp,16)/100
            self.envTempRcvEdit.setText(str(temp))
            humid = int(humid,16)/100
            self.envHumidRcvEdit.setText(str(humid))
            dew = int(dew,16)/100
            self.envDewRcvEdit.setText(str(dew))
        elif cmd == 'PD':
            pd1, pd2, reserved = data.split(',')
            self.pd1RcvEdit.setText(str(int(pd1,16)))
            self.pd2RcvEdit.setText(str(int(pd2,16)))
        elif cmd == 'PDPOW':
            self.pdpowRcvEdit.setText(str(int(data,16)))
        elif cmd == 'ENABLED':
            self.enableBtn.setStyleSheet("background-color: green")

        elif cmd == 'PILOT ENABLED':
            self.pilotEnBtn.setStyleSheet("background-color: green")

        elif cmd == 'ISETMODE':
            print(data)
            if data == 'P':
                self.setModeBtn.setStyleSheet("background-color: green")  
            elif data == 'I':
                self.setModeBtn.setStyleSheet("background-color: yellow")  
            else:
                self.setModeBtn.setStyleSheet("background-color: red")  
        else:
            print(cmd)

    def disconnectLaser(self):
        self.laserConnect.setText('Connect') 

    def defaultMsg(self):
        cmd = self.cmdMsg.toPlainText()
        data = self.dataMsg.toPlainText()
        self.ser.send(cmd, data)

    def chillerConnect(self):
        if self.chiller.bConnect == False:
            if self.chiller.connect():
                self.chillerCntBtn.setStyleSheet("background-color: green")
                self.chillerCntBtn.setText('Connected')
            else:
                self.chiller.stop()
                self.recvmsg.clear()
                self.chillerCntBtn.setText('Connect')
                self.chillerCntBtn.setStyleSheet("background-color: lightgray")
        else:
            self.chiller.stop()
            self.recvmsg.clear()
            self.chillerCntBtn.setText('Connect')
            self.chillerCntBtn.setStyleSheet("background-color: lightgray")

    def updateChiller(self, cmd, sc, length, data):
        self.chillerCmdRcvEdit.setText(str(cmd))
        self.chillerScRcvEdit.setText(str(sc))
        self.chillerLengthRcvEdit.setText(str(length))
        self.chillerDataRcvEdit.setText(data)

        if cmd == '040':
            if sc == '1':
                self.targetTempRcvEdit.setText(data)
            elif sc == '3':
                self.tragetTempBtn.setStyleSheet("background-color: green")
            elif sc == '4':
                self.tragetTempBtn.setStyleSheet("background-color: red")
            else:
                self.tragetTempBtn.setStyleSheet("background-color: lightgray")

        elif cmd == '041':
            if sc == '1':
                self.highTemp1RcvEdit.setText(data)
            elif sc == '3':
                self.highTemp1Btn.setStyleSheet("background-color: green")
            elif sc == '4':
                self.highTemp1Btn.setStyleSheet("background-color: red")
            else:
                self.highTemp1Btn.setStyleSheet("background-color: lightgray")

        elif cmd == '042':
            if sc == '1':
                self.highTemp2RcvEdit.setText(data)
            elif sc == '3':
                self.highTemp2Btn.setStyleSheet("background-color: green")
            elif sc == '4':
                self.highTemp2Btn.setStyleSheet("background-color: red")
            else:
                self.highTemp2Btn.setStyleSheet("background-color: lightgray")

        elif cmd == '043':
            if sc == '1':
                self.lowTemp1RcvEdit.setText(data)
            elif sc == '3':
                self.lowTemp1Btn.setStyleSheet("background-color: green")
            elif sc == '4':
                self.lowTemp1Btn.setStyleSheet("background-color: red")
            else:
                self.lowTemp1Btn.setStyleSheet("background-color: lightgray")

        elif cmd == '044':
            if sc == '1':
                self.lowTemp2RcvEdit.setText(data)
            elif sc == '3':
                self.lowTemp2Btn.setStyleSheet("background-color: green")
            elif sc == '4':
                self.lowTemp2Btn.setStyleSheet("background-color: red")
            else:
                self.lowTemp2Btn.setStyleSheet("background-color: lightgray")

        elif cmd == '150':
            self.ch0TempRcvEdit.setText(data)
        elif cmd == '151':
            self.ch1TempRcvEdit.setText(data)
        elif cmd == '154':
            if sc == '1':
                if data == '0':
                    self.cStanbyBtn.setStyleSheet("background-color: green")
                elif data == '1':
                    self.cStartCheckBtn.setStyleSheet("background-color: green")
                elif data == '2':
                    self.cPumpStartBtn.setStyleSheet("background-color: green")
                elif data == '3':
                    self.cPumpDelayBtn.setStyleSheet("background-color: green")
                elif data == '4':
                    self.cPrepStartBtn.setStyleSheet("background-color: green")
                elif data == '5':
                    self.cPrepDelayBtn.setStyleSheet("background-color: green")
                elif data == '6':
                    self.cReadyStartBtn.setStyleSheet("background-color: green")
                elif data == '7':
                    self.cReadyDelayBtn.setStyleSheet("background-color: green")
                elif data == '8':
                    self.cRunBtn.setStyleSheet("background-color: green")
                elif data == '9':
                    self.cStopBtn.setStyleSheet("background-color: green")
                elif data == '10':
                    self.cStopDelayBtnBtn.setStyleSheet("background-color: green")
            elif sc == '3':
                self.cStartBtn.setStyleSheet("background-color: green")
            elif sc == '4':
                self.cStartBtn.setStyleSheet("background-color: red")
            else:
                self.cStartBtn.setStyleSheet("background-color: lightgray")
        elif cmd == '156':
            if int(data) & 0b0000000000000001 == 0b0000000000000001:
                self.cOverHeatBtn.setStyleSheet("background-color: red")
            else:
                self.cOverHeatBtn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0000000000000010 == 0b0000000000000010:
                self.cOverCurBtn.setStyleSheet("background-color: red")
            else:
                self.cOverCurBtn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0000000000000100 == 0b0000000000000100:
                self.cLowPresBtn.setStyleSheet("background-color: red")
            else:
                self.cLowPresBtn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0000000000001000 == 0b0000000000001000:
                self.cHighPresBtn.setStyleSheet("background-color: red")
            else:
                self.cHighPresBtn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0000000000010000 == 0b0000000000010000:
                self.cFMSBtn.setStyleSheet("background-color: red")
            else:
                self.cFMSBtn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0000000000100000 == 0b0000000000100000:
                self.cFSSBtn.setStyleSheet("background-color: red")
            else:
                self.cFSSBtn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0000000001000000 == 0b0000000001000000:
                self.cFlowMeterBtn.setStyleSheet("background-color: red")
            else:
                self.cFlowMeterBtn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0000000010000000 == 0b0000000010000000:
                self.cFlowSwitchBtn.setStyleSheet("background-color: red")
            else:
                self.cFlowSwitchBtn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0000000100000000 == 0b0000000100000000:
                self.cTSBtn.setStyleSheet("background-color: red")
            else:
                self.cTSBtn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0000001000000000 == 0b0000001000000000:
                self.cLSBtn.setStyleSheet("background-color: red")
            else:
                self.cLSBtn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0000010000000000 == 0b0000010000000000:
                self.cLL2Btn.setStyleSheet("background-color: red")
            else:
                self.cLL2Btn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0000100000000000 == 0b0000100000000000:
                self.cLL1Btn.setStyleSheet("background-color: red")
            else:
                self.cLL1Btn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0001000000000000 == 0b0001000000000000:
                self.cLT2Btn.setStyleSheet("background-color: red")
            else:
                self.cLT2Btn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0010000000000000 == 0b0010000000000000:
                self.cLT1Btn.setStyleSheet("background-color: red")
            else:
                self.cLT1Btn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b0100000000000000 == 0b0100000000000000:
                self.cHT2Btn.setStyleSheet("background-color: red")
            else:
                self.cHT2Btn.setStyleSheet("background-color: lightgray")
            if int(data) & 0b1000000000000000 == 0b1000000000000000:
                self.cHT1Btn.setStyleSheet("background-color: red")
            else:
                self.cHT1Btn.setStyleSheet("background-color: lightgray")
        elif cmd == '157':
            self.flowRcvEdit.setText(data)
        elif cmd == '158':
            self.pidRcvEdit.setText(data)


    def disconnectChiller(self):
        self.laserConnect.setText('Connect')

    def defaultChiller(self):
        cmd = self.chillerCmd.toPlainText()
        sc = self.chillerSc.toPlainText()
        length = self.chillerLength.toPlainText()
        data = self.chillerData.toPlainText()
        self.chiller.send(cmd, sc, length, data)

    def status(self):
        cmd='?STATUS'
        data=''
        self.ser.send(cmd, data)

    def dsn(self):
        cmd='?DSN'
        data=''
        self.ser.send(cmd, data)

    def opmdReq(self):
        cmd='?OPMD'
        data=''
        self.ser.send(cmd, data)

    def limit(self):
        cmd='?IMAXUSR'
        data=''
        self.ser.send(cmd, data)
        sleep(2)
        cmd='?STATUS'
        self.ser.send(cmd, data)
        sleep(2)
        cmd='?OUTPUT'
        self.ser.send(cmd, data)

    def temp(self):
        cmd='?TOFW'
        data=''
        self.ser.send(cmd, data)
        sleep(2)
        cmd='?TMONRT'
        self.ser.send(cmd, data)
        sleep(2)
        cmd='?ENVC'
        self.ser.send(cmd, data)

    def pd(self):
        cmd='?PD'
        data=''
        self.ser.send(cmd, data)
        sleep(2)
        cmd='?PDPOW'
        self.ser.send(cmd, data)

    def enable(self):
        cmd = 'ENABLE='
        data = self.enableEdit.toPlainText()
        self.ser.send(cmd, data)

    def pilot(self):
        cmd = 'PILOT_EN='
        if self.pilotFlag:
            self.pilotFlag = False
            data='0'
            self.pilotBtn.setStyleSheet("background-color: lightgray")
        else:
            self.pilotFlag = True
            data='1'
            self.pilotBtn.setStyleSheet("background-color: green")
        self.ser.send(cmd, data)

    def opmd(self):
        cmd = 'OPMD='
        data = 'DGC'
        self.ser.send(cmd, data)

    def setMode(self):
        cmd = 'ISETMODE='
        data = 'P'
        self.ser.send(cmd, data)

    def output(self):
        cmd = 'OUTPUT='
        data = self.outputEdit.toPlainText()
        self.ser.send(cmd, data)   

    def clearMsg(self):
        self.recvmsg.clear()

    # def closeEvent(self, e):
        # self.lc.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())