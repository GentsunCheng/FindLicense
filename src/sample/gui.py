from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
import sys


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My PyQt Window")
        self.setGeometry(100, 100, 400, 300)

        # 创建一个 QLabel 用于显示文本
        label = QLabel("Hello, PyQt!", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 创建一个垂直布局，并将 QLabel 放入其中
        layout = QVBoxLayout()
        layout.addWidget(label)

        # 创建一个 QWidget，将布局设置为它的主布局
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # 将 QWidget 设置为主窗口的中央部分
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
