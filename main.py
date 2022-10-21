import sys
from PyQt5.QtWidgets import QApplication, QPushButton
from Windows import BaseWindow


class MainWindow(BaseWindow):
    def initButton(self):
        btn = QPushButton("Начать расчёт", self)


def main():
    app = QApplication(sys.argv)
    form = MainWindow("Входная точка", size=[300, 300], locate="в центр")
    form.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()