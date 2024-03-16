import sys
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class MeinWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(200, 50, 300, 300)
        self.pen1 = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self.pen2 = QtGui.QPen(QtGui.QColor(255, 0, 0))
        self.pen3 = QtGui.QPen(QtGui.QColor(0, 255, 0))
        self.pen4 = QtGui.QPen(QtGui.QColor(0, 0, 255))
        self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))

        self.pens = (self.pen1, self.pen2, self.pen3, self.pen4)
        self.rw = 100
        self.rh = 50

        self.label = QLabel(self)
        self.label.setGeometry(200, 50, 300, 300)
        pixmap = QPixmap("plane.jpg")  # Đường dẫn đến tệp hình ảnh
        self.label.setPixmap(pixmap)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.translate(QtCore.QPointF(self.rw, self.rh))  # move rotation center to an arbitrary point of widget
        angle = 10
        for i in range(0, len(self.pens)):
            dy = self.rh - self.rh * math.cos(math.radians(angle))  # vertical offset of bottom left corner
            dx = self.rh * math.sin(math.radians(angle))  # horizontal offset of bottom left corner
            p = self.pens[i]
            p.setWidth(3)
            painter.setPen(p)
            painter.drawRect(0, 0, self.rw, self.rh)
            painter.translate(QtCore.QPointF(dx, dy))  # move the wanted rotation center to old position
            painter.rotate(angle)
            angle += 20


app = QtWidgets.QApplication(sys.argv)
widget = MeinWidget()
widget.show()
sys.exit(app.exec_())
