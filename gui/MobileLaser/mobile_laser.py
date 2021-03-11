import cv2
import sys
import io
import os
import folium
import ccd_thread
import swir_thread
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from imutils.video import FPS

class App(QWidget):
    def __init__(self):
        super().__init__()        
        
        self.data = io.BytesIO()
        self.x = 37.40494
        self.y = 127.11130
        self.loadMap(self.x, self.y)

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

    def loadMap(self, x, y):
        m = folium.Map(zoom_start=18, location=(x,y))
        m.save(self.data, close_file=False)
        m.save("map.html")

    def initUI(self):
        self.setWindowTitle('Mobile Laser')

        box = QHBoxLayout()
        # create a label
        self.ccdLabel = QLabel(self)
        self.ccdLabel.resize(1280, 720)
        box.addWidget(self.ccdLabel)

        swirGpsBox = QVBoxLayout()
        box.addLayout(swirGpsBox)
        self.swirLabel = QLabel(self)
        self.swirLabel.resize(640, 360)
        swirGpsBox.addWidget(self.swirLabel)
        self.webView = QWebEngineView()
        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.html"))
        self.webView.load(QUrl.fromLocalFile(filepath))
        swirGpsBox.addWidget(self.webView)
        self.setLayout(box)        
        self.show()
    
    def keyPressEvent(self, e):        
        if e.key() == Qt.Key_Right:
            self.x, self.y = self.x, self.y+0.0005

        elif e.key() == Qt.Key_Left:
            self.x, self.y = self.x, self.y-0.0005

        elif e.key() == Qt.Key_Up:
            self.x, self.y = self.x+0.0005, self.y

        elif e.key() == Qt.Key_Down:
            self.x, self.y = self.x-0.0005, self.y

        m = folium.Map(zoom_start=18,location=(self.x, self.y))
        m.save(self.data, close_file=False)
        m.save("map.html")
        self.webView.reload()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = App()
    sys.exit(app.exec_())