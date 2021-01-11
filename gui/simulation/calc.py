from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import func

class PopUpProgress(QWidget):

    def __init__(self):
        super().__init__()
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 500, 75)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.pbar)
        self.setLayout(self.layout)
        self.setGeometry(700, 500, 550, 100)
        self.setWindowTitle('Calculating')

        self.thread = QThread()

    def start_progress(self):  # To restart the progress every time
        self.show()
        self.thread.start()

class Step1Thread(QThread):
    result = pyqtSignal(np.ndarray)

    def __init__(self, N, wd, z, Z, theta_diff, theta_spread, u1, r, x1, y1, l2, P0, k, D0, P, wvl, delta_z, d1, n0):
        super().__init__()
        self.N = N
        self.wd = wd
        self.z = z
        self.Z = Z
        self.theta_diff = theta_diff
        self.theta_spread = theta_spread
        self.u1 = u1
        self.r = r
        self.x1 = x1
        self.y1 = y1
        self.l2 = l2
        self.P0 = P0
        self.k = k
        self.D0 = D0
        self.P = P
        self.wvl = wvl
        self.delta_z = delta_z
        self.d1 = d1
        self.n0 = n0

    def run(self):
        wz = []
        wz_spread = []
        step1Results = np.zeros((self.N, self.N, 3))

        for _ in range(51):
            wz.append(0)
            wz_spread.append(0)
        for i in range(51):
            wz[i] = np.sqrt(
                (self.wd * (1 - self.z[i] / self.Z)) ** 2 + self.theta_diff ** 2 * self.z[i] ** 2)
            wz_spread[i] = np.sqrt(
                (self.wd * (1 - self.z[i] / self.Z)) ** 2 + self.theta_spread ** 2 * self.z[
                    i] ** 2)

        for i in range(51):
            self.u1[:, :, i] = (self.wd / wz[i]) * np.exp(-np.power(self.r, 2) / np.power(wz[i], 2))
            l = np.abs(np.power(self.u1[:, :, i], 2))
            # Nomalization
            A0 = np.trapz(np.trapz(l, self.x1, axis=1), self.y1)
            self.l2[:, :, i] = l * (1 / A0) * self.P0

        step1Results[:,:,0] = self.l2[:, :, 0]
        step1Results[:,:,1] = self.l2[:, :, 50]
        Uin = self.u1[:, :, 0] * np.exp(complex("0+j") * self.k / (2 * self.Z) * self.r ** 2) \
              * func.make_nanmask(self.r / (self.D0 / 2.67), 1)
        Uout = Uin

        for i in range(1, len(self.z) - 1):
            Uout = func.fft_BPM(Uout, self.P, self.wvl, max(self.x1[:]), max(self.x1[:]),
                                self.delta_z / 2, self.d1, self.delta_z / 2, self.n0)
            Uout = func.fft_BPM(Uout, self.P, self.wvl, max(self.x1[:]), max(self.x1[:]),
                                self.delta_z / 2, self.d1, self.delta_z / 2, self.n0)

        l2_target2 = abs(np.power(Uout, 2))
        A0 = np.trapz(np.trapz(l2_target2, self.x1, axis=1), self.y1)
        l2_target2 = l2_target2 * (1 / A0) * self.P0
        step1Results[:,:,2] = l2_target2
        self.result.emit(step1Results)

class Step2Thread(QThread):
    result = pyqtSignal(np.ndarray)

    def __init__(self, N, z, l2, move_pixel, mu, v_wind, u1, k, Z, r, D0, P, wvl, x1, delta_z, d1, n0, r0sw):
        super().__init__()
        self.N = N
        self.z = z
        self.l2 = l2
        self.move_pixel = move_pixel
        self.mu = mu
        self.v_wind = v_wind
        self.u1 = u1
        self.k = k
        self.Z = Z
        self.r = r
        self.D0 = D0
        self.P = P
        self.wvl = wvl
        self.x1 = x1
        self.delta_z = delta_z
        self.d1 = d1
        self.n0 = n0
        self.r0sw = r0sw
        self.popup = PopUpProgress()
        self.popup.start_progress()

    def run(self):
        # With Thermal Blooming & Atmosphere
        # Thermal blooming
        n_step = 51
        count = 0
        l2_new = np.ndarray((512, 512, 51))
        delta_n = np.ndarray((512, 512, 51))
        for i in range(len(self.z)):
            # print(l2[:,:,i])
            l2_new[:, :, i] = np.roll(self.l2[:, :, i], np.int(np.round(self.move_pixel / n_step) * i))
            n_temp = -self.mu / self.v_wind * l2_new[:, :, i]
            delta_n[:, :, i] = n_temp

        # Input Phase -> Uin = U * lens_aperture * phase_TB * phase_turb
        Uin = self.u1[:, :, 0] * np.exp(complex("0+j") * self.k / (2 * self.Z) * self.r ** 2) \
              * func.make_nanmask(self.r / (self.D0 / 2.67), 1)
        Uout_turb = Uin

        phz_turbs = np.zeros((self.N, self.N, len(self.z)))
        Uout_turbs = np.zeros((self.N, self.N, len(self.z)))
        img = np.abs(np.power(Uout_turb, 2))
        img = np.uint8(img * 255 / np.max(img))
        Uout_turbs[:, :, 0] = img
        for i in range(1, len(self.z)):
            Uout_turb = func.fft_BPM(Uout_turb, self.P, self.wvl, max(self.x1[:]), max(self.x1[:]),
                                     self.delta_z / 2, self.d1, self.delta_z / 2, self.n0)
            # Atmosphere
            phz_turb = func.ft_phase_screen(self.r0sw, self.N, self.d1, 100, 0.01)
            phz_turbs[:, :, i] = phz_turb
            delta_n2 = self.k * np.trapz(delta_n[:, :, i - 1:i + 1], [i - 1, i], axis=2)
            delta_n2 = delta_n2 / np.min(delta_n2)
            Uout_turb = Uout_turb * np.exp(complex("j") * delta_n2) * np.exp(
                complex("j") * np.sum(phz_turbs, axis=2) / len(self.z))
            Uout_turb = func.fft_BPM(Uout_turb, self.P, self.wvl, max(self.x1[:]), max(self.x1[:]), self.delta_z / 2,
                                     self.d1, self.delta_z / 2, self.n0)

            img = np.abs(np.power(Uout_turb, 2))
            img = np.uint8(img * 255 / np.max(img))
            Uout_turbs[:, :, i] = img
            count += 100 / (len(self.z) - 1)
            self.popup.pbar.setValue(int(count))
        self.popup.thread.quit()
        self.popup.hide()
        self.result.emit(Uout_turbs)

