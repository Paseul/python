import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from imutils.video import FPS
from cv2 import dnn_superres

class Thread(QThread):
    changePixmap = pyqtSignal(QImage, QImage)

    def __init__(self, parent=None):
        super().__init__()
        self.play = True

        self.sr = dnn_superres.DnnSuperResImpl_create()
        self.path = "models/ESPCN_x4.pb"
        self.sr.readModel(self.path)
        self.sr.setModel("espcn", 4)

    def run(self):
        vs = cv2.VideoCapture("rtsp://admin:laser123@192.168.1.64:554/Streaming/Channels/101/")
        fps = FPS().start()
        while self.play:
            success, frame = vs.read()
            if success:
                # rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 0)
                frame= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                sr_frame = frame
                fps.update()
                fps.stop()                
                text = "{:.2f}".format(fps.fps())
                cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                h, w, ch = frame.shape
                bytesPerLine = ch * w                
                convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1600, 900, Qt.KeepAspectRatio)

                sr_frame = sr_frame[(int)(h/2 - 60):(int)(h/2 + 60), (int)(w/2 - 60):(int)(w/2 + 60)]
                sr_frame = self.sr.upsample(sr_frame)
                h, w, ch = sr_frame.shape
                bytesPerLine = ch * w                
                convertToQtFormat = QImage(sr_frame.data, w, h, bytesPerLine, QImage.Format_RGB888)                
                q = convertToQtFormat.scaled(480, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p, q)

    def stop(self):
        self.play = False
