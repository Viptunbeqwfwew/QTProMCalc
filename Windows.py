from PyQt5.QtWidgets import QWidget, QPushButton
from win32api import GetSystemMetrics


class BaseWindow(QWidget):
    def __init__(self, title, **kwargs):
        super().__init__()
        self.initUI(title, kwargs.get("size"), kwargs.get("locate"))
        self.initButton()

    def initUI(self, title, size, locate):
        if size is None or len(size) != 2:
            size = [300, 300]
        self.setGeometry(*self.locate_calc(locate, *size), *size)
        self.setWindowTitle(title)

    def locate_calc(self, locate, *size):
        if type(locate) == type(tuple()) or type(locate) == type(list()):
            return locate
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        locates = {}
        locates_rus = {"центр": self._cordsCenter,
                       "сверху": self._cordsTop,
                       "снизу": self._cordsBottom,
                       "справа": self._cordsLeft,
                       "слева": self._cordsRight}
        locates_eng = {"center": self._cordsCenter,
                       "top": self._cordsTop,
                       "bottom": self._cordsBottom,
                       "left": self._cordsLeft,
                       "right": self._cordsRight}
        locates.update(locates_eng), locates.update(locates_rus)
        if locate in locates:
            func = locates[locate]
        else:
            return 0, 0
        return func(width, height, *size)

    def _cordsBottom(self, w, h, *s):
        return (w - s[0]) // 2, h - s[1]

    def _cordsTop(self, w, h, *s):
        return (w - s[0]) // 2, 45

    def _cordsCenter(self, w, h, *s):
        return (w - s[0]) // 2, (h - s[1]) // 2

    def _cordsLeft(self, w, h, *s):
        return 0, (h - s[1]) // 2

    def _cordsRight(self, w, h, *s):
        return w - s[0], (h - s[1]) // 2

    def initButton(self):
        pass