class Step3Thread(QThread):
    result = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self, material, dwell_time, N, z, n_iter, l2, move_pixel, mu, v_wind, u1, k, Z, r, D0, P, P0, wvl, x1, y1, delta_z, d1, n0, r0sw, delta_t):
        super().__init__()
        self.material = material
        self.dwell_time = dwell_time
        self.N = N
        self.z = z
        self.n_iter = n_iter
        self.l2 = l2
        self.move_pixel = move_pixel
        self.mu = mu
        self.v_wind = v_wind
        self.u1 = u1
        self.k = k
        self.Z = Z
        self.r = r
        self.D0 = D0
        self.P = P
        self.P0 = P0
        self.wvl = wvl
        self.x1 = x1
        self.y1 = y1
        self.delta_z = delta_z
        self.d1 = d1
        self.n0 = n0
        self.r0sw = r0sw
        self.delta_t = delta_t
        self.popup = PopUpProgress()
        self.popup.start_progress()

    def run(self):
        ## Energy fot the Destruction
        # Required Power Calculation
        reqPower = self.material / self.dwell_time

        ## Time averaging with thermal blooming and tubulence
        # Assume that Turbulence is randomly changed according to time variation or flowed by wind speed
        phz_turbs = np.zeros((self.N, self.N, len(self.z), self.n_iter))
        l2_target2_turbs = np.zeros((self.N, self.N, self.n_iter))

        n_step = 51
        count = 0
        l2_new = np.ndarray((512, 512, 51))
        delta_n = np.ndarray((512, 512, 51))
        for i in range(len(self.z)):
            # print(l2[:,:,i])
            l2_new[:, :, i] = np.roll(self.l2[:, :, i], np.int(np.round(self.move_pixel / n_step) * i))
            n_temp = -self.mu / self.v_wind * l2_new[:, :, i]
            delta_n[:, :, i] = n_temp

        centers = []

        infl_t, invs = func.dm()
        target2_turbs = np.zeros((self.N, self.N, self.n_iter))
        target2_holes = np.zeros((self.N, self.N, self.n_iter))

        for j in range(self.n_iter):
            Uin = self.u1[:, :, 0] * np.exp(complex("0+j") * self.k / (2 * self.Z) * self.r ** 2) \
                  * func.make_nanmask(self.r / (self.D0 / 2.67), 1)
            Uout_turb = Uin

            for i in range(1, len(self.z)):
                Uout_turb = func.fft_BPM(Uout_turb, self.P, self.wvl, max(self.x1[:]),
                                         max(self.x1[:]), self.delta_z / 2, \
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
                Uout_turb = func.fft_BPM(Uout_turb, self.P, self.wvl, max(self.x1[:]),
                                         max(self.x1[:]), self.delta_z / 2, \
                                         self.d1, self.delta_z / 2, self.n0)
                count += 100 / (self.n_iter * (len(self.z) - 1))
                self.popup.pbar.setValue(int(count))
            l2_target2_turb = np.abs(np.power(Uout_turb, 2))
            A0 = np.trapz(np.trapz(l2_target2_turb, self.x1, axis=1), self.y1)
            l2_target2_turb = l2_target2_turb * (1 / A0) * self.P0

            l2_target2_turbs[:, :, j] = l2_target2_turb * self.delta_t
            l3 = np.sum(l2_target2_turbs, axis=2)
            img = np.uint8(l3 * 255 / np.max(l3))
            target2_turbs[:, :, j] = img
            img2 = np.zeros(shape=l3.shape, dtype=np.uint8)
            img2[np.where(l3 > reqPower)] = 255
            target2_holes[:, :, j] = img2
        self.popup.thread.quit()
        self.popup.hide()
        self.result.emit(target2_turbs, target2_holes)