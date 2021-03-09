import cv2
import sys
import ccd_thread
import swir_thread
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from imutils.video import FPS

class App(QWidget):
    def __init__(self):
        super().__init__()        

        self.initUI()

        self.ccd = ccd_thread.Thread(self)
        self.ccd.changePixmap.connect(self.setCcdImage)        
        self.ccd.deamon = True
        self.ccd.start()
        self.swir = swir_thread.Thread(self)
        self.swir.changePixmap.connect(self.setSwirImage)        
        self.swir.deamon = True
        self.swir.start()

    def closeEvent(self, e):
        self.ccd.stop()
        self.swir.stop()

    @pyqtSlot(QImage)
    def setCcdImage(self, image):
        self.ccdLabel.setPixmap(QPixmap.fromImage(image))
    
    @pyqtSlot(QImage)
    def setSwirImage(self, image):
        self.swirLabel.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle('Mobile Laser')

        box = QHBoxLayout()
        # create a label
        self.ccdLabel = QLabel(self)
        self.ccdLabel.resize(1280, 720)
        box.addWidget(self.ccdLabel)
        self.swirLabel = QLabel(self)
        self.swirLabel.resize(640, 360)
        box.addWidget(self.swirLabel)
        self.setLayout(box)        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = App()
    sys.exit(app.exec_())