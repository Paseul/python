import sys
import io
import os
import folium # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from PyQt5.QtCore import Qt, QUrl

"""
Folium in PyQt5
"""
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 480, 480
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.x = 37.40494
        self.y = 127.11130
        m = folium.Map(
        	# tiles='Stamen Terrain',
        	zoom_start=18,
        	location=(self.x, self.y)
        )

        # save map data to data object
        self.data = io.BytesIO()
        m.save(self.data, close_file=False)
        m.save("map.html")

        self.webView = QWebEngineView()
        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.html"))
        self.webView.load(QUrl.fromLocalFile(filepath))
        layout.addWidget(self.webView)
    
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
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')