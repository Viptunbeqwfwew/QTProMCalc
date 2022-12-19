import sys
from PyQt5.QtWidgets import QApplication
from BaseElement import BaseWindow, BaseButton, BaseWindowError


class MainWindow(BaseWindow):
    def Error(self):
        if self.MSE.isHidden():
            self.MSE.show()
        else:
            self.MSE.btn.show()
        self.MSE.setFunctionError(lambda: (self.MSE.btn.hide(), self.btn.show()))
        self.btn.hide()

    def initButton(self):
        self.btn = BaseButton(self, "Старт", locate="центр")
        self.btn.clicked.connect(self.Error)

    def initWindows(self):
        self.MSE = BaseWindowError("Error", locate="center", size=[250, 100])


def main():
    app = QApplication(sys.argv)
    form = MainWindow("Входная точка", size=[400, 300], locate="центр")
    form.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()