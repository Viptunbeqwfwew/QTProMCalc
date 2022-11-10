from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton
from win32api import GetSystemMetrics


class BaseUnit:
    def locate_element(self, locate, *size, funch=int):
        if type(locate) == type(tuple()) or type(locate) == type(list()):
            return locate
        width = funch(0)
        height = funch(1)
        locates = {}
        locates_rus = {"центр": self._Center,
                       "верху": self._Top,
                       "внизу": self._Bottom,
                       "права": self._Left,
                       "лева": self._Right}
        locates_eng = {"center": self._Center,
                       "top": self._Top,
                       "bottom": self._Bottom,
                       "left": self._Left,
                       "right": self._Right}
        locates.update(locates_eng), locates.update(locates_rus)
        if locate in locates:
            func = locates[locate]
        else:
            return 0, 0
        return func(width, height, *size)

    def _Bottom(self, w, h, *s):
        return (w - s[0]) // 2, h - s[1]

    def _Top(self, w, h, *s):
        return (w - s[0]) // 2, 45

    def _Center(self, w, h, *s):
        return (w - s[0]) // 2, (h - s[1]) // 2

    def _Left(self, w, h, *s):
        return 0, (h - s[1]) // 2

    def _Right(self, w, h, *s):
        return w - s[0], (h - s[1]) // 2


class BaseWindow(QWidget, BaseUnit):
    def __init__(self, title, **kwargs):
        super().__init__()
        self.initUI(title, kwargs.get("size"), kwargs.get("locate"))
        self.initButton()
        self.initWindows()

    def initUI(self, title, size, locate):
        if size is None or len(size) != 2:
            size = [300, 300]
        self.setGeometry(*self.locate_element(locate, *size, funch=GetSystemMetrics), *size)
        self.setWindowTitle(title)

    def setGeometry(self, *cord):
        super().setGeometry(*cord)

    def initButton(self):
        pass

    def size(self):
        """size() возвращает кортедж размера ({ширина}, {высота})"""
        return super().size().width(), super().size().height()

    def initWindows(self):
        pass


class BaseButton(QPushButton, BaseUnit):
    def __init__(self, window, title: str, **kwargs):
        self.window = window
        super().__init__(title, window)
        self.initUI(kwargs.get("size"), kwargs.get("locate"))

    def getSizeWindow(self, i):
        return self.window.size()[i]

    def size(self):
        return super().size().width(), super().size().height()

    def initUI(self, size, locate):
        if size is None or len(size) != 2:
            size = [70, 35]
        self.setGeometry(*self.locate_element(locate, *size, funch=self.getSizeWindow), *size)


class BaseWindowError(BaseWindow):
    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)
        self.setWindowFlag(Qt.Dialog)

    def initButton(self):
        self.btn = BaseButton(self, "Ok", locate=(BasePoint(self.size()[0], self.size()[1]) - [100, 40]).getTuple(),
                              size=[90, 30])
        self.btn.clicked.connect(exit, 1)

    def setFunctionError(self, r):
        self.btn.clicked.disconnect()
        self.btn.clicked.connect(r)


class BasePoint(BaseUnit):
    def __init__(self, x, y, object=None):
        self.x = x
        self.y = y
        self.object = object

    def __add__(self, other):
        if type(other) == type(self):
            return BasePoint(self.x + other.x, self.y + other.y)
        return BasePoint(self.x + other[0], self.y + other[1])

    def __neg__(self):
        return BasePoint(-self.x, -self.y)

    def __abs__(self):
        return (self.x ^ 2 + self.y ^ 2) ^ 0.5

    def __sub__(self, other):
        if type(other) == type(self):
            return BasePoint(self.x - other.x, self.y - other.y)
        return BasePoint(self.x - other[0], self.y - other[1])

    def __mul__(self, other):
        if type(other) == type(self):
            return BasePoint(self.x * other.x, self.y * other.y)
        return BasePoint(self.x * other[0], self.y * other[1])

    def __repr__(self):
        return f"x: {self.x}, y: {self.y}"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def getTuple(self):
        return self.x, self.y
