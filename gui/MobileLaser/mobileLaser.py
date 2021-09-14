import cv2
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pypylon import pylon
import ser

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
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
        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                # Access the image data
                image = converter.Convert(grabResult)
                img = image.GetArray()
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                h, w = img.shape
                convertToQtFormat = QImage(img, w, h, w, QImage.Format_Grayscale8)
                p = convertToQtFormat.scaled(1024, 1024, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def stop(self):
        self.camera.StopGrabbing()

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.ser = ser.SerialSocket(self)

        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.picture.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle('Mobile Laser')

        # 채팅창 부분
        infobox = QHBoxLayout()
        gb = QGroupBox('디스플레이')
        infobox.addWidget(gb)

        box = QVBoxLayout()

        self.picture = QLabel(self)
        self.picture.resize(1024, 1024)
        box.addWidget(self.picture)

        gb.setLayout(box)

        # 전원 제어부
        lensControlBox = QHBoxLayout()

        gb = QGroupBox('렌즈 제어부')
        lensControlBox.addWidget(gb)

        box = QVBoxLayout()

        # 전원 BIT
        controlBtnBox = QHBoxLayout()
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

        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(infobox)
        vbox.addLayout(lensControlBox)
        self.setLayout(vbox)

        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.daemon = True
        self.th.start()
        self.show()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())