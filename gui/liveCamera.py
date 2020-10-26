import cv2
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from pypylon import pylon
import numpy as np
from matplotlib import pyplot as plt
import cv2
import argparse
from Iso11146 import Iso11146

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="Original.avi",
                help="path to the (optional) video file")
ap.add_argument("-e", "--exposure_time", type=int, default=20000,
                help="Set Exposure Time")
ap.add_argument("-min", "--minimum_thresh", type=int, default=50,
                help="minimum thresh value")
ap.add_argument("-max", "--maximum_thresh", type=int, default=255,
                help="maximum thresh value")
args = vars(ap.parse_args())

class ShowVideo(QtCore.QObject):
    flag = 0
    height, width = 343, 480

    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)

    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()

    # Control Exposure Time
    camera.ExposureTime.SetValue(args["exposure_time"])

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    # save video
    videoWriter = cv2.VideoWriter()

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    videoWriter.open(args["output"], fourcc, 14, (480, 343), False)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        global image

        while self.camera.IsGrabbing():

            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                # Access the image data
                img = self.converter.Convert(grabResult)
                img = img.GetArray()
                image = cv2.resize(img, (480, 343))
                color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                qt_image1 = QtGui.QImage(color_swapped_image.data,
                                         self.width,
                                         self.height,
                                         color_swapped_image.strides[0],
                                         QtGui.QImage.Format_Grayscale8)
                self.VideoSignal1.emit(qt_image1)

                if self.flag:
                    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    img_canny = cv2.Canny(img_gray, 50, 100)

                    qt_image2 = QtGui.QImage(img_canny.data,
                                             self.width,
                                             self.height,
                                             img_canny.strides[0],
                                             QtGui.QImage.Format_Grayscale8)

                    self.VideoSignal2.emit(qt_image2)

                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(25, loop.quit)  # 25 ms
                loop.exec_()

            grabResult.Release()
        self.camera.StopGrabbing()
        self.videoWriter.release()
    @QtCore.pyqtSlot()
    def canny(self):
        self.flag = 1 - self.flag


class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)

    image_viewer1 = ImageViewer()
    image_viewer2 = ImageViewer()

    vid.VideoSignal1.connect(image_viewer1.setImage)
    vid.VideoSignal2.connect(image_viewer2.setImage)

    push_button1 = QtWidgets.QPushButton('Start')
    push_button2 = QtWidgets.QPushButton('Canny')
    push_button1.clicked.connect(vid.startVideo)
    push_button2.clicked.connect(vid.canny)

    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()
    horizontal_layout.addWidget(image_viewer1)
    horizontal_layout.addWidget(image_viewer2)
    vertical_layout.addLayout(horizontal_layout)
    vertical_layout.addWidget(push_button1)
    vertical_layout.addWidget(push_button2)

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    # Releasing the resource
    sys.exit(app.exec_())