# ************************** tool check labeling v1.0 *************************
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QFont
# pip install pyqt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from gui2 import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.count_2 = None
        self.count_1 = None
        self.max_objects = None
        self.index = 0
        self.link = None
        self.file_link = None
        self.origin_image = None
        self.image = None

        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.pushButton.clicked.connect(self.load_link)
        self.uic.pushButton_3.clicked.connect(self.next)
        self.uic.pushButton_5.clicked.connect(self.back)

        # -------------- adjust objects ---------------
        self.uic.pushButton_3.setText("Next")
        self.uic.pushButton_5.setText("Back")
        self.uic.pushButton_2.setText("--")
        self.uic.pushButton_4.setText("--")

    def load_link(self):
        # hiển thị cửa sổ chọn của pyqt5 tự vẽ, thay vì cửa sổ chọn mặc định của window
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Hiển thị cửa sổ chọn tệp
        self.link, _ = QFileDialog.getOpenFileNames(self, "Chọn ảnh", "", "Images (*.png *.jpg *.bmp)",
                                                    options=options)

        # đếm tổng số hình đã mở
        self.max_objects = len(self.link)
        self.uic.lineEdit.setText(str(self.max_objects))
        self.open_pic()

    def open_pic(self):
        self.file_link = self.link[self.index]

        if self.file_link:
            print(self.file_link)
            # loading image
            self.origin_image = QPixmap(self.file_link)
            self.uic.label.setScaledContents(False)
            w = self.uic.label.width()
            h = self.uic.label.height()
            self.image = self.origin_image.scaled(w, h, Qt.KeepAspectRatio)
            self.uic.label.setFrameShape(QtWidgets.QFrame.Box)  # tạo viền màu đen
            self.uic.label.setPixmap(self.image)

            # vẽ bounding box
            self.bounding_box()

    def bounding_box(self):
        # lấy ra tên file trong link
        name = self.file_link.split("/")[-1][:-4]
        # loại bỏ tên file và folder chứa file trong link
        root_link_split = self.file_link.split("/")[:-3]
        # link folder gốc
        root_link = "/".join(root_link_split)
        # đường link đến file txt
        link_file_txt = f"{root_link}/labels/train2017/{name}.txt"
        print("check", link_file_txt)
        try:
            # Đọc từ tệp văn bản
            with open(link_file_txt, 'r') as file:
                lines = file.readlines()
            # Loại bỏ ký tự xuống dòng (newline) từ mỗi dòng
            lines = [line.strip() for line in lines]

            # Tạo danh sách 2D từ dữ liệu đã đọc
            matrix_2d = [list(map(float, line.split())) for line in lines]

            # In danh sách 2D
            # print("matrix_2d", matrix_2d)

            # chuyển tọa độ dạng % sang tọa độ dạng số
            point_list = self.change_percent_to_point(matrix_2d)

            # vẽ hình chữ nhật lên hình
            self.draw_rectangle(point_list)
        except:
            pass
        # vẽ lại pixmap
        self.uic.label.setPixmap(self.image)

    def change_percent_to_point(self, matrix_2d):
        w = self.image.width()
        h = self.image.height()
        point_list = [[i[0], (i[1] - i[3] / 2) * w, (i[2] - i[4] / 2) * h, i[3] * w, i[4] * h] for i in matrix_2d]
        return point_list

    def draw_rectangle(self, matrix_2d):
        # Vẽ hình chữ nhật lên label
        painter = QPainter(self.image)
        pen = QPen(QColor(255, 0, 0))  # Màu đỏ
        pen.setWidth(2)
        painter.setPen(pen)
        # draw rectangle
        for i in matrix_2d:
            p = list(map(int, i))
            painter.drawRect(p[1], p[2], p[3], p[4])  # Vẽ hình chữ nhật (x, y, width, height)

        # draw class number objects in list
        for i in matrix_2d:
            if i:
                font = QFont('Arial', 15)
                painter.setFont(font)
                painter.setPen(QColor(0, 0, 255))
                painter.drawText(int(i[1]), int(i[2])+18, f'{int(i[0])}')
        painter.end()

    def next(self):
        self.count_1 = int(self.uic.lineEdit.text())
        if self.count_1 < self.max_objects:
            self.count_1 += 1
            self.uic.lineEdit.setText(str(self.count_1))

            # cập nhật index
            self.index = self.count_1-1
            print(self.index)
            # load ảnh mới
            self.open_pic()

    def back(self):
        self.count_2 = int(self.uic.lineEdit.text())
        if self.count_2 > 1:
            self.count_2 -= 1
            self.uic.lineEdit.setText(str(self.count_2))

            # cập nhật index
            self.index = self.count_2-1
            print(self.index)
            # load ảnh mới
            self.open_pic()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
