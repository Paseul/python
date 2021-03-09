import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from imutils.video import FPS

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def __init__(self, parent=None):
        super().__init__()
        self.play = True

    def run(self):
        vs = cv2.VideoCapture("rtsp://admin:laser123@192.168.1.64:554/Streaming/Channels/101/")
        fps = FPS().start()
        while self.play:
            success, frame = vs.read()
            if success:
                # rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 0)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                fps.update()
                fps.stop() 
                text = "{:.2f}".format(fps.fps())
                cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                h, w, ch = frame.shape
                bytesPerLine = ch * w                
                convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1280, 720, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def stop(self):
        self.play = False
