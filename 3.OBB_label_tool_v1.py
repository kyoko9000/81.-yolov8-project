# ************************** man hinh loai 2 *************************
import math
import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPolygon, QPixmap, QPen, QFont, QColor
# pip install pyqt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QFileDialog
from gui2 import Ui_MainWindow
from gui1 import Ui_MainWindow as sub_form


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.check = False
        self.percent_list = []
        self.origin_image = None
        self.result = None
        self.file_link = None
        self.uic1 = None
        self.sub_win = None
        self.image = None
        self.x11 = None
        self.y11 = None
        self.y00 = None
        self.x00 = None
        self.qp = None
        self.rotation_angle = None
        self.draw = False
        self.y1 = None
        self.x1 = None
        self.y0 = None
        self.x0 = None
        self.start = False
        self.top_left = []
        self.top_right = []
        self.bottom_left = []
        self.bottom_right = []

        self.new_top_left = []
        self.new_top_right = []
        self.new_bottom_left = []
        self.new_bottom_right = []
        self.list_point = [[]]
        self.list_clas = []

        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.pushButton.clicked.connect(self.load_image)
        self.uic.pushButton_2.clicked.connect(self.start_draw)
        self.uic.pushButton_5.clicked.connect(self.add_rec)
        self.uic.pushButton_3.clicked.connect(self.delete_rec)
        self.uic.pushButton_4.clicked.connect(self.export_yolo)

        self.uic.lineEdit.setText("0")

        #  ===================== resize section =======================
        # resize gui
        self.resize(700, 800)
        # resize and change align label
        self.uic.label.setAlignment(QtCore.Qt.AlignTop)
        self.uic.label.setGeometry(QtCore.QRect(0, 0, 650, 400))
        # resize lineedit
        self.uic.lineEdit.setGeometry(QtCore.QRect(210, 430, 100, 51))

        #  ===================== add section ==========================
        # add lineedit 1
        self.lineEdit1 = QtWidgets.QLineEdit(self.uic.centralwidget)
        self.lineEdit1.setGeometry(QtCore.QRect(350, 430, 100, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit1.setFont(font)
        self.lineEdit1.setObjectName("lineEdit1")

        # add lineedit 2
        self.lineEdit2 = QtWidgets.QLineEdit(self.uic.centralwidget)
        self.lineEdit2.setGeometry(QtCore.QRect(500, 430, 100, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit2.setFont(font)
        self.lineEdit2.setObjectName("lineEdit2")
        self.lineEdit2.setText("0")

        # add slider
        self.slider = QSlider(self.uic.centralwidget)
        self.slider.setGeometry(QtCore.QRect(80, 600, 250, 30))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        # Set the minimum and maximum values of the slider to 0 and 360 degrees, respectively
        self.slider.setMinimum(-90)
        self.slider.setMaximum(90)
        # Set the initial value of the slider to 0 degrees
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.change_angle)

        # add slider1
        self.slider1 = QSlider(self.uic.centralwidget)
        self.slider1.setGeometry(QtCore.QRect(80, 650, 250, 30))
        self.slider1.setOrientation(QtCore.Qt.Horizontal)
        # Set the minimum and maximum values of the slider to 0 and 360 degrees, respectively
        self.slider1.setMinimum(-180)
        self.slider1.setMaximum(180)
        # Set the initial value of the slider to 0 degrees
        self.slider1.setValue(0)
        self.slider1.valueChanged.connect(self.left)

        # add slider2
        self.slider2 = QSlider(self.uic.centralwidget)
        self.slider2.setGeometry(QtCore.QRect(80, 700, 250, 30))
        self.slider2.setOrientation(QtCore.Qt.Horizontal)
        # Set the minimum and maximum values of the slider to 0 and 360 degrees, respectively
        self.slider2.setMinimum(-180)
        self.slider2.setMaximum(180)
        # Set the initial value of the slider to 0 degrees
        self.slider2.setValue(0)
        self.slider2.valueChanged.connect(self.top)

        # add slider3
        self.slider3 = QSlider(self.uic.centralwidget)
        self.slider3.setGeometry(QtCore.QRect(440, 650, 250, 30))
        self.slider3.setOrientation(QtCore.Qt.Horizontal)
        # Set the minimum and maximum values of the slider to 0 and 360 degrees, respectively
        self.slider3.setMinimum(-180)
        self.slider3.setMaximum(180)
        # Set the initial value of the slider to 0 degrees
        self.slider3.setValue(0)
        self.slider3.valueChanged.connect(self.right)

        #  add slider4
        self.slider4 = QSlider(self.uic.centralwidget)
        self.slider4.setGeometry(QtCore.QRect(440, 700, 250, 30))
        self.slider4.setOrientation(QtCore.Qt.Horizontal)
        # Set the minimum and maximum values of the slider to 0 and 360 degrees, respectively
        self.slider4.setMinimum(-180)
        self.slider4.setMaximum(180)
        # Set the initial value of the slider to 0 degrees
        self.slider4.setValue(0)
        self.slider4.valueChanged.connect(self.bottom)

        # add label2
        self.label2 = QtWidgets.QLabel(self.uic.centralwidget)
        self.label2.setGeometry(QtCore.QRect(10, 590, 100, 30))
        self.label2.setText("angel")
        self.label2.setFont(font)

        # add label3
        self.label3 = QtWidgets.QLabel(self.uic.centralwidget)
        self.label3.setGeometry(QtCore.QRect(10, 650, 100, 30))
        self.label3.setText("left")
        self.label3.setFont(font)

        # add label4
        self.label4 = QtWidgets.QLabel(self.uic.centralwidget)
        self.label4.setGeometry(QtCore.QRect(10, 700, 100, 30))
        self.label4.setText("top")
        self.label4.setFont(font)

        # add label5
        self.label5 = QtWidgets.QLabel(self.uic.centralwidget)
        self.label5.setGeometry(QtCore.QRect(350, 650, 100, 30))
        self.label5.setText("right")
        self.label5.setFont(font)

        # add label6
        self.label6 = QtWidgets.QLabel(self.uic.centralwidget)
        self.label6.setGeometry(QtCore.QRect(350, 700, 100, 30))
        self.label6.setText("bottom")
        self.label6.setFont(font)

        # add pushbutton_6
        self.pushButton_6 = QtWidgets.QPushButton(self.uic.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(20, 410, 101, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setText("Test")
        self.pushButton_6.clicked.connect(self.sub_gui)

    def export_yolo(self):
        self.check = True
        self.number_change_to_percent()
        print("export recs")
        link = self.file_link
        name = link.split("/")[-1][:-4]
        clas = self.list_clas
        mylist = self.percent_list
        with open(f'labels/{name}.txt', 'w') as f:
            for i in range(len(mylist)):
                s = mylist[i]
                if len(s) == 0:
                    continue
                OBB = map(str, mylist[i].reshape(-1).tolist())
                f.write(f'{clas[i]} ' + ' '.join(OBB) + '\n')
            print(f'save at labels/{name}.txt')

    def number_change_to_percent(self):
        print("number change to percent")
        image_w = self.origin_image.width()
        image_h = self.origin_image.height()
        # print("w", image_w, "h", image_h)

        # # Chuyển danh sách thành mảng NumPy
        # numpy_list = np.array(self.result)
        #
        # # Lấy tọa độ x (phần tử thứ 1) và nhân với 2
        # l1 = np.round(((numpy_list[..., 0])/image_w), 4)
        #
        # # Lấy tọa độ y (phần tử thứ 2)
        # l2 = np.round(((numpy_list[..., 1])/image_h), 4)
        #
        # # Ghép l1 và l2 để tạo danh sách mới
        # self.percent_list = np.stack((l1, l2), axis=-1)
        # print("Danh sách mới:")
        # print(self.percent_list)
        a = []
        print("self.result", self.result)
        for i in self.result:
            # multiplied_sublist = [[int(element[0] / 1.3), int(element[1] / 1.3)] for element in sublist]
            # result_list.append(multiplied_sublist)
            coordinates_list = []
            for coordinates in i:
                coordinates_list.append([(coordinates[0] / image_w), (coordinates[1] / image_h)])
            a.append(coordinates_list)
        self.percent_list = np.round(np.array(a), 4)

    def delete_rec(self):
        self.list_point = [[]]
        self.list_clas = []
        print("delete recs", self.list_point)
        print("delete clas", self.list_clas)

    def load_image(self):
        # hiển thị cửa sổ chọn của pyqt5 tự vẽ, thay vì cửa sổ chọn mặc định của window
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Hiển thị cửa sổ chọn tệp
        self.file_link, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Images (*.png *.jpg *.bmp)",
                                                        options=options)

        if self.file_link:
            # loading image
            self.origin_image = QPixmap(self.file_link)
            self.uic.label.setScaledContents(False)
            w = self.uic.label.width()
            h = self.uic.label.height()
            self.image = self.origin_image.scaled(w, h, Qt.KeepAspectRatio)
            self.uic.label.setFrameShape(QtWidgets.QFrame.Box)  # tạo viền màu đen
            self.uic.label.setPixmap(self.image)

    def change_angle(self, data):
        if self.start:
            self.uic.lineEdit.setText(str(data))
            self.math_point()

    def left(self, number):
        if self.start:
            self.x0 = self.x00 + number
            print(self.x0, number)
            self.math_point()

    def top(self, number):
        if self.start:
            self.y0 = self.y00 - number
            self.math_point()

    def right(self, number):
        if self.start:
            self.x1 = self.x11 + number
            self.math_point()

    def bottom(self, number):
        if self.start:
            self.y1 = self.y11 + number
            self.math_point()

    def start_draw(self):
        # signal for event capture coordinates
        self.start = True

    def mousePressEvent(self, event):
        if self.start:
            self.x0 = event.x()
            self.y0 = event.y()
            self.x00 = self.x0
            self.y00 = self.y0
            # print("start cap", self.x0, self.y0)

    def mouseMoveEvent(self, event):
        if self.start:
            self.x1 = event.x()
            self.y1 = event.y()
            self.x11 = self.x1
            self.y11 = self.y1
            self.update()
            # print("x1:", self.x1, "y1:", self.y1)
            self.draw = True
            self.math_point()

    def mouseReleaseEvent(self, a0):
        if self.start:
            self.slider1.setValue(0)
            self.slider2.setValue(0)
            self.slider3.setValue(0)
            self.slider4.setValue(0)

    def paintEvent(self, event):
        if self.draw:
            pixmap = QPixmap(self.image)
            # pixmap.fill(Qt.transparent) # use when draw pixmap on other label or clear previous pixmap
            self.qp = QPainter(pixmap)
            pen = QPen(Qt.blue, 3, Qt.SolidLine)
            self.qp.setPen(pen)
            self.draw_polygon()
            self.uic.label.setPixmap(pixmap)
            self.qp.end()

    def math_point(self):
        self.top_left = (self.x0, self.y0)
        self.top_right = (self.x1, self.y0)
        self.bottom_left = (self.x0, self.y1)
        self.bottom_right = (self.x1, self.y1)

        self.rotation_angle = int(self.uic.lineEdit.text())
        # Tọa độ tâm (175, 175)
        center = (((self.top_right[0] - self.top_left[0]) / 2) + self.x0,
                  ((self.bottom_right[1] - self.top_right[1]) / 2) + self.y0)

        # Tính toán tọa độ mới sau khi quay
        self.new_top_left = self.rotate_point(self.top_left, center, self.rotation_angle)
        self.new_top_right = self.rotate_point(self.top_right, center, self.rotation_angle)
        self.new_bottom_left = self.rotate_point(self.bottom_left, center, self.rotation_angle)
        self.new_bottom_right = self.rotate_point(self.bottom_right, center, self.rotation_angle)

    def add_rec(self):
        # clean empty data in list
        self.list_point = list(filter(None, self.list_point))
        # list of all rectangle position after done draw
        if self.start:
            self.list_clas.append(int(self.lineEdit2.text()))
            self.list_point.append([self.new_bottom_left, self.new_bottom_right, self.new_top_right, self.new_top_left])

            print("list point", self.list_point)
            print("list clas", self.list_clas)

            # count_1 object in list
            num_object = len(self.list_point)
            self.lineEdit1.setText(str(num_object))

            # convert list point size to origin image size
            image_w = self.origin_image.width()
            image_h = self.origin_image.height()
            label_w = 650
            label_h = 400
            ratio_h = label_h / image_h  # tính theo cạnh nào của hình, bằng cạnh của label sau khi load ảnh lên label
            self.result = self.multiply_elements_in_nested_list(ratio_h, self.list_point)
            print("Danh sách sau khi nhân:")
            print("self.result", self.result)

            # reset angel
            self.slider.setValue(0)

    def multiply_elements_in_nested_list(self, ratio_h, list):
        result_list = []
        for sublist in list:
            multiplied_sublist = [[int(element[0] / ratio_h), int(element[1] / ratio_h)] for element in sublist]
            result_list.append(multiplied_sublist)
        return result_list

    def rotate_point(self, point, center, angle_degrees):
        # Chuyển đổi góc từ độ sang radian
        angle_radians = math.radians(angle_degrees)

        # Tính toán tọa độ mới sau khi quay
        x, y = point
        cx, cy = center
        new_x = (x - cx) * math.cos(angle_radians) - (y - cy) * math.sin(angle_radians) + cx
        new_y = (x - cx) * math.sin(angle_radians) + (y - cy) * math.cos(angle_radians) + cy
        # print((x - cx), math.cos(angle_radians), (x - cx) * math.cos(angle_radians),
        #       (y - cy), math.sin(angle_radians), (y - cy) * math.sin(angle_radians))

        return int(new_x), int(new_y)

    def draw_polygon(self):
        # draw polygon by mouse event
        points = QPolygon([
            QPoint(int(self.new_top_left[0]), int(self.new_top_left[1])),  # Điểm thứ nhất
            QPoint(int(self.new_top_right[0]), int(self.new_top_right[1])),  # Điểm thứ hai
            QPoint(int(self.new_bottom_right[0]), int(self.new_bottom_right[1])),  # Điểm thứ ba
            QPoint(int(self.new_bottom_left[0]), int(self.new_bottom_left[1]))  # Điểm thứ tư
        ])
        self.qp.drawPolygon(points)

        # draw all polygon in the self.list_point
        for i in self.list_point:
            if i:
                self.qp.setPen(QPen(Qt.red, 3, Qt.SolidLine))
                self.qp.drawLine(QPoint(int(i[0][0]), int(i[0][1])), QPoint(int(i[1][0]), int(i[1][1])))
                self.qp.drawLine(QPoint(int(i[1][0]), int(i[1][1])), QPoint(int(i[2][0]), int(i[2][1])))
                self.qp.drawLine(QPoint(int(i[2][0]), int(i[2][1])), QPoint(int(i[3][0]), int(i[3][1])))
                self.qp.drawLine(QPoint(int(i[3][0]), int(i[3][1])), QPoint(int(i[0][0]), int(i[0][1])))

        # draw number count_1 objects in list
        for No, i in enumerate(self.list_point):
            if i:
                font = QFont('Arial', 15)
                self.qp.setFont(font)
                self.qp.setPen(QColor(255, 255, 0))
                self.qp.drawText(int(i[0][0]), int(i[0][1]), f'{No + 1}')

        # draw number class objects in list
        for No, i in enumerate(self.list_point):
            if i:
                font = QFont('Arial', 15)
                self.qp.setFont(font)
                self.qp.setPen(QColor(0, 0, 255))
                self.qp.drawText(int(i[2][0]), int(i[2][1]), f'{self.list_clas[No]}')

    # ==================== sub window section ========================
    def sub_gui(self):
        self.sub_win = QMainWindow()
        self.uic1 = sub_form()
        self.uic1.setupUi(self.sub_win)
        self.sub_win.show()

        self.uic1.label.setGeometry(QtCore.QRect(0, 0, 650, 400))
        self.uic1.label.setAlignment(QtCore.Qt.AlignTop)

        self.uic1.Button_start.clicked.connect(self.cv2_show)

    def cv2_show(self):
        if self.check:
            print("run sub gui")
            # chuyển từ tọa độ dạng % sang tọa độ dạng số
            convert_list = self.convert_percent_to_number()
            # Đường dẫn tới tệp tin hình ảnh
            print("convert list", convert_list)
            image_path = self.file_link

            # Sử dụng phương thức imread để đọc hình ảnh từ tệp tin.
            image = cv2.imread(image_path)

            # draw rectangle
            color = (255, 0, 0)
            thickness = 2

            for i in convert_list:
                image = cv2.line(image, i[0], i[1], color, thickness)
                image = cv2.line(image, i[1], i[2], color, thickness)
                image = cv2.line(image, i[2], i[3], color, thickness)
                image = cv2.line(image, i[3], i[0], color, thickness)

                self.show_webcam(image)
        else:
            self.uic1.label.setText("not export")
            font = QtGui.QFont()
            font.setPointSize(40)
            self.uic1.label.setFont(font)

    def convert_percent_to_number(self):
        image_w = self.origin_image.width()
        image_h = self.origin_image.height()
        print("convert percent to number")
        print("self.percent_list", self.percent_list)
        convert_list = []
        for sublist in self.percent_list:
            multiplied_sublist = [[int(element[0] * image_w), int(element[1] * image_h)] for element in sublist]
            convert_list.append(multiplied_sublist)
        print("self.result", self.result)
        return convert_list

    def show_webcam(self, cv_img):
        label_w = self.uic1.label.width()
        label_h = self.uic1.label.height()
        qt_img = self.convert_cv_qt(cv_img, label_w, label_h)
        self.uic1.label.setScaledContents(False)
        self.uic1.label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img, label_w, label_h):
        rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_img.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(label_w, label_h, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
