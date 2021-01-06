from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
import func
import matplotlib.pyplot as plt

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.L = 1
        self.N = 512
        self.d1 = self.L / self.N
        self.k = 2 * np.pi / self.wvl
        self.delta_z = 10e+1
        self.I0 = 4*self.P0 / (np.pi * self.D0**2)
        self.w0 = (self.M_sqr * self.wvl) / (np.pi * self.NA)
        self.wd = self.w0 * (self.D0 / self.D_core)
        self.R0sw = 0.124 * np.power(self.k, 7 / 6) * self.Cn2 * np.power(self.Z, 11 / 6)  # Spherical-wave Rytov number
        self.r0sw = np.power((0.159 * np.power(self.k, 2) * self.Cn2 * self.Z), -3 / 5)  # Spherical-wave Fried Parameter[m]
        self.theta0 = 0.314 * self.r0sw / self.Z  # Isoplanetic angle[rad]
        self.fG = np.power((0.102 * (self.k ** 2) * self.Cn2 * np.power(self.v_wind, 2) * self.Z), 3 / 5)  # Greenweed frequency[Hz]
        self.delta_t = self.D0 / self.v_wind  # decrease delta_t -> no wind effect
        self.move_pixel = int(self.v_wind * (1 / self.d1) * self.delta_t)
        self.n_iter = int(self.dwell_time / self.delta_t)
        self.q = self.Lamvert_Law(self.v)
        self.nu = (3.912 / (self.v / 1000)) * np.power((550 / (self.wvl * np.power(10, 9))), self.q)  # Atmospheric extinction coefficient[km-1]
        self.T_atmos = np.exp(-(self.Z / 1000) * self.nu)  # Transmittance of the laser beam at the range
        self.alpha_a = 5e-6  # Absorbtion coefficient[1/m]
        self.alpha_s = 5e-5  # Absorbtion coefficient[1/m]
        self.alpha = self.alpha_a + self.alpha_s
        self.lambda2 = self.wvl * 1e+6  # wavelength[um]
        self.n0 = 1 + 2.602e-4
        self.mu = (self.n0 - 1) * self.alpha / (self.Cp * self.rho * self.T0)
        self.N_d = (4 * np.sqrt(2) * self.P0 / 1000 * self.k * (self.n0 - 1) * self.alpha_a * np.exp(-self.alpha_a * self.Z) * np.exp(-self.alpha_s * self.Z) * self.Z) / (self.Cp * self.rho * self.T0 * self.D0 * self.v_wind)
        self.Dz = 2.44 * self.wvl * self.Z / (self.D0 * self.n0)
        self.paramInit()

    def __del__(self):
        self.c.stop()

    def initUI(self):
        self.setWindowTitle('효과도 분석 프로그램')

        # 클라이언트 설정 부분
        parambox = QVBoxLayout()

        gb = QGroupBox('Prameter')
        parambox.addWidget(gb)

        box = QVBoxLayout()

        label = QLabel('Wavelength[m]')
        box.addWidget(label)
        label = QLabel('Propagation distance[m]')
        box.addWidget(label)
        label = QLabel('Initial Power[kW]')
        box.addWidget(label)
        label = QLabel('Aperture diameter[m]')
        box.addWidget(label)
        label = QLabel('Beam quality')
        box.addWidget(label)
        label = QLabel('half of the Fiber[rad]')
        box.addWidget(label)
        label = QLabel('Diameter of the core[m]')
        box.addWidget(label)
        label = QLabel('Refractive index structure[Cn^2]')
        box.addWidget(label)
        label = QLabel('Wind speed[m/s]')
        box.addWidget(label)
        label = QLabel('dwell time[s]')
        box.addWidget(label)
        label = QLabel('Visibility[m]')
        box.addWidget(label)
        label = QLabel('Density of the air[kg/m^3]')
        box.addWidget(label)
        label = QLabel('heat capacity of air[J/kg/Kelvin]')
        box.addWidget(label)
        label = QLabel('Ambient temperature[Kelvin]')
        box.addWidget(label)

        gb.setLayout(box)

        # 값 설정
        editbox = QVBoxLayout()

        gb = QGroupBox(' ')
        editbox.addWidget(gb)

        box = QVBoxLayout()

        self.wvl = QTextEdit()
        self.wvl.setText('1000e-9')
        self.wvl.setFixedHeight(27)
        box.addWidget(self.wvl)
        self.Z = QTextEdit()
        self.Z.setText('5e+3')
        self.Z.setFixedHeight(27)
        box.addWidget(self.Z)
        self.P0 = QTextEdit()
        self.P0.setText('4.72e+3')
        self.P0.setFixedHeight(27)
        box.addWidget(self.P0)
        self.D0 = QTextEdit()
        self.D0.setText('0.5')
        self.D0.setFixedHeight(27)
        box.addWidget(self.D0)
        self.M_sqr = QTextEdit()
        self.M_sqr.setText('1.1')
        self.M_sqr.setFixedHeight(27)
        box.addWidget(self.M_sqr)
        self.NA = QTextEdit()
        self.NA.setText('0.035')
        self.NA.setFixedHeight(27)
        box.addWidget(self.NA)
        self.D_core = QTextEdit()
        self.D_core.setText('3e-6')
        self.D_core.setFixedHeight(27)
        box.addWidget(self.D_core)
        self.Cn2 = QTextEdit()
        self.Cn2.setText('1e-15')
        self.Cn2.setFixedHeight(27)
        box.addWidget(self.Cn2)
        self.v_wind = QTextEdit()
        self.v_wind.setText('5')
        self.v_wind.setFixedHeight(27)
        box.addWidget(self.v_wind)
        self.dwell_time = QTextEdit()
        self.dwell_time.setText('1')
        self.dwell_time.setFixedHeight(27)
        box.addWidget(self.dwell_time)
        self.v = QTextEdit()
        self.v.setText('13000')
        self.v.setFixedHeight(27)
        box.addWidget(self.v)
        self.rho = QTextEdit()
        self.rho.setText('1.293')
        self.rho.setFixedHeight(27)
        box.addWidget(self.rho)
        self.Cp = QTextEdit()
        self.Cp.setText('1.004')
        self.Cp.setFixedHeight(27)
        box.addWidget(self.Cp)
        self.T0 = QTextEdit()
        self.T0.setText('300')
        self.T0.setFixedHeight(27)
        box.addWidget(self.T0)

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

        # LD1 설정
        ld1box = QHBoxLayout()
        box.addLayout(ld1box)

        self.ld1SetBtn = QPushButton('LD 1')
        self.ld1SetBtn.setAutoDefault(True)
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

        self.clearBtn = QPushButton('채팅창 지움')

        hbox.addWidget(self.sendBtn)
        hbox.addWidget(self.clearBtn)
        gb.setLayout(box)

        # 전체 배치
        vbox = QHBoxLayout()
        vbox.addLayout(parambox)
        vbox.addLayout(editbox)
        vbox.addLayout(bitbox)
        vbox.addLayout(infobox)
        self.setLayout(vbox)

        self.show()

    def paramInit(self):
        self.z = []
        for i in range(51):
            if i == 0:
                self.z.append(1e-20)
            else:
                self.z.append(100*i)

    def Lamvert_Law(self, v):
        if v < 6000:
            q = 0.585 * np.power(self.Z / 1000, 1 / 3)
        elif v >= 6000 and v < 50000:
            q = 1.3
        else:
            q = 1.6
        return q

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())