import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow
from qvncwidget import QVNCWidget
#logging.basicConfig(level=logging.DEBUG)  # DEBUG及以上的日志信息都会显示
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setStyleSheet("background: black;")
        self.setWindowTitle("QVNCWidget")

        self.vnc = QVNCWidget(
            parent=self,
            #host="127.0.0.1", port=5905,
            host="10.0.0.8", port=5900,
            readOnly=False
        )

        self.setCentralWidget(self.vnc)

        # you can disable mouse tracking if desired
        self.vnc.setMouseTracking(True)
        self.setAutoFillBackground(True)
        def a():
            while True:
                import time
                time.sleep(1)
                #self.vnc.reconnect()
        import threading
        threading.Thread(target=a).start()
        
        self.vnc.start()
        

    def keyPressEvent(self, ev):
        self.vnc.keyPressEvent(ev)
        return super().keyPressEvent(ev) # in case you need the signal somewhere else in the window

    def keyReleaseEvent(self, ev):
        self.vnc.keyReleaseEvent(ev)
        return super().keyReleaseEvent(ev) # in case you need the signal somewhere else in the window

    def closeEvent(self, ev):
        self.vnc.stop()
        return super().closeEvent(ev)
    
#logging.basicConfig(level=logging.DEBUG)

app = QApplication(sys.argv)
window = Window()
window.resize(800, 600)
window.show()

sys.exit(app.exec_())