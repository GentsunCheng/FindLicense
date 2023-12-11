import os
import sys
import cv2
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("车牌识别")
        self.setGeometry(100, 100, 1280, 720)

        self.BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../source/"))
        self.num = "未识别到车牌号"
        self.im = cv2.imread(os.path.join(self.BASE_PATH, "load.png"), 1)

        # 创建一个 QLabel 用于显示图片
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 创建一个 QLabel 用于显示文本
        self.text_label = QLabel(self.num, self)
        font = self.text_label.font()
        font.setPointSize(16)
        self.text_label.setFont(font)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 创建一个垂直布局，并将两个 QLabel 放入其中
        layout = QVBoxLayout()
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_label, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_gui(self, image, num):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
        self.text_label.setText(num)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Q:
            self.close()
            QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
