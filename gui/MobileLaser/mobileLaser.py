import cv2
import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pypylon import pylon
from PyQt5.QtWebEngineWidgets import QWebEngineView
import ser
import socket
import struct
import numpy as np
from cv2 import dnn_superres
from filterpy.kalman import UnscentedKalmanFilter as UKF
from filterpy.kalman import MerweScaledSigmaPoints
from filterpy.common import Q_discrete_white_noise
import js

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

port = 5000
ip = '127.0.1.1'
serverAddressPort = ("192.168.1.31", 55000)

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    thread_signal = pyqtSignal(int, int)
    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
        self.val = ""
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.dt = 1.0 / 30.0

    def f_cv(self, x, dt):
        """ state transition function for a
        constant velocity aircraft"""

        F = np.array([[1, self.dt, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, self.dt],
                      [0, 0, 0, 1]])
        return np.dot(F, x)

    def h_cv(self, x):
        return x[[0, 2]]

    def run(self):
        sigmas = MerweScaledSigmaPoints(4, alpha=.1, beta=2., kappa=-1.)
        ukf = UKF(dim_x=4, dim_z=2, fx=self.f_cv,
                  hx=self.h_cv, dt=self.dt, points=sigmas)

        # assume error is 0.3m
        ukf.R = np.diag([0.09, 0.09])

        ukf.Q[0:2, 0:2] = Q_discrete_white_noise(2, dt=self.dt, var=0.02)
        ukf.Q[2:4, 2:4] = Q_discrete_white_noise(2, dt=self.dt, var=0.02)

        last_measurement = None
        last_prediction = None

        trackers = [cv2.TrackerCSRT_create,
                    cv2.TrackerMIL_create,
                    cv2.TrackerKCF_create
                    ]

        tracker = cv2.TrackerCSRT_create

        # conecting to the first available camera
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        # Grabing Continusely (video) with minimal delay
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        converter = pylon.ImageFormatConverter()

        # Control Exposure Time
        self.camera.ExposureTime.SetValue(20000)

        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        # Create an SR object
        sr = dnn_superres.DnnSuperResImpl_create()

        # Read the desired model
        path = "ESPCN_x4.pb"
        sr.readModel(path)

        # Set the desired model and scale to get correct pre- and post-processing
        sr.setModel("espcn", 4)

        initBB = None

        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                # Access the image data
                image = converter.Convert(grabResult)
                img = image.GetArray()
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                if initBB is not None:
                    # grab the new bounding box coordinates of the object
                    (success, box) = tracker.update(img)
                    # check to see if the tracking was a success
                    if success:
                        (x, y, w, h) = [int(v) for v in box]
                        cv2.rectangle(img, (x, y), (x + w, y + h),
                                      (0, 255, 0), 2)
                        (img_h, img_w) = img.shape
                        center_x, center_y = x + w / 2, y + h / 2

                        measurement = np.array([center_x, center_y], np.float32)
                        if last_measurement is None:
                            ukf.x = np.array([center_x, 0, center_y, 0], np.float32)
                            # prediction = measurement
                            self.thread_signal.emit((int)(measurement[0] - img_w / 2), (int)(measurement[1] - img_h / 2))
                        else:
                            ukf.predict()
                            ukf.update(measurement)

                            # Trace the path of the prediction in red.
                            # cv2.arrowedLine(frame, (measurement[0], measurement[1]),
                            # 	((int)(ukf.x[0]), (int)(ukf.x[2])), (0, 0, 255), 1)
                            # cv2.rectangle(frame, (last_prediction[0], last_prediction[1]), (last_prediction[0] + w, last_prediction[1] + h),
                            # 	(0, 0, 255), 2)
                            self.thread_signal.emit((int)(measurement[0] - img_w - ukf.x[0]), (int)(center_y - img_h / 2 - ukf.x[2]))
                        # last_prediction = ukf.x.copy()
                        last_measurement = measurement

                        # try:
                        #     frame = img[(int)(y - h * 2):(int)(y + h * 3), (int)(x - w * 2):(int)(x + w * 3)]
                        #     frame = sr.upsample(frame)
                        #     frame = cv2.resize(frame, dsize=(640, 480), interpolation=cv2.INTER_CUBIC)
                        #     convertToQtFormat2 = QImage(frame, 640, 480, 640, QImage.Format_Grayscale8)
                        #     q = convertToQtFormat2.scaled(640, 640, Qt.KeepAspectRatio)
                        # except Exception as e:
                        #     q = convertToQtFormat.scaled(640, 640, Qt.KeepAspectRatio)
                h, w = img.shape

                convertToQtFormat = QImage(img, w, h, w, QImage.Format_Grayscale8)

                p = convertToQtFormat.scaled(1020, 1020, Qt.KeepAspectRatio)
                # if initBB is None:
                #     q = convertToQtFormat.scaled(640, 640, Qt.KeepAspectRatio)

                if self.val == "c":
                    self.val = ""
                    tracker = trackers[0]()
                    initBB = (self.x, self.y, self.w, self.h)
                    # start OpenCV object tracker using the supplied bounding box
                    # coordinates, then start the FPS throughput estimator as well
                    tracker.init(img, initBB)

                self.changePixmap.emit(p)


    def stop(self):
        self.camera.StopGrabbing()

    def recive_signal(self, val, x, y, w, h):
        self.val = val
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class App(QWidget):
    main_signal = pyqtSignal(str, int, int, int, int)
    def __init__(self):
        super().__init__()

        self.ser = ser.SerialSocket(self)
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.start_x = 0
        self.start_y = 0

        self.js = js.Joystick(self)

        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.picture.setPixmap(QPixmap.fromImage(image))
        # self.swirLabel.setPixmap(QPixmap.fromImage(image2))


    def initUI(self):
        self.setWindowTitle('Mobile Laser')

        # 채팅창 부분
        mainView = QVBoxLayout()
        gb = QGroupBox('디스플레이')
        mainView.addWidget(gb)

        box = QHBoxLayout()

        self.picture = QLabel(self)
        self.picture.resize(1020, 1020)
        box.addWidget(self.picture)

        gb.setLayout(box)

        # swirGpsBox = QVBoxLayout()
        # box.addLayout(swirGpsBox)
        #
        # self.swirLabel = QLabel(self)
        # self.swirLabel.resize(640, 640)
        # swirGpsBox.addWidget(self.swirLabel)
        # self.webView = QWebEngineView()
        # filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.html"))
        # self.webView.load(QUrl.fromLocalFile(filepath))
        # swirGpsBox.addWidget(self.webView)
        # gb.setLayout(swirGpsBox)

        # 전원 제어부
        bitDisplayBox = QHBoxLayout()
        gb = QGroupBox('Control')
        bitDisplayBox.addWidget(gb)

        box = QVBoxLayout()

        # 전원 BIT
        bitBox = QVBoxLayout()
        box.addLayout(bitBox)

        self.laser_bit = QPushButton('Stop')
        self.laser_bit.clicked.connect(self.gimbalStop)
        bitBox.addWidget(self.laser_bit)

        self.power_bit = QPushButton('Zero')
        self.power_bit.clicked.connect(self.gimbalCenter)
        bitBox.addWidget(self.power_bit)

        self.chiller_bit = QPushButton('Manual')
        self.chiller_bit.clicked.connect(self.gimbalManual)
        bitBox.addWidget(self.chiller_bit)

        self.act_bit = QPushButton('Joystick')
        self.act_bit.clicked.connect(self.gimbalJoystick)
        bitBox.addWidget(self.act_bit)

        self.camera_bit = QPushButton('Pixel')
        self.camera_bit.clicked.connect(self.gimbalPixel)
        bitBox.addWidget(self.camera_bit)

        # self.p_Btn = QPushButton('접속')
        # self.p_Btn.clicked.connect(self.powerConnect)
        # bitBox.addWidget(self.p_Btn)
        #
        # self.focusNearBtn = QPushButton('Focus Near')
        # self.focusNearBtn.clicked.connect(self.focusNear)
        # bitBox.addWidget(self.focusNearBtn)
        #
        # self.focusWideBtn = QPushButton('Focus Wide')
        # self.focusWideBtn.clicked.connect(self.focusWide)
        # bitBox.addWidget(self.focusWideBtn)
        #
        # self.zoomWideBtn = QPushButton('Zoom Wide')
        # self.zoomWideBtn.clicked.connect(self.zoomWide)
        # bitBox.addWidget(self.zoomWideBtn)
        #
        # self.zoomTeleBtn = QPushButton('Zoom Tele')
        # self.zoomTeleBtn.clicked.connect(self.zoomTele)
        # bitBox.addWidget(self.zoomTeleBtn)
        #
        # self.irisCloseBtn = QPushButton('Iris Close')
        # self.irisCloseBtn.clicked.connect(self.irisClose)
        # bitBox.addWidget(self.irisCloseBtn)
        #
        # self.irisOpenBtn = QPushButton('Iris Open')
        # self.irisOpenBtn.clicked.connect(self.irisOpen)
        # bitBox.addWidget(self.irisOpenBtn)
        #
        # self.stopBtn = QPushButton('Stop')
        # self.stopBtn.clicked.connect(self.stop)
        # bitBox.addWidget(self.stopBtn)

        self.distanceMsg = QTextEdit()
        self.distanceMsg.setFixedHeight(30)
        self.distanceMsg.setText('12345')
        bitBox.addWidget(self.distanceMsg)

        self.label = QLabel(self)
        bitBox.addWidget(self.label)

        gb.setLayout(box)

        # 전체 배치
        hbox = QHBoxLayout()
        hbox.addLayout(mainView)
        hbox.addLayout(bitDisplayBox)
        self.setLayout(hbox)

        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.main_signal.connect(self.th.recive_signal)
        self.th.thread_signal.connect(self.udpSend)
        self.th.daemon = True
        self.th.start()
        self.show()

    def udpUpdate(self, mode, cbit, aziLocalAngle, eleLocalAngle, aziLocalSpeed, eleLocalSpeed, aziGlobalAngle, eleGlobalAngle, aziGlobalSpeed, eleGlobalSpeed):
        self.recvmsg.addItem(mode, cbit, aziLocalAngle, eleLocalAngle, aziLocalSpeed, eleLocalSpeed, aziGlobalAngle, eleGlobalAngle, aziGlobalSpeed, eleGlobalSpeed)

    def udpSend(self, x, y):
        distance = int(self.distanceMsg.toPlainText(), 32)

        values = (32770, 0, 0, 0, 0, x, y, distance)
        fmt = '>H i i i i i i I'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)
        # print(x, y)
        # print(sendData)
        self.UDPClientSocket.sendto(sendData, serverAddressPort)

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

    def gimbalStop(self):
        values = (32769, 0)
        fmt = '>H b'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)

        self.UDPClientSocket.sendto(sendData, serverAddressPort)

    def gimbalCenter(self):
        values = (32769, 1)
        fmt = '>H b'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)

        self.UDPClientSocket.sendto(sendData, serverAddressPort)

    def gimbalManual(self):
        values = (32769, 2)
        fmt = '>H b'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)

        self.UDPClientSocket.sendto(sendData, serverAddressPort)

    def gimbalJoystick(self):
        values = (32769, 3)
        fmt = '>H b'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)

        self.UDPClientSocket.sendto(sendData, serverAddressPort)

    def gimbalPixel(self):
        values = (32769, 4)
        fmt = '>H b'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)

        self.UDPClientSocket.sendto(sendData, serverAddressPort)

    def focusNear(self):
        self.ser.send(1, 1, 0)

    def focusWide(self):
        self.ser.send(1, 0, 128)

    def zoomWide(self):
        self.ser.send(1, 0, 64)

    def zoomTele(self):
        self.ser.send(1, 0, 32)

    def irisClose(self):
        self.ser.send(1, 4, 0)

    def irisOpen(self):
        self.ser.send(1, 2, 0)

    def stop(self):
        self.ser.send(1, 0, 0)

    def updatePower(self, msg):
        self.recvmsg.addItem(msg)

    def powerDisconnect(self):
        self.p_btn.setText('접속')

    def closeEvent(self, e):
        self.hide()
        self.th.stop()

    def mousePressEvent(self, e):  # e ; QMouseEvent
        self.start_x = e.x()
        self.start_y = e.y()

    def mouseReleaseEvent(self, e): # e ; QMouseEvent
        x = self.start_x + e.x()-42
        y = self.start_y + e.y()-66
        w = (e.x() - self.start_x)*2
        h = (e.y() - self.start_y)*2

        self.main_signal.emit("c", x, y, w, h)

    def jsUpdate(self, azimuth, elivation):
        values = (32770, 0, 0, azimuth, elivation, 0, 0, 0)
        fmt = '>H i i i i i i I'
        packer = struct.Struct(fmt)
        sendData = packer.pack(*values)

        self.UDPClientSocket.sendto(sendData, serverAddressPort)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())