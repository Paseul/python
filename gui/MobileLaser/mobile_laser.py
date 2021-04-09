import cv2
import sys
import io
import os
import folium
import numpy as np
import ccd_thread
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from imutils.video import FPS
from cv2 import dnn_superres

class App(QWidget):
    def __init__(self):
        super().__init__()        
        
        self.data = io.BytesIO()
        self.x = 37.40494
        self.y = 127.11130
        self.loadMap(self.x, self.y)
        self.arcreading = 270
        self.adder = 0.1

        self.initUI()

        self.ccd = ccd_thread.Thread(self)
        self.ccd.changePixmap.connect(self.setCcdImage)        
        self.ccd.deamon = True
        self.ccd.start()        

    def closeEvent(self, e):
        self.ccd.stop()

    @pyqtSlot(QImage, QImage)
    def setCcdImage(self, image, image2):
        self.ccdLabel.setPixmap(QPixmap.fromImage(image))
        self.swirLabel.setPixmap(QPixmap.fromImage(image2))

    def convertQImageToMat(self, incomingImage):
        '''  Converts a QImage into an opencv MAT format  '''

        incomingImage = incomingImage.convertToFormat(4)

        width = incomingImage.width()
        height = incomingImage.height()

        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
        return arr
    
    def loadMap(self, x, y):
        m = folium.Map(zoom_start=16, location=(x,y))
        m.save(self.data, close_file=False)
        m.save("map.html")

    def initUI(self):
        self.setWindowTitle('Mobile Laser')
        box = QHBoxLayout()
        gb = QGroupBox()
        box.addWidget(gb)

        ccdBox = QVBoxLayout()
        # create a label
        self.ccdLabel = QLabel(self)
        self.ccdLabel.resize(1920, 1080)
        ccdBox.addWidget(self.ccdLabel)
        gb.setLayout(ccdBox)
           
        swirbox = QHBoxLayout()
        gb = QGroupBox()
        swirbox.addWidget(gb)

        swirGpsBox = QVBoxLayout() 
        box.addLayout(swirGpsBox)
        self.swirLabel = QLabel(self)
        self.swirLabel.resize(640, 360)
        swirGpsBox.addWidget(self.swirLabel)
        self.webView = QWebEngineView()
        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.html"))
        self.webView.load(QUrl.fromLocalFile(filepath))
        swirGpsBox.addWidget(self.webView)
        gb.setLayout(swirGpsBox)

        paintBox = QHBoxLayout()
        gb = QGroupBox()
        gb.setFixedHeight(200)
        paintBox.addWidget(gb)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(box)
        vbox.addLayout(paintBox)
        self.setLayout(vbox)             
        self.show()

    def paintEvent(self, event):
        arcwidth = 50       # arc width
        self.painter = QPainter(self)    # create a painter object
        self.painter.setRenderHint(QPainter.Antialiasing)  # tune up painter
        self.painter.setPen(QPen(Qt.green, arcwidth, cap=Qt.FlatCap))
        # 그리기 함수의 호출 부분
        self.drawPoints(self, self.painter)
        self.painter.end() 
    
    def drawPoints(self, event, painter):
        kanvasx = 50        # binding box origin: x
        kanvasy = 650        # binding box origin: y
        kanvasheight = 75  # binding box height
        kanvaswidth = 75   # binding box width
        arcsize = 270       # arc angle between start and end.
        arcwidth = 50       # arc width
        # ---------- the following lines simulate sensor reading. -----------
        if self.arcreading > arcsize or self.arcreading < 0:  # variable to make arc move
            self.adder = -self.adder  # arcreading corresponds to the
            # value to be indicated by the arc.
        self.arcreading = self.arcreading + self.adder
        # --------------------- end simulation ------------------------------
        #print(arcreading)

        # drawArc syntax:
        #       drawArc(x_axis, y_axis, width, length, startAngle, spanAngle)
        painter.drawArc(kanvasx, kanvasy,   # binding box: x0, y0, pixels
                kanvasheight + arcwidth, # binding box: height
                kanvaswidth + arcwidth,  # binding box: width
                int((arcsize + (180 - arcsize) / 2)*16),  # arc start point, degrees (?)
                int(-self.arcreading*16))         # arc span
        painter.drawArc(kanvasx+190, kanvasy,   # binding box: x0, y0, pixels
                kanvasheight + arcwidth, # binding box: height
                kanvaswidth + arcwidth,  # binding box: width
                int((arcsize + (180 - arcsize) / 2)*16),  # arc start point, degrees (?)
                int(-self.arcreading*16))         # arc span
        painter.drawArc(kanvasx+380, kanvasy,   # binding box: x0, y0, pixels
                kanvasheight + arcwidth, # binding box: height
                kanvaswidth + arcwidth,  # binding box: width
                int((arcsize + (180 - arcsize) / 2)*16),  # arc start point, degrees (?)
                int(-self.arcreading*16))         # arc span
        painter.drawArc(kanvasx+570, kanvasy,   # binding box: x0, y0, pixels
                kanvasheight + arcwidth, # binding box: height
                kanvaswidth + arcwidth,  # binding box: width
                int((arcsize + (180 - arcsize) / 2)*16),  # arc start point, degrees (?)
                int(-self.arcreading*16))         # arc span
        painter.drawArc(kanvasx+760, kanvasy,   # binding box: x0, y0, pixels
                kanvasheight + arcwidth, # binding box: height
                kanvaswidth + arcwidth,  # binding box: width
                int((arcsize + (180 - arcsize) / 2)*16),  # arc start point, degrees (?)
                int(-self.arcreading*16))         # arc span
        painter.setFont(QFont('Times New Roman', 24, weight=QFont.Bold))
        painter.setPen(QPen(Qt.black, arcwidth, cap=Qt.FlatCap))
        painter.drawText(kanvasx+40, kanvasy+70, str(int(self.arcreading)))

    def keyPressEvent(self, e):        
        if e.key() == Qt.Key_Right:
            self.x, self.y = self.x, self.y+0.0005
            self.arcreading += 10

        elif e.key() == Qt.Key_Left:
            self.x, self.y = self.x, self.y-0.0005
            self.arcreading -= 10

        elif e.key() == Qt.Key_Up:
            self.x, self.y = self.x+0.0005, self.y
            self.arcreading += 1

        elif e.key() == Qt.Key_Down:
            self.x, self.y = self.x-0.0005, self.y
            self.arcreading -= 1
        
        m = folium.Map(zoom_start=18,location=(self.x, self.y))
        m.save(self.data, close_file=False)
        m.save("map.html")
        self.webView.reload()
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = App()
    sys.exit(app.exec_())