import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from win32api import GetSystemMetrics


class BaseWindow(QWidget):
    def __init__(self, title, **kwargs):
        super().__init__()
        self.initUI(title, kwargs.get("size"))
        self.initButton()

    def initUI(self, title, size):
        if size is None or len(size) != 4:
            size = [300, 300, 900, 600]
        self.setGeometry(*size)
        self.setWindowTitle(title)

    def initButton(self):
        pass


class MainWindow(BaseWindow):
    def initButton(self):
        btn = QPushButton("Начать расчёт", self)


def main():
    width = GetSystemMetrics(0) * 1.5
    height = GetSystemMetrics(1) * 1.5
    print(width, height)
    app = QApplication(sys.argv)
    form = MainWindow("Входная точка", size=[(width - 300) // 2, (height - 300) // 2, 300, 300])
    form.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()