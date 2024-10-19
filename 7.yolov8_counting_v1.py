import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from ultralytics import YOLO
from ultralytics.solutions import ObjectCounter

from gui1 import Ui_MainWindow


class MyLabel(QLabel):
    y0 = 0
    x0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
        print("start cap", self.x0, self.y0)

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
            # print("move", self.x1, self.y1)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        rec = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter.drawRect(rec)


class MainWindow(QMainWindow):
    def __init__(self):  # Show GUI
        super().__init__()
        self.take = False
        self.uic1 = None
        self.lb = None
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.Button_start.clicked.connect(self.draw_rect)
        self.uic.Button_stop.clicked.connect(self.stop_capture_video)

        self.uic.label.setAlignment(QtCore.Qt.AlignTop)

        self.thread = {}

    def mouseReleaseEvent(self, event):
        if self.take:
            new_region = [self.lb.x0, self.lb.y0, self.lb.x1, self.lb.y1]
            self.thread[1].change_data(new_region)

    def draw_rect(self):
        # show rectangle
        self.lb = MyLabel(self.uic.label)  # call function of paintEvent
        self.lb.setGeometry(QRect(0, 0, 700, 500))  # limit of rectangle and set up geometry
        self.lb.setCursor(Qt.CrossCursor)  # change type of mouse cursor
        self.lb.show()
        self.take = True

        # start counting
        self.start_capture_video()

    def start_capture_video(self):
        self.thread[1] = live_stream(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_webcam)

    def stop_capture_video(self):
        self.thread[1].stop_app()

    def show_webcam(self, cv_img):
        label_w = self.uic.label.width()
        label_h = self.uic.label.height()
        print("label", label_w, label_h)
        qt_img = self.convert_cv_qt(cv_img, label_w, label_h)
        self.uic.label.setScaledContents(False)
        self.uic.label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img, label_w, label_h):
        rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_img.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(label_w, label_h, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class live_stream(QThread):
    signal = pyqtSignal(object)

    def __init__(self, index):
        self.end_point = None
        self.start_point = None
        self.region_points = None
        self.stop = False
        self.index = index
        print("Starting threading: ", self.index)
        super(live_stream, self).__init__()

    def run(self):
        model = "yolo11n.pt"
        cap = cv2.VideoCapture("video1.mp4")
        assert cap.isOpened(), "Error reading video file"
        # w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
        # print("w, h", w, h)

        # Define region points
        self.region_points = [(300, 400), (1280, 404), (1280, 360), (300, 360)]

        # Init Object Counter
        counter = ObjectCounter(show=False,
                                region=self.region_points,
                                model=model)

        while cap.isOpened():
            success, im0 = cap.read()
            if not success:
                print("Video frame is empty or video processing has been successfully completed.")
                break
            im1 = counter.count(im0)

            # draw rectangle
            color = (255, 0, 0)
            thickness = 2
            start_point = self.region_points[3]
            end_point = self.region_points[1]
            image = cv2.rectangle(im1, start_point, end_point, color, thickness)

            self.signal.emit(image)
            if self.stop:
                break

        cap.release()
        cv2.destroyAllWindows()

    def change_data(self, new_region):
        pos_1 = (int(new_region[0] * 1.95), int(new_region[3] * 1.53 * 1.27))
        pos_2 = (int(new_region[2] * 1.95), int(new_region[3] * 1.53 * 1.27))
        pos_3 = (int(new_region[2] * 1.95), int(new_region[1] * 1.53 * 1.27))
        pos_4 = (int(new_region[0] * 1.95), int(new_region[1] * 1.53 * 1.27))

        self.region_points = [pos_1, pos_2, pos_3, pos_4]
        print("self.region_points", self.region_points)

    def stop_app(self):
        print("stop")
        self.stop = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
