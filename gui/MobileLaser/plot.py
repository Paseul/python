import sys, random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.arcreading = 270
        self.adder = 0.1
        
    def initUI(self):      
        self.setGeometry(300, 300, 1800, 400)
        self.setWindowTitle('QPainter를 이용한 그래픽스')
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
        kanvasy = 50        # binding box origin: y
        kanvasheight = 100  # binding box height
        kanvaswidth = 100   # binding box width
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
        painter.drawArc(kanvasx+300, kanvasy,   # binding box: x0, y0, pixels
                kanvasheight + arcwidth, # binding box: height
                kanvaswidth + arcwidth,  # binding box: width
                int((arcsize + (180 - arcsize) / 2)*16),  # arc start point, degrees (?)
                int(-self.arcreading*16))         # arc span
        painter.drawArc(kanvasx+600, kanvasy,   # binding box: x0, y0, pixels
                kanvasheight + arcwidth, # binding box: height
                kanvaswidth + arcwidth,  # binding box: width
                int((arcsize + (180 - arcsize) / 2)*16),  # arc start point, degrees (?)
                int(-self.arcreading*16))         # arc span
        painter.drawArc(kanvasx+900, kanvasy,   # binding box: x0, y0, pixels
                kanvasheight + arcwidth, # binding box: height
                kanvaswidth + arcwidth,  # binding box: width
                int((arcsize + (180 - arcsize) / 2)*16),  # arc start point, degrees (?)
                int(-self.arcreading*16))         # arc span
        painter.drawArc(kanvasx+1200, kanvasy,   # binding box: x0, y0, pixels
                kanvasheight + arcwidth, # binding box: height
                kanvaswidth + arcwidth,  # binding box: width
                int((arcsize + (180 - arcsize) / 2)*16),  # arc start point, degrees (?)
                int(-self.arcreading*16))         # arc span
        

    def keyPressEvent(self, e):        
        if e.key() == Qt.Key_Right:
            self.arcreading += 10                             

        elif e.key() == Qt.Key_Left:
            self.arcreading -= 10

        elif e.key() == Qt.Key_Up:
            self.arcreading += 1

        elif e.key() == Qt.Key_Down:
            self.arcreading -= 1
        self.update() 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())