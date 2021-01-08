from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
import func
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class CWidget(QWidget):
    def __init__(self):
        super().__init__()

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
        self.N_d = (4 * np.sqrt(2) * float(self.P0.toPlainText()) / 1000 * self.k * (self.n0 - 1) * self.alpha_a * np.exp(-self.alpha_a * float(self.Z.toPlainText())) \
                    * np.exp(-self.alpha_s * float(self.Z.toPlainText())) * float(self.Z.toPlainText())) / (float(self.Cp.toPlainText())\
                    * float(self.rho.toPlainText()) * float(self.T0.toPlainText()) * float(self.D0.toPlainText()) * float(self.v_wind.toPlainText()))
        self.Dz = 2.44 * float(self.wvl.toPlainText()) * float(self.Z.toPlainText()) / (float(self.D0.toPlainText()) * self.n0)
        self.theta_diff = 1.22 * float(self.wvl.toPlainText()) / float(self.D0.toPlainText())
        self.theta_quality = (float(self.M_sqr.toPlainText()) - 1) * self.theta_diff
        self.theta_turb = 1.6 * float(self.wvl.toPlainText()) / (np.pi * self.r0sw)
        self.theta_jitter = 10e-6
        self.theta_bloom = 0
        self.theta_spread = np.sqrt(self.theta_diff ** 2 + self.theta_quality ** 2 + self.theta_turb ** 2 + self.theta_jitter ** 2 + self.theta_bloom ** 2)

        self.paramInit()

        # self.Step1()

    # def __del__(self):
    #     self.c.stop()

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
        self.wvl.setAlignment(Qt.AlignRight)
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

        # Step1
        setp1box = QHBoxLayout()

        gb = QGroupBox('Step1')
        setp1box.addWidget(gb)

        box = QVBoxLayout()

        self.step1Fig = plt.Figure()
        self.step1Canvas = FigureCanvas(self.step1Fig)
        box.addWidget(self.step1Canvas)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        self.step1Btn = QPushButton('Step1')
        self.step1Btn.setAutoDefault(True)
        self.step1Btn.clicked.connect(self.Step1)
        hbox.addWidget(self.step1Btn)
        self.step1Cb = QComboBox()
        self.step1Cb.addItem('Source')
        self.step1Cb.addItem('Target anal')
        self.step1Cb.addItem('Target')
        self.step1Cb.activated[str].connect(self.onStep1CbChanged)
        hbox.addWidget(self.step1Cb)
        gb.setLayout(box)

        # Step2
        setp2box = QHBoxLayout()

        gb = QGroupBox('Step2')
        setp2box.addWidget(gb)

        box = QVBoxLayout()

        self.step2Fig = plt.Figure()
        self.step2Canvas = FigureCanvas(self.step2Fig)
        self.step2Canvas.resize(500, 500)
        box.addWidget(self.step2Canvas)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        self.step2Btn = QPushButton('Step2')
        self.step2Btn.setAutoDefault(True)
        self.step2Btn.clicked.connect(self.Step2)
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
        gb.setLayout(box)

        # Step3
        setp3box = QHBoxLayout()

        gb = QGroupBox('Step3')
        gb.setFixedWidth(1000)
        setp3box.addWidget(gb)

        box = QVBoxLayout()
        hbox = QHBoxLayout()
        box.addLayout(hbox)

        self.step3Fig = plt.Figure()
        self.step3Canvas = FigureCanvas(self.step3Fig)
        hbox.addWidget(self.step3Canvas)
        self.step3HoleFig = plt.Figure()
        self.step3HoleCanvas = FigureCanvas(self.step3HoleFig)
        hbox.addWidget(self.step3HoleCanvas)

        hbox = QHBoxLayout()
        box.addLayout(hbox)
        self.step3Btn = QPushButton('Step3')
        self.step3Btn.setAutoDefault(True)
        self.step3Btn.clicked.connect(self.Step3)
        hbox.addWidget(self.step3Btn)
        self.step3BwBtn = QPushButton('<<')
        self.step3BwBtn.setAutoDefault(True)
        self.step3BwBtn.clicked.connect(self.Step3Bw)
        hbox.addWidget(self.step3BwBtn)
        self.step3Cb = QComboBox()
        self.step3Cb.activated[str].connect(self.onStep3CbChanged)
        hbox.addWidget(self.step3Cb)
        self.step3FwBtn = QPushButton('>>')
        self.step3FwBtn.setAutoDefault(True)
        self.step3FwBtn.clicked.connect(self.Step3Fw)
        hbox.addWidget(self.step3FwBtn)
        gb.setLayout(box)

        # 전체 배치
        vbox = QHBoxLayout()
        vbox.addLayout(parambox)
        vbox.addLayout(editbox)
        vbox.addLayout(setp1box)
        vbox.addLayout(setp2box)
        vbox.addLayout(setp3box)
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

    def Step1(self):
        # beam waist size vs distance
        wz = []
        wz_spread = []
        for _ in range(51):
            wz.append(0)
            wz_spread.append(0)
        for i in range(51):
            wz[i] = np.sqrt((self.wd * (1 - self.z[i] / float(self.Z.toPlainText()))) ** 2 + self.theta_diff ** 2 * self.z[i] ** 2)
            wz_spread[i] = np.sqrt((self.wd * (1 - self.z[i] / float(self.Z.toPlainText()))) ** 2 + self.theta_spread ** 2 * self.z[i] ** 2)

        for i in range(51):
            self.u1[:, :, i] = (self.wd / wz[i]) * np.exp(-np.power(self.r, 2) / np.power(wz[i], 2))
            l = np.abs(np.power(self.u1[:, :, i], 2))
            # Nomalization
            A0 = np.trapz(np.trapz(l, self.x1, axis=1), self.y1)
            self.l2[:, :, i] = l * (1 / A0) * float(self.P0.toPlainText())

        self.l2_source = self.l2[:, :, 0]
        self.l2_target_anal = self.l2[:, :, 50]
        Uin = self.u1[:, :, 0] * np.exp(complex("0+j") * self.k / (2 * float(self.Z.toPlainText())) * self.r ** 2)\
              * func.make_nanmask(self.r / (float(self.D0.toPlainText()) / 2.67), 1)
        Uout = Uin

        for i in range(1, len(self.z) - 1):
            Uout = func.fft_BPM(Uout, self.P, float(self.wvl.toPlainText()), max(self.x1[:]), max(self.x1[:]), self.delta_z / 2, self.d1, self.delta_z / 2, self.n0)
            Uout = func.fft_BPM(Uout, self.P, float(self.wvl.toPlainText()), max(self.x1[:]), max(self.x1[:]), self.delta_z / 2, self.d1, self.delta_z / 2, self.n0)

        self.l2_target2 = abs(np.power(Uout, 2))
        A0 = np.trapz(np.trapz(self.l2_target2, self.x1, axis=1), self.y1)
        self.l2_target2 = self.l2_target2 * (1 / A0) * float(self.P0.toPlainText())
        self.onStep1CbChanged('Source')
        print('step1 End')

    def onStep1CbChanged(self, text):
        if text == 'Source':
            self.step1Fig.clear()
            ax = self.step1Fig.add_subplot(111)
            ax.imshow(self.l2_source)
            self.step1Canvas.draw()
        elif text == 'Target anal':
            self.step1Fig.clear()
            ax = self.step1Fig.add_subplot(111)
            ax.imshow(self.l2_target_anal)
            self.step1Canvas.draw()
        elif text == 'Target':
            self.step1Fig.clear()
            ax = self.step1Fig.add_subplot(111)
            ax.imshow(self.l2_target2)
            self.step1Canvas.draw()

    def Step2(self):
        # With Thermal Blooming & Atmosphere
        # Thermal blooming
        n_temp = np.zeros((self.N, self.N), dtype='d')
        n_step = 51
        l2_new = np.ndarray((512, 512, 51))
        delta_n = np.ndarray((512, 512, 51))
        for i in range(len(self.z)):
            # print(l2[:,:,i])
            l2_new[:, :, i] = np.roll(self.l2[:, :, i], np.int(np.round(self.move_pixel / n_step) * i))
            n_temp = -self.mu / float(self.v_wind.toPlainText()) * l2_new[:, :, i]
            delta_n[:, :, i] = n_temp

        # Input Phase -> Uin = U * lens_aperture * phase_TB * phase_turb
        Uin = self.u1[:, :, 0] * np.exp(complex("0+j") * self.k / (2 * float(self.Z.toPlainText())) * self.r ** 2) \
              * func.make_nanmask(self.r / (float(self.D0.toPlainText()) / 2.67), 1)
        Uout_turb = Uin

        phz_turbs = np.zeros((self.N, self.N, len(self.z)))
        self.Uout_turbs = np.zeros((self.N, self.N, len(self.z)))
        img = np.abs(np.power(Uout_turb, 2))
        img = np.uint8(img * 255 / np.max(img))
        self.Uout_turbs[:, :, 0] = img
        for i in range(1, len(self.z)):
            Uout_turb = func.fft_BPM(Uout_turb, self.P, float(self.wvl.toPlainText()), max(self.x1[:]), max(self.x1[:]), self.delta_z / 2, self.d1, self.delta_z / 2, self.n0)
            # Atmosphere
            phz_turb = func.ft_phase_screen(self.r0sw, self.N, self.d1, 100, 0.01)
            phz_turbs[:, :, i] = phz_turb
            delta_n2 = self.k * np.trapz(delta_n[:, :, i - 1:i + 1], [i - 1, i], axis=2)
            delta_n2 = delta_n2 / np.min(delta_n2)
            Uout_turb = Uout_turb * np.exp(complex("j") * delta_n2) * np.exp(
                complex("j") * np.sum(phz_turbs, axis=2) / len(self.z))
            Uout_turb = func.fft_BPM(Uout_turb, self.P, self.wvl, max(self.x1[:]), max(self.x1[:]), self.delta_z / 2, self.d1, self.delta_z / 2, self.n0)

            img = np.abs(np.power(Uout_turb, 2))
            img = np.uint8(img * 255 / np.max(img))
            self.Uout_turbs[:, :, i] = img
        self.onStep2CbChanged()
        print('step2 End')

    def onStep2CbChanged(self):
        self.step2Fig.clear()
        index = self.step2Cb.currentIndex()
        ax = self.step2Fig.add_subplot(111)
        ax.imshow(self.Uout_turbs[:,:,index])
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
        ## Energy fot the Destruction
        # Pleas refer to the Excel file "Destruction_Energy.excel"
        for i in range(int(self.n_iter)):
            self.step3Cb.addItem('Ither {}'.format(i))

        Q_Al = 3169502
        Q_Copper = 4748486
        Q_Steel = 5511702

        # Required Power Calculation
        I_need_Al = Q_Al / float(self.dwell_time.toPlainText())
        I_need_Copper = Q_Copper / float(self.dwell_time.toPlainText())
        I_need_Steel = Q_Steel / float(self.dwell_time.toPlainText())

        ## Time averaging with thermal blooming and tubulence
        # Assume that Turbulence is randomly changed according to time variation or flowed by wind speed
        phz_turbs = np.zeros((self.N, self.N, len(self.z), self.n_iter))
        l2_target2_turbs = np.zeros((self.N, self.N, self.n_iter))

        n_step = 51
        l2_new = np.ndarray((512, 512, 51))
        delta_n = np.ndarray((512, 512, 51))
        for i in range(len(self.z)):
            # print(l2[:,:,i])
            l2_new[:, :, i] = np.roll(self.l2[:, :, i], np.int(np.round(self.move_pixel / n_step) * i))
            n_temp = -self.mu / float(self.v_wind.toPlainText()) * l2_new[:, :, i]
            delta_n[:, :, i] = n_temp

        centers = []

        infl_t, invs = func.dm()
        self.target2_turbs = np.zeros((self.N, self.N, self.n_iter))
        self.target2_holes = np.zeros((self.N, self.N, self.n_iter))

        for j in range(self.n_iter):
            Uin = self.u1[:, :, 0] * np.exp(complex("0+j") * self.k / (2 * float(self.Z.toPlainText())) * self.r ** 2) \
                  * func.make_nanmask(self.r / (float(self.D0.toPlainText()) / 2.67), 1)
            Uout_turb = Uin

            for i in range(1, len(self.z)):
                Uout_turb = func.fft_BPM(Uout_turb, self.P, float(self.wvl.toPlainText()), max(self.x1[:]), max(self.x1[:]), self.delta_z / 2, \
                                         self.d1, self.delta_z / 2, self.n0)
                # Atmosphere
                phz_turb = func.ft_phase_screen(self.r0sw, self.N, self.d1, 100, 0.01)
                phz_turbs[:, :, i, j] = phz_turb
                delta_n2 = self.k * np.trapz(delta_n[:, :, i - 1:i + 1], [i - 1, i], axis=2)
                delta_n2 = delta_n2 / np.min(delta_n2)
                phz_total = delta_n2 + np.sum(phz_turbs[:, :, :, j], axis=2) / len(self.z)
                cmd = np.dot(invs, phz_total.reshape(512 ** 2, 1))
                recon_phz = np.dot(infl_t, cmd)
                resi = phz_total - recon_phz.reshape(512, 512)
                Uout_turb = Uout_turb * np.exp(complex("j") * resi)
                Uout_turb = func.fft_BPM(Uout_turb, self.P, float(self.wvl.toPlainText()), max(self.x1[:]), max(self.x1[:]), self.delta_z / 2, \
                                         self.d1, self.delta_z / 2, self.n0)
            l2_target2_turb = np.abs(np.power(Uout_turb, 2))
            A0 = np.trapz(np.trapz(l2_target2_turb, self.x1, axis=1), self.y1)
            l2_target2_turb = l2_target2_turb * (1 / A0) * float(self.P0.toPlainText())

            l2_target2_turbs[:, :, j] = l2_target2_turb * self.delta_t
            l3 = np.sum(l2_target2_turbs, axis=2)
            img = np.uint8(l3 * 255 / np.max(l3))
            self.target2_turbs[:, :, j] = img
            img2 = np.zeros(shape=l3.shape, dtype=np.uint8)
            img2[np.where(l3 > I_need_Al)] = 255
            self.target2_holes[:, :, j] = img2
        self.onStep3CbChanged()
        print('step3 End')

    def onStep3CbChanged(self):
        self.step3Fig.clear()
        self.step3HoleFig.clear()
        index = self.step3Cb.currentIndex()
        ax = self.step3Fig.add_subplot(111)
        ax2 = self.step3HoleFig.add_subplot(111)
        ax.imshow(self.target2_turbs[:, :, index])
        ax2.imshow(self.target2_holes[:, :, index])
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())