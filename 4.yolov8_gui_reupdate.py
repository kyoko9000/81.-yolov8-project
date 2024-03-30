import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from ultralytics import YOLO

from gui1 import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):  # Show GUI
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.uic.Button_start.clicked.connect(self.start_capture_video)
        self.uic.Button_stop.clicked.connect(self.stop_capture_video)
        self.thread = {}

    def closeEvent(self, event):  # click button stop
        self.stop_capture_video()

    def start_capture_video(self):
        self.thread[1] = live_stream(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_webcam)

    def stop_capture_video(self):
        self.thread[1].stop_app()

    def show_webcam(self, cv_img):
        qt_img = convert_cv_qt(cv_img)
        self.uic.label.setPixmap(qt_img)


def convert_cv_qt(cv_img):
    rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_img.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_img.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(651, 321, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)


class live_stream(QThread):
    signal = pyqtSignal(np.ndarray)

    def __init__(self, index):
        self.stop = False
        self.index = index
        print("Starting threading: ", self.index)
        super(live_stream, self).__init__()

    def run(self):
        # model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
        # results = model('video1.mp4', stream=True)  # List of Results objects
        # for result in results:
        #     # self.signal.emit(result.orig_img)
        #     self.signal.emit(result.plot())
            # if result:
            #     boxes = result[0].boxes.numpy()  # Boxes object for bbox outputs
            #     for box in boxes:  # there could be more than one detection
            #         print("class", box.cls)

        # Load the YOLOv8 model
        model = YOLO('yolov8n.pt')

        # Open the video file
        cap = cv2.VideoCapture("video1.mp4")

        # Loop through the video frames
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:
                # Run YOLOv8 inference on the frame
                results = model(frame)

                for result in results:
                    # self.signal.emit(result.orig_img)
                    self.signal.emit(result.plot())
                    # if result:
                    #     boxes = result[0].boxes.numpy()  # Boxes object for bbox outputs
                    #     for box in boxes:  # there could be more than one detection
                    #         print("class", box.cls)

            # Break the loop if 'q' is pressed
            if self.stop:
                break

        # Release the video capture object and close the display window
        cap.release()
        cv2.destroyAllWindows()

    def stop_app(self):
        print("stop")
        self.stop = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
