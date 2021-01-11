from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
import func
import calc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(250, 0, 1400, 1080)

        self.initUI()

        self.L = 1
        self.N = 512
        self.d1 = self.L / self.N
        self.k = 2 * np.pi / float(self.wvl.toPlainText())
        self.delta_z = 10e+1
        self.I0 = 4*float(self.P0.toPlainText()) / (np.pi * float(self.D0.toPlainText())**2)
        self.w0 = (float(self.M_sqr.toPlainText()) * float(self.wvl.toPlainText())) / (np.pi * float(self.NA.toPlainText()))
        self.wd = self.w0 * (float(self.D0.toPlainText()) / float(self.D_core.toPlainText()))
        self.R0sw = 0.124 * np.power(self.k, 7 / 6) * float(self.Cn2.toPlainText()) * np.power(float(self.Z.toPlainText()), 11 / 6)  # Spherical-wave Rytov number
        self.r0sw = np.power((0.159 * np.power(self.k, 2) * float(self.Cn2.toPlainText()) * float(self.Z.toPlainText())), -3 / 5)  # Spherical-wave Fried Parameter[m]
        self.theta0 = 0.314 * self.r0sw / float(self.Z.toPlainText())  # Isoplanetic angle[rad]
        self.fG = np.power((0.102 * (self.k ** 2) * float(self.Cn2.toPlainText()) * float(self.v_wind.toPlainText())**2 * float(self.Z.toPlainText())), 3 / 5)  # Greenweed frequency[Hz]
        self.delta_t = float(self.D0.toPlainText()) / float(self.v_wind.toPlainText())  # decrease delta_t -> no wind effect
        self.move_pixel = int(float(self.v_wind.toPlainText()) * (1 / self.d1) * self.delta_t)
        self.n_iter = int(float(self.dwell_time.toPlainText()) / self.delta_t)
        self.q = self.Lamvert_Law(float(self.v.toPlainText()))
        self.nu = (3.912 / (float(self.v.toPlainText()) / 1000)) * np.power((550 / (float(self.wvl.toPlainText()) * np.power(10, 9))), self.q)  # Atmospheric extinction coefficient[km-1]
        self.T_atmos = np.exp(-(float(self.Z.toPlainText()) / 1000) * self.nu)  # Transmittance of the laser beam at the range
        self.alpha_a = 5e-6  # Absorbtion coefficient[1/m]
        self.alpha_s = 5e-5  # Absorbtion coefficient[1/m]
        self.alpha = self.alpha_a + self.alpha_s
        self.lambda2 = float(self.wvl.toPlainText()) * 1e+6  # wavelength[um]
        self.n0 = 1 + 2.602e-4
        self.mu = (self.n0 - 1) * self.alpha / (float(self.Cp.toPlainText()) * float(self.rho.toPlainText()) * float(self.T0.toPlainText()))
        self.N_d = (4 * np.sqrt(2) * float(self.P0.toPlainText()) / 1000 * self.k * (self.n0 - 1) * self.alpha_a * np.exp(-self.alpha_a * float(self.Z.toPlainText()))
                    * np.exp(-self.alpha_s * float(self.Z.toPlainText())) * float(self.Z.toPlainText())) / (float(self.Cp.toPlainText())
                    * float(self.rho.toPlainText()) * float(self.T0.toPlainText()) * float(self.D0.toPlainText()) * float(self.v_wind.toPlainText()))
        self.Dz = 2.44 * float(self.wvl.toPlainText()) * float(self.Z.toPlainText()) / (float(self.D0.toPlainText()) * self.n0)
        self.theta_diff = 1.22 * float(self.wvl.toPlainText()) / float(self.D0.toPlainText())
        self.theta_quality = (float(self.M_sqr.toPlainText()) - 1) * self.theta_diff
        self.theta_turb = 1.6 * float(self.wvl.toPlainText()) / (np.pi * self.r0sw)
        self.theta_jitter = 10e-6
        self.theta_bloom = 0
        self.theta_spread = np.sqrt(self.theta_diff ** 2 + self.theta_quality ** 2 + self.theta_turb ** 2 + self.theta_jitter ** 2 + self.theta_bloom ** 2)

        self.paramInit()

        self.expand = 0
        self.material = 0
        self.onMaterialCbChanged()
        self.step1Results = np.zeros((self.N, self.N, 3))
        self.step2Results = np.zeros((self.N, self.N, len(self.z)))
        self.step3Results = np.zeros((self.N, self.N, self.n_iter))
        self.step3Holes = np.zeros((self.N, self.N, self.n_iter))
        self.onStep1CbChanged()
        self.onStep2CbChanged()
        self.onStep3CbChanged()

    def initUI(self):
        self.setWindowTitle('효과도 분석 프로그램')

        # 클라이언트 설정 부분
        parambox = QVBoxLayout()

        gb = QGroupBox('Prameter')
        parambox.addWidget(gb)

        box = QVBoxLayout()

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Wavelength[m]')
        hbox.addWidget(label)
        self.wvl = QTextEdit()
        self.wvl.setText('1000e-9')
        self.wvl.setFixedHeight(27)
        self.wvl.setFixedWidth(75)
        self.wvl.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.wvl)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Propagation distance[m]')
        hbox.addWidget(label)
        self.Z = QTextEdit()
        self.Z.setText('5e+3')
        self.Z.setFixedHeight(27)
        self.Z.setFixedWidth(75)
        self.Z.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.Z)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Initial Power[kW]')
        hbox.addWidget(label)
        self.P0 = QTextEdit()
        self.P0.setText('4.72e+3')
        self.P0.setFixedHeight(27)
        self.P0.setFixedWidth(75)
        self.P0.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.P0)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Aperture diameter[m]')
        hbox.addWidget(label)
        self.D0 = QTextEdit()
        self.D0.setText('0.5')
        self.D0.setFixedHeight(27)
        self.D0.setFixedWidth(75)
        self.D0.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.D0)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Beam quality')
        hbox.addWidget(label)
        self.M_sqr = QTextEdit()
        self.M_sqr.setText('1.1')
        self.M_sqr.setFixedHeight(27)
        self.M_sqr.setFixedWidth(75)
        self.M_sqr.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.M_sqr)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('half of the Fiber[rad]')
        hbox.addWidget(label)
        self.NA = QTextEdit()
        self.NA.setText('0.035')
        self.NA.setFixedHeight(27)
        self.NA.setFixedWidth(75)
        self.NA.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.NA)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Diameter of the core[m]')
        hbox.addWidget(label)
        self.D_core = QTextEdit()
        self.D_core.setText('3e-6')
        self.D_core.setFixedHeight(27)
        self.D_core.setFixedWidth(75)
        self.D_core.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.D_core)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Refractive index structure[Cn^2]')
        hbox.addWidget(label)
        self.Cn2 = QTextEdit()
        self.Cn2.setText('1e-15')
        self.Cn2.setFixedHeight(27)
        self.Cn2.setFixedWidth(75)
        self.Cn2.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.Cn2)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Wind speed[m/s]')
        hbox.addWidget(label)
        self.v_wind = QTextEdit()
        self.v_wind.setText('5')
        self.v_wind.setFixedHeight(27)
        self.v_wind.setFixedWidth(75)
        self.v_wind.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.v_wind)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('dwell time[s]')
        hbox.addWidget(label)
        self.dwell_time = QTextEdit()
        self.dwell_time.setText('1')
        self.dwell_time.setFixedHeight(27)
        self.dwell_time.setFixedWidth(75)
        self.dwell_time.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.dwell_time)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Visibility[m]')
        hbox.addWidget(label)
        self.v = QTextEdit()
        self.v.setText('13000')
        self.v.setFixedHeight(27)
        self.v.setFixedWidth(75)
        self.v.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.v)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Density of the air[kg/m^3]')
        hbox.addWidget(label)
        self.rho = QTextEdit()
        self.rho.setText('1.293')
        self.rho.setFixedHeight(27)
        self.rho.setFixedWidth(75)
        self.rho.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.rho)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('heat capacity of air[J/kg/Kelvin]')
        hbox.addWidget(label)
        self.Cp = QTextEdit()
        self.Cp.setText('1.004')
        self.Cp.setFixedHeight(27)
        self.Cp.setFixedWidth(75)
        self.Cp.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.Cp)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Ambient temperature[Kelvin]')
        hbox.addWidget(label)
        self.T0 = QTextEdit()
        self.T0.setText('300')
        self.T0.setFixedHeight(27)
        self.T0.setFixedWidth(75)
        self.T0.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.T0)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        self.materialCb = QComboBox()
        self.materialCb.addItem('Aluminum')
        self.materialCb.addItem('Cooper')
        self.materialCb.addItem('Steel')
        self.materialCb.addItem('Magnesium')
        self.materialCb.addItem('Iron')
        self.materialCb.addItem('Titanium')
        self.materialCb.activated[str].connect(self.onMaterialCbChanged)
        hbox.addWidget(self.materialCb)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Target Thickness[mm]')
        hbox.addWidget(label)
        self.targetThickness = QTextEdit()
        self.targetThickness.setText('3')
        self.targetThickness.setFixedHeight(27)
        self.targetThickness.setFixedWidth(75)
        self.targetThickness.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.targetThickness)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Target Area[cm]')
        hbox.addWidget(label)
        self.targetArea = QTextEdit()
        self.targetArea.setText('1')
        self.targetArea.setFixedHeight(27)
        self.targetArea.setFixedWidth(75)
        self.targetArea.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.targetArea)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Temperature[C]')
        hbox.addWidget(label)
        self.temperature = QTextEdit()
        self.temperature.setText('25')
        self.temperature.setFixedHeight(27)
        self.temperature.setFixedWidth(75)
        self.temperature.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.temperature)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('fiberDiameter[cm]')
        hbox.addWidget(label)
        self.fiberDiameter = QTextEdit()
        self.fiberDiameter.setText('0.015')
        self.fiberDiameter.setFixedHeight(27)
        self.fiberDiameter.setFixedWidth(75)
        self.fiberDiameter.setAlignment(Qt.AlignRight)
        hbox.addWidget(self.fiberDiameter)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        label = QLabel('Parameter Setting')
        hbox.addWidget(label)
        self.settingBtn = QPushButton('Set')
        self.settingBtn.setAutoDefault(True)
        self.settingBtn.setFixedWidth(75)
        self.settingBtn.clicked.connect(self.setting)
        hbox.addWidget(self.settingBtn)

        gb.setLayout(box)

        # Calculation
        calcbox = QHBoxLayout()

        gb = QGroupBox('Calculation')
        gb.setFixedWidth(1024)
        gb.setFixedHeight(1024)
        calcbox.addWidget(gb)

        box = QVBoxLayout()
        hbox = QHBoxLayout()
        box.addLayout(hbox)

        self.step1Fig = plt.Figure()
        self.step1Canvas = FigureCanvas(self.step1Fig)
        hbox.addWidget(self.step1Canvas)
        self.step2Fig = plt.Figure()
        self.step2Canvas = FigureCanvas(self.step2Fig)
        self.step2Canvas.resize(500, 500)
        hbox.addWidget(self.step2Canvas)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        self.step1Btn = QPushButton('Step1')
        self.step1Btn.setAutoDefault(True)
        self.step1Btn.clicked.connect(self.Step1)
        self.step1Btn.setEnabled(False)
        hbox.addWidget(self.step1Btn)
        self.step1BwBtn = QPushButton('<<')
        self.step1BwBtn.setAutoDefault(True)
        self.step1BwBtn.clicked.connect(self.Step1Bw)
        hbox.addWidget(self.step1BwBtn)
        self.step1Cb = QComboBox()
        self.step1Cb.addItem('Source')
        self.step1Cb.addItem('Target anal')
        self.step1Cb.addItem('Target')
        self.step1Cb.activated[str].connect(self.onStep1CbChanged)
        hbox.addWidget(self.step1Cb)
        self.step1FwBtn = QPushButton('>>')
        self.step1FwBtn.setAutoDefault(True)
        self.step1FwBtn.clicked.connect(self.Step1Fw)
        hbox.addWidget(self.step1FwBtn)
        self.step2Btn = QPushButton('Step2')
        self.step2Btn.setAutoDefault(True)
        self.step2Btn.clicked.connect(self.Step2)
        self.step2Btn.setEnabled(False)
        hbox.addWidget(self.step2Btn)
        self.step2BwBtn = QPushButton('<<')
        self.step2BwBtn.setAutoDefault(True)
        self.step2BwBtn.clicked.connect(self.Step2Bw)
        hbox.addWidget(self.step2BwBtn)
        self.step2Cb = QComboBox()
        self.step2Cb.addItem('0m')
        for i in range(1, 51):
            self.step2Cb.addItem('{}00m'.format(i))
        self.step2Cb.activated[str].connect(self.onStep2CbChanged)
        hbox.addWidget(self.step2Cb)
        self.step2FwBtn = QPushButton('>>')
        self.step2FwBtn.setAutoDefault(True)
        self.step2FwBtn.clicked.connect(self.Step2Fw)
        hbox.addWidget(self.step2FwBtn)

        # Step3
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)

        self.step3Fig = plt.Figure()
        self.step3Canvas = FigureCanvas(self.step3Fig)
        hbox.addWidget(self.step3Canvas)
        self.step3HoleFig = plt.Figure()
        self.step3HoleCanvas = FigureCanvas(self.step3HoleFig)
        hbox.addWidget(self.step3HoleCanvas)

        hbox = QHBoxLayout()
        vbox.addLayout(hbox)
        self.step3Btn = QPushButton('Step3')
        self.step3Btn.setAutoDefault(True)
        self.step3Btn.setFixedWidth(120)
        self.step3Btn.clicked.connect(self.Step3)
        self.step3Btn.setEnabled(False)
        hbox.addWidget(self.step3Btn)
        self.step3BwBtn = QPushButton('<<')
        self.step3BwBtn.setAutoDefault(True)
        self.step3BwBtn.setFixedWidth(120)
        self.step3BwBtn.clicked.connect(self.Step3Bw)
        hbox.addWidget(self.step3BwBtn)
        self.step3Cb = QComboBox()
        self.step3Cb.activated[str].connect(self.onStep3CbChanged)
        hbox.addWidget(self.step3Cb)
        self.step3FwBtn = QPushButton('>>')
        self.step3FwBtn.setAutoDefault(True)
        self.step3FwBtn.setFixedWidth(120)
        self.step3FwBtn.clicked.connect(self.Step3Fw)
        hbox.addWidget(self.step3FwBtn)
        self.step3MinusBtn = QPushButton('-')
        self.step3MinusBtn.setAutoDefault(True)
        self.step3MinusBtn.setFixedWidth(120)
        self.step3MinusBtn.clicked.connect(self.Step3Minus)
        hbox.addWidget(self.step3MinusBtn)
        self.step3PlusBtn = QPushButton('+')
        self.step3PlusBtn.setAutoDefault(True)
        self.step3PlusBtn.setFixedWidth(120)
        self.step3PlusBtn.clicked.connect(self.Step3Plus)
        hbox.addWidget(self.step3PlusBtn)
        self.saveBtn = QPushButton('Save')
        self.saveBtn.setAutoDefault(True)
        self.saveBtn.setFixedWidth(120)
        self.saveBtn.clicked.connect(self.Save)
        hbox.addWidget(self.saveBtn)
        box.addLayout(vbox)

        gb.setLayout(box)

        # 전체 배치
        vbox = QHBoxLayout()
        vbox.addLayout(parambox)
        vbox.addLayout(calcbox)
        self.setLayout(vbox)

        self.show()

    def paramInit(self):
        self.z = []
        for i in range(51):
            if i == 0:
                self.z.append(1e-20)
            else:
                self.z.append(100*i)

        # Coordinate at source
        self.x1 = []
        for i in range(512):
            self.x1.append(-self.N / 2 * self.d1 + (self.N * self.d1) / 512 * i)
        self.y1 = self.x1
        X1 = []
        for i in range(512):
            X1.append(self.x1)
        X1 = np.array(X1)
        Y1 = np.transpose(X1)
        self.r = np.sqrt(np.power(X1, 2) + np.power(Y1, 2))

        self.u1 = np.zeros((self.N, self.N, len(self.z)), dtype='d')
        self.l2 = np.zeros((self.N, self.N, len(self.z)), dtype='d')

        self.P = np.zeros((self.N, self.N), dtype=complex)
        self.P = func.propagator(float(self.wvl.toPlainText()), self.N, self.N, max(self.x1[:]), self.d1, self.delta_z / 2, self.n0)

    def Lamvert_Law(self, v):
        if v < 6000:
            q = 0.585 * np.power(self.Z / 1000, 1 / 3)
        elif v >= 6000 and v < 50000:
            q = 1.3
        else:
            q = 1.6
        return q

    def onMaterialCbChanged(self):
        index = self.materialCb.currentIndex()
        if index == 0:
            # Aluminum
            targetDensity = 2.7
            specificHeat = 0.91
            meltingPoint = 660
            vapoPoint = 2467
            meltingLatentHeat = 321
            vapoLatentHeat = 10500
        elif index == 1:
            targetDensity = 8.96
            specificHeat = 0.38
            meltingPoint = 1100
            vapoPoint = 2600
            meltingLatentHeat = 210
            vapoLatentHeat = 4700
        elif index == 2:
            targetDensity = 7.87
            specificHeat = 0.452
            meltingPoint = 1425
            vapoPoint = 2971
            meltingLatentHeat = 250
            vapoLatentHeat = 6200
        elif index == 3:
            targetDensity = 1.74
            specificHeat = 1
            meltingPoint = 650
            vapoPoint = 1100
            meltingLatentHeat = 370
            vapoLatentHeat = 5300
        elif index == 4:
            targetDensity = 7.9
            specificHeat = 0.46
            meltingPoint = 1500
            vapoPoint = 3000
            meltingLatentHeat = 250
            vapoLatentHeat = 6300
        elif index == 5:
            targetDensity = 4.5
            specificHeat = 0.52
            meltingPoint = 1700
            vapoPoint = 3700
            meltingLatentHeat = 320
            vapoLatentHeat = 8800

        self.material = self.onMaterialCalc(float(self.targetThickness.toPlainText()),
                                            float(self.targetArea.toPlainText()), targetDensity, specificHeat,
                                            meltingPoint, vapoPoint, meltingLatentHeat, vapoLatentHeat,
                                            float(self.temperature.toPlainText()), float(self.dwell_time.toPlainText()),
                                            float(self.fiberDiameter.toPlainText()))

    def onMaterialCalc(self, targetThickness, targetArea, targetDensity, specificHeat, meltingPoint, vapoPoint, meltingLatentHeat, vapoLatentHeat, temperature, dwell_time, fiberDiameter):
        targetWeight = targetDensity*(targetArea*targetThickness*0.1)
        q1 = targetWeight * specificHeat * (meltingPoint - temperature)
        q2 = targetWeight * meltingLatentHeat
        q3 = targetWeight * specificHeat * (vapoPoint - temperature)
        q4 = targetWeight * vapoLatentHeat

        q_total = q1 + q2 + q3 + q4
        powerCalc = q_total / (dwell_time * (fiberDiameter ** 2) * np.pi)
        return powerCalc

    def setting(self):
        self.step3Cb.clear()
        self.k = 2 * np.pi / float(self.wvl.toPlainText())
        self.I0 = 4 * float(self.P0.toPlainText()) / (np.pi * float(self.D0.toPlainText()) ** 2)
        self.w0 = (float(self.M_sqr.toPlainText()) * float(self.wvl.toPlainText())) / (
                    np.pi * float(self.NA.toPlainText()))
        self.wd = self.w0 * (float(self.D0.toPlainText()) / float(self.D_core.toPlainText()))
        self.R0sw = 0.124 * np.power(self.k, 7 / 6) * float(self.Cn2.toPlainText()) * np.power(
            float(self.Z.toPlainText()), 11 / 6)  # Spherical-wave Rytov number
        self.r0sw = np.power(
            (0.159 * np.power(self.k, 2) * float(self.Cn2.toPlainText()) * float(self.Z.toPlainText())),
            -3 / 5)  # Spherical-wave Fried Parameter[m]
        self.theta0 = 0.314 * self.r0sw / float(self.Z.toPlainText())  # Isoplanetic angle[rad]
        self.fG = np.power((0.102 * (self.k ** 2) * float(self.Cn2.toPlainText()) * float(
            self.v_wind.toPlainText()) ** 2 * float(self.Z.toPlainText())), 3 / 5)  # Greenweed frequency[Hz]
        self.delta_t = float(self.D0.toPlainText()) / float(
            self.v_wind.toPlainText())  # decrease delta_t -> no wind effect
        self.move_pixel = int(float(self.v_wind.toPlainText()) * (1 / self.d1) * self.delta_t)
        self.n_iter = int(float(self.dwell_time.toPlainText()) / self.delta_t)
        self.q = self.Lamvert_Law(float(self.v.toPlainText()))
        self.nu = (3.912 / (float(self.v.toPlainText()) / 1000)) * np.power(
            (550 / (float(self.wvl.toPlainText()) * np.power(10, 9))),
            self.q)  # Atmospheric extinction coefficient[km-1]
        self.T_atmos = np.exp(
            -(float(self.Z.toPlainText()) / 1000) * self.nu)  # Transmittance of the laser beam at the range
        self.lambda2 = float(self.wvl.toPlainText()) * 1e+6  # wavelength[um]
        self.mu = (self.n0 - 1) * self.alpha / (
                    float(self.Cp.toPlainText()) * float(self.rho.toPlainText()) * float(self.T0.toPlainText()))
        self.N_d = (4 * np.sqrt(2) * float(self.P0.toPlainText()) / 1000 * self.k * (
                    self.n0 - 1) * self.alpha_a * np.exp(-self.alpha_a * float(self.Z.toPlainText())) * np.exp(
            -self.alpha_s * float(self.Z.toPlainText())) * float(self.Z.toPlainText())) / (
                               float(self.Cp.toPlainText()) * float(self.rho.toPlainText()) * float(
                           self.T0.toPlainText()) * float(self.D0.toPlainText()) * float(self.v_wind.toPlainText()))
        self.Dz = 2.44 * float(self.wvl.toPlainText()) * float(self.Z.toPlainText()) / (
                    float(self.D0.toPlainText()) * self.n0)
        self.theta_diff = 1.22 * float(self.wvl.toPlainText()) / float(self.D0.toPlainText())
        self.theta_quality = (float(self.M_sqr.toPlainText()) - 1) * self.theta_diff
        self.theta_turb = 1.6 * float(self.wvl.toPlainText()) / (np.pi * self.r0sw)
        self.theta_spread = np.sqrt(
            self.theta_diff ** 2 + self.theta_quality ** 2 + self.theta_turb ** 2 + self.theta_jitter ** 2 + self.theta_bloom ** 2)
        self.paramInit()
        for i in range(self.n_iter):
            self.step3Cb.addItem('Ither {}'.format(i))
        self.expand = 0
        self.onMaterialCbChanged()
        self.step1Results = np.zeros((self.N, self.N, 3))
        self.step2Results = np.zeros((self.N, self.N, len(self.z)))
        self.step3Results = np.zeros((self.N, self.N, self.n_iter))
        self.step3Holes = np.zeros((self.N, self.N, self.n_iter))
        self.onStep1CbChanged()
        self.onStep2CbChanged()
        self.onStep3CbChanged()
        self.step1Btn.setEnabled(True)
        self.step2Btn.setEnabled(False)
        self.step3Btn.setEnabled(False)

    def Step1(self):
        self.step1Btn.setEnabled(False)
        self.step1 = calc.Step1Thread(self.N, self.wd, self.z, float(self.Z.toPlainText()), self.theta_diff, self.theta_spread,
                                 self.u1, self.r, self.x1, self.y1, self.l2, float(self.P0.toPlainText()), self.k,
                                 float(self.D0.toPlainText()), self.P, float(self.wvl.toPlainText()), self.delta_z,
                                 self.d1, self.n0)
        self.step1.result.connect(self.Step1Result)
        self.step1.start()

    def Step1Result(self, img):
        self.step1Results = img
        self.onStep1CbChanged()
        print('step1 End')
        self.step1Btn.setEnabled(True)
        self.step2Btn.setEnabled(True)

    def onStep1CbChanged(self):
        self.step1Fig.clear()
        index = self.step1Cb.currentIndex()
        ax = self.step1Fig.add_subplot(111)
        ax.set_title("Analytic vs. FFT method")
        ax.imshow(self.step1Results[:, :, index])
        self.step1Canvas.draw()

    def Step1Bw(self):
        index = self.step1Cb.currentIndex()
        if index <= 0:
            self.step1Cb.setCurrentIndex(0)
            self.onStep1CbChanged()
        else:
            self.step1Cb.setCurrentIndex(index-1)
            self.onStep1CbChanged()

    def Step1Fw(self):
        index = self.step1Cb.currentIndex()
        if index >= 2:
            self.step1Cb.setCurrentIndex(2)
            self.onStep1CbChanged()
        else:
            self.step1Cb.setCurrentIndex(index+1)
            self.onStep1CbChanged()

    def Step2(self):
        self.step1Btn.setEnabled(False)
        self.step2Btn.setEnabled(False)
        self.step2 = calc.Step2Thread(self.N, self.z, self.l2, self.move_pixel, self.mu, float(self.v_wind.toPlainText()),
                                 self.u1, self.k, float(self.Z.toPlainText()), self.r, float(self.D0.toPlainText()),
                                 self.P, float(self.wvl.toPlainText()), self.x1, self.delta_z, self.d1, self.n0,
                                 self.r0sw)
        self.step2.result.connect(self.Step2Result)
        self.step2.start()

    def Step2Result(self, img):
        self.step2Results = img
        self.onStep2CbChanged()
        print('step2 End')
        self.step2Btn.setEnabled(True)
        self.step3Btn.setEnabled(True)

    def onStep2CbChanged(self):
        self.step2Fig.clear()
        index = self.step2Cb.currentIndex()
        ax = self.step2Fig.add_subplot(111)
        ax.set_title("Intensity Map @ {}m Target".format(self.Z.toPlainText()))
        ax.imshow(self.step2Results[:,:,index])
        self.step2Canvas.draw()

    def Step2Bw(self):
        index = self.step2Cb.currentIndex()
        if index <= 0:
            self.step2Cb.setCurrentIndex(0)
            self.onStep2CbChanged()
        else:
            self.step2Cb.setCurrentIndex(index-1)
            self.onStep2CbChanged()

    def Step2Fw(self):
        index = self.step2Cb.currentIndex()
        if index >= 50:
            self.step2Cb.setCurrentIndex(50)
            self.onStep2CbChanged()
        else:
            self.step2Cb.setCurrentIndex(index+1)
            self.onStep2CbChanged()

    def Step3(self):
        self.step1Btn.setEnabled(False)
        self.step2Btn.setEnabled(False)
        self.step3Btn.setEnabled(False)
        self.step3 = calc.Step3Thread(self.material, float(self.dwell_time.toPlainText()), self.N,
                                 self.z, self.n_iter, self.l2, self.move_pixel, self.mu,
                                 float(self.v_wind.toPlainText()), self.u1, self.k, float(self.Z.toPlainText()), self.r,
                                 float(self.D0.toPlainText()), self.P, float(self.P0.toPlainText()), float(self.wvl.toPlainText()), self.x1, self.y1,
                                 self.delta_z, self.d1, self.n0, self.r0sw, self.delta_t)
        self.step3.result.connect(self.Step3Result)
        self.step3.start()

    def Step3Result(self, img, img_hole):
        self.step3Results = img
        self.step3Holes = img_hole
        self.onStep3CbChanged()
        print('step3 End')
        self.step3Btn.setEnabled(True)

    def onStep3CbChanged(self):
        self.step3Fig.clear()
        self.step3HoleFig.clear()
        index = self.step3Cb.currentIndex()
        ax = self.step3Fig.add_subplot(111)
        ax.set_title("Target Intensity Map")
        ax2 = self.step3HoleFig.add_subplot(111)
        ax2.set_title("Hole Detection Map")
        if self.expand <= 0 or self.expand >= 26:
            ax.imshow(self.step3Results[:, :, index])
            ax2.imshow(self.step3Holes[:, :, index])
        else:
            ax.imshow(self.step3Results[10*self.expand:-10*self.expand, 10*self.expand:-10*self.expand, index])
            ax2.imshow(self.step3Holes[10*self.expand:-10*self.expand, 10*self.expand:-10*self.expand, index])
        self.step3Canvas.draw()
        self.step3HoleCanvas.draw()

    def Step3Bw(self):
        index = self.step3Cb.currentIndex()
        if index <= 0:
            self.step3Cb.setCurrentIndex(0)
            self.onStep3CbChanged()
        else:
            self.step3Cb.setCurrentIndex(index - 1)
            self.onStep3CbChanged()

    def Step3Fw(self):
        index = self.step3Cb.currentIndex()
        if index >= self.n_iter -1:
            self.step3Cb.setCurrentIndex(self.n_iter -1)
            self.onStep3CbChanged()
        else:
            self.step3Cb.setCurrentIndex(index + 1)
            self.onStep3CbChanged()

    def Step3Minus(self):
        self.expand -= 1
        if self.expand <= 0:
            self.expand = 0
        self.onStep3CbChanged()

    def Step3Plus(self):
        self.expand += 1
        if self.expand >= 25:
            self.expand = 25
        self.onStep3CbChanged()

    def Save(self):
        screen = QApplication.primaryScreen().grabWindow(w.winId())
        screen.save('Output.jpg', 'jpg')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())