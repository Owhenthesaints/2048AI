from PyQt6.QtWidgets import QMainWindow, QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout, QGraphicsRectItem, \
    QGraphicsTextItem, QGraphicsItem, QSizePolicy, QStackedLayout, QHBoxLayout
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QRectF
import numpy as np
from typing import Union

DEFAULT_WINDOW_SIZE = (300, 300, 300, 300)
DEFAULT_DIV = (4, 4)



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

    def paint(self, painter: QPainter, option, widget=None):
        self._square_background.paint(painter, option, widget)
        self._text_item.paint(painter, option, widget)


class Overlay2048(QGraphicsView):
    def __init__(self, num_div: tuple = DEFAULT_DIV, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self._SIZE = num_div
        self.__background_squares: list[BoxNumber2048] = [BoxNumber2048(2, 0, 0, (50, 50))]
        for background_box in self.__background_squares:
            self.scene.addItem(background_box)

    def draw_board(self, board: Union[np.ndarray, list[list]]):
        if board.shape != self._SIZE:
            raise ValueError("The board does not have have the right size")

    def drawBackground(self, painter, rect):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QColor(0, 0, 0))

        if self.height() <= self._SIZE[0] or self.width() <= self._SIZE[0]:
            return

        for i in range(0, self.width(), self.width() // self._SIZE[0]):
            painter.drawLine(i, 0, i, self.height())

        for j in range(0, self.height(), self.height() // self._SIZE[0]):
            painter.drawLine(0, j, self.width(), j)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setSceneRect(0, 0, self.viewport().width(), self.viewport().height())


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
