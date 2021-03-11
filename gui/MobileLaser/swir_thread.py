import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from pypylon import pylon
from imutils.video import FPS
import numpy as np

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def __init__(self, parent=None):
        super().__init__()
        # conecting to the first available camera
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        # Grabing Continusely (video) with minimal delay
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        self.converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        # # Control Exposure Time
        # self.camera.ExposureTime.SetValue(10000)

        self.play = True

    def run(self):
        fps = FPS().start()
        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)   

            if grabResult.GrabSucceeded():
                # Access the image data
                frame = self.converter.Convert(grabResult)
                frame = frame.GetArray()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                fps.update()
                fps.stop()        
                text = "{:.2f}".format(fps.fps())
                cv2.putText(frame, text, (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 5)

                h, w, ch = frame.shape
                bytesPerLine = ch * w             
                convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 360, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
            grabResult.Release()
            if self.play == False:
                break
        self.camera.StopGrabbing()

    def stop(self):
        self.play = False