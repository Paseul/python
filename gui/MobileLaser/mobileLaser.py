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

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

port = 5000
ip = '127.0.1.1'
serverAddressPort = ("192.168.1.31", 55000)

class Thread(QThread):
    changePixmap = pyqtSignal(QImage, QImage)
    thread_signal = pyqtSignal(int, int)
    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
        self.val = ""
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

    def run(self):
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
                                      (0, 255, 0), 1)
                        self.thread_signal.emit(x-1020, y-1020)

                h, w = img.shape

                convertToQtFormat = QImage(img, w, h, w, QImage.Format_Grayscale8)
                p = convertToQtFormat.scaled(1020, 1020, Qt.KeepAspectRatio)
                q = convertToQtFormat.scaled(640, 640, Qt.KeepAspectRatio)

                if self.val == "c":
                    self.val = ""
                    tracker = trackers[0]()
                    initBB = (self.x, self.y, self.w, self.h)
                    # start OpenCV object tracker using the supplied bounding box
                    # coordinates, then start the FPS throughput estimator as well
                    tracker.init(img, initBB)

                self.changePixmap.emit(p, q)

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

        self.initUI()

    @pyqtSlot(QImage, QImage)
    def setImage(self, image, image2):
        self.picture.setPixmap(QPixmap.fromImage(image))
        self.swirLabel.setPixmap(QPixmap.fromImage(image2))

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

        swirGpsBox = QVBoxLayout()
        box.addLayout(swirGpsBox)

        self.swirLabel = QLabel(self)
        self.swirLabel.resize(640, 640)
        swirGpsBox.addWidget(self.swirLabel)
        self.webView = QWebEngineView()
        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.html"))
        self.webView.load(QUrl.fromLocalFile(filepath))
        swirGpsBox.addWidget(self.webView)
        gb.setLayout(swirGpsBox)

        # 전원 제어부
        bitDisplayBox = QHBoxLayout()
        gb = QGroupBox('BIT')
        bitDisplayBox.addWidget(gb)

        box = QVBoxLayout()

        # 전원 BIT
        bitBox = QVBoxLayout()
        box.addLayout(bitBox)

        self.laser_bit = QPushButton('레이저 BIT')
        self.laser_bit.setStyleSheet("background-color: green")
        bitBox.addWidget(self.laser_bit)

        self.power_bit = QPushButton('전원 BIT')
        self.power_bit.setStyleSheet("background-color: green")
        bitBox.addWidget(self.power_bit)

        self.chiller_bit = QPushButton('냉각기 BIT')
        self.chiller_bit.setStyleSheet("background-color: green")
        bitBox.addWidget(self.chiller_bit)

        self.act_bit = QPushButton('구동장치 BIT')
        self.act_bit.setStyleSheet("background-color: green")
        bitBox.addWidget(self.act_bit)

        self.camera_bit = QPushButton('카메라 BIT')
        self.camera_bit.setStyleSheet("background-color: green")
        bitBox.addWidget(self.camera_bit)

        self.lens_bit = QPushButton('줌랜즈 BIT')
        self.lens_bit.setStyleSheet("background-color: green")
        bitBox.addWidget(self.lens_bit)

        self.lrf_bit = QPushButton('LRF BIT')
        self.lrf_bit.setStyleSheet("background-color: green")
        bitBox.addWidget(self.lrf_bit)

        self.gps_bit = QPushButton('GPS BIT')
        self.gps_bit.setStyleSheet("background-color: green")
        bitBox.addWidget(self.gps_bit)

        self.joystick_bit = QPushButton('조이스틱 BIT')
        self.joystick_bit.setStyleSheet("background-color: green")
        bitBox.addWidget(self.joystick_bit)

        self.label = QLabel(self)
        bitBox.addWidget(self.label)

        gb.setLayout(box)

        # 전원 BIT
        lensControlBox = QHBoxLayout()
        gb = QGroupBox('Control')
        lensControlBox.addWidget(gb)

        box = QVBoxLayout()

        controlBtnBox = QVBoxLayout()
        box.addLayout(controlBtnBox)

        self.p_Btn = QPushButton('접속')
        self.p_Btn.clicked.connect(self.powerConnect)
        controlBtnBox.addWidget(self.p_Btn)

        self.focusNearBtn = QPushButton('Focus Near')
        self.focusNearBtn.clicked.connect(self.focusNear)
        controlBtnBox.addWidget(self.focusNearBtn)

        self.focusWideBtn = QPushButton('Focus Wide')
        self.focusWideBtn.clicked.connect(self.focusWide)
        controlBtnBox.addWidget(self.focusWideBtn)

        self.zoomWideBtn = QPushButton('Zoom Wide')
        self.zoomWideBtn.clicked.connect(self.zoomWide)
        controlBtnBox.addWidget(self.zoomWideBtn)

        self.zoomTeleBtn = QPushButton('Zoom Tele')
        self.zoomTeleBtn.clicked.connect(self.zoomTele)
        controlBtnBox.addWidget(self.zoomTeleBtn)

        self.irisCloseBtn = QPushButton('Iris Close')
        self.irisCloseBtn.clicked.connect(self.irisClose)
        controlBtnBox.addWidget(self.irisCloseBtn)

        self.irisOpenBtn = QPushButton('Iris Open')
        self.irisOpenBtn.clicked.connect(self.irisOpen)
        controlBtnBox.addWidget(self.irisOpenBtn)

        self.stopBtn = QPushButton('Stop')
        self.stopBtn.clicked.connect(self.stop)
        controlBtnBox.addWidget(self.stopBtn)

        # Cmd
        self.cmdMsg = QTextEdit()
        self.cmdMsg.setFixedHeight(30)
        self.cmdMsg.setText('4')
        controlBtnBox.addWidget(self.cmdMsg)
        # data
        self.aziMsg = QTextEdit()
        self.aziMsg.setFixedHeight(30)
        self.aziMsg.setText('11')
        controlBtnBox.addWidget(self.aziMsg)
        # data
        self.eleMsg = QTextEdit()
        self.eleMsg.setFixedHeight(30)
        self.eleMsg.setText('22')
        controlBtnBox.addWidget(self.eleMsg)

        # data
        self.distanceMsg = QTextEdit()
        self.distanceMsg.setFixedHeight(30)
        self.distanceMsg.setText('12345')
        controlBtnBox.addWidget(self.distanceMsg)

        self.udpSendBtn = QPushButton('UDP Send')
        self.udpSendBtn.clicked.connect(self.udpSend)
        controlBtnBox.addWidget(self.udpSendBtn)

        self.recvmsg = QListWidget()
        box.addWidget(self.recvmsg)

        self.label = QLabel(self)
        controlBtnBox.addWidget(self.label)

        gb.setLayout(box)

        # 전체 배치
        hbox = QHBoxLayout()
        hbox.addLayout(mainView)
        hbox.addLayout(bitDisplayBox)
        hbox.addLayout(lensControlBox)
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
        # self.UDPClientSocket.sendto(sendData, serverAddressPort)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())