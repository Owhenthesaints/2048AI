from PyQt6.QtWidgets import QMainWindow, QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout, QGraphicsRectItem, \
    QGraphicsTextItem, QGraphicsItem, QSizePolicy, QStackedLayout, QHBoxLayout
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QRectF
import numpy as np
from typing import Union

DEFAULT_WINDOW_SIZE = (300, 300, 300, 300)
DEFAULT_DIV = (4, 4)
COLOR_DICT = {
    0: QColor(0, 0, 0, 0),
    2: QColor(238, 228, 218, 255),
    4: QColor(236, 224, 202, 255),
    8: QColor(244, 177, 125),
    16: QColor(245, 149, 101, 255),
    32: QColor(245, 124, 95, 255),
    64: QColor(246, 93, 59, 255),
    128: QColor(239, 205, 115, 255),
    256: QColor(237,204,99,255),
    512: QColor(237, 198, 81),
    1024: QColor(238, 199, 68),
    2048: QColor(238, 193, 48),
    4096: QColor(254, 61, 62),
    8192: QColor(255, 32, 33),
    16384: QColor(255, 32, 33),
    32768: QColor(255, 32, 33),
    65536: QColor(255, 32, 33),
    131072: QColor(255, 32, 33)
}


class BoxNumber2048(QGraphicsItem):
    def __init__(self, number: int, x: int, y: int, size: tuple = (50, 50), parent=None):
        """
        A Box with a number and a Background Color
        :param number: Number inside the box
        :param x: positioning x
        :param y: positioning y
        :param size: size width then height
        :param parent: define parent for memory management
        """
        super().__init__(parent)
        self.__position = [x, y]
        self._square_background = QGraphicsRectItem(x, y, size[0], size[1], self)
        self._square_background.setBrush(QColor("yellow"))
        self._text_item = QGraphicsTextItem(str(number), self._square_background)
        self._text_item.setDefaultTextColor(QColor(0, 0, 0))

    def boundingRect(self):
        return self._square_background.boundingRect()

    def resize_event(self, position: list, size: tuple):
        self.__position = position
        self._square_background.setRect(self.__position[0], self.__position[1], size[0], size[1])

    def paint(self, painter: QPainter, option, widget=None):
        self._square_background.paint(painter, option, widget)
        self._text_item.paint(painter, option, widget)


class Overlay2048(QGraphicsView):
    def __init__(self, num_div: tuple = DEFAULT_DIV, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self._DIVS = num_div
        self.__background_squares: list[BoxNumber2048] = [
            BoxNumber2048(2, 0, 0, (self.width() // self._DIVS[0], self.height() // self._DIVS[0]))]

        for background_box in self.__background_squares:
            self.scene.addItem(background_box)

    def draw_board(self, board: Union[np.ndarray, list[list]]):
        if board.shape != self._DIVS:
            raise ValueError("The board does not have have the right size")

    def drawBackground(self, painter, rect):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QColor(0, 0, 0))

        if self.height() <= self._DIVS[0] or self.width() <= self._DIVS[0]:
            return

        for i in range(0, self.width(), self.width() // self._DIVS[0]):
            painter.drawLine(i, 0, i, self.height())

        for j in range(0, self.height(), self.height() // self._DIVS[0]):
            painter.drawLine(0, j, self.width(), j)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setSceneRect(0, 0, self.viewport().width(), self.viewport().height())
        for background_square in self.__background_squares:
            background_square.resize_event([0, 0], (self.width() // self._DIVS[0], self.height() // self._DIVS[1]))


class Window2048(QMainWindow):
    def __init__(self, num_divs: tuple = DEFAULT_DIV, window_size: tuple = DEFAULT_WINDOW_SIZE) -> None:
        """
        A class to instantiate a Window which can host a 2048 game.
        :param window_size: x, y and initial width and height of the window
        :type window_size: tuple
        :param num_divs: n then m representing size of playable area
        :type num_divs: tuple
        :rtype: None
        """
        super().__init__()
        # setting up window generally
        self.setWindowTitle("2048 Game")
        self.setGeometry(*window_size)
        self.setStyleSheet('background-color:grey; color: black')

        # setting up central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # intialize background widget and 2048 overlay
        self._view2048 = Overlay2048(num_divs, self.central_widget)
        self._view2048.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._view2048.setStyleSheet("background-color: transparent")

        # intialize layout
        self.layout = QStackedLayout(self.central_widget)
        self.layout.addWidget(self._view2048)
