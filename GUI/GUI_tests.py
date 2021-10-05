from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QApplication, QMainWindow
from PyQt5 import  QtCore, QtGui
import sys

class application(QMainWindow):
    def __init__(self, xpos = 1100, ypos=300,width=500,height=500,title=None):
        super(application,self).__init__()

        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.title = title


        self.setGeometry(self.xpos, self.ypos, self.width, self.height)
        self.setWindowTitle(self.title)

        self.initUI()

    def initUI(self):
        self.lb1 = QtWidgets.QLabel(self)
        self.lb1.setText("press bt1")
        self.lb1.move(50,50)

        self.bt1 = QtWidgets.QPushButton(self)
        self.bt1.setText("bt1")
        self.bt1.setGeometry((QtCore.QRect(100, 200, 200, 200)))
        self.bt1.move(250, 250)
        self.bt1.clicked.connect(self.commend_bt1)

    def commend_bt1(self):
        self.lb1.setText("bt1 preesd!")
        self.update()

    def update(self):
        self.lb1.adjustSize()



def window():
    app = QApplication(sys.argv)
    win = application()
    win.show()
    sys.exit(app.exec_())

window()