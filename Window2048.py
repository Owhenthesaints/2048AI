from PyQt6.QtWidgets import QMainWindow, QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout, QGraphicsRectItem, \
    QGraphicsTextItem, QGraphicsItem, QSizePolicy, QStackedLayout, QHBoxLayout
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt
import numpy as np

DEFAULT_WINDOW_SIZE = (300, 300, 300, 300)
DEFAULT_SIZE = (4, 4)


class BoxNumber2048(QGraphicsItem):
    def __init__(self, number: int, x, y, size: tuple, parent=None):
        """
        A Box with a number and a Background Color
        :param number: Number inside the box
        :param x: positioning x
        :param y: positioning y
        :param size: size width then height
        :param parent: define parent for memory management
        """
        super().__init__(parent)
        self._square_background = QGraphicsRectItem(0, 0, size[0], size[1], self)
        self._square_background.setBrush(QColor(0, 0, 0))
        self._text_item = QGraphicsTextItem(str(number), self)
        self._text_item.setDefaultTextColor(QColor("white"))


class Overlay2048(QGraphicsView):
    def __init__(self, board: np.ndarray = None, window_size: tuple = DEFAULT_SIZE, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self._SIZE = window_size

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
    def __init__(self, size: tuple = DEFAULT_SIZE, window_size: tuple = DEFAULT_WINDOW_SIZE) -> None:
        """
        A class to instantiate a Window which can host a 2048 game.
        :param window_size: x, y and initial width and height of the window
        :type window_size: tuple
        :param size: n then m representing size of playable area
        :type size: tuple
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
        self.view2048 = Overlay2048(np.zeros((4, 4)), size, self.central_widget)
        self.view2048.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.view2048.setStyleSheet("background-color: transparent")

        # intialize layout
        self.layout = QStackedLayout(self.central_widget)
        self.layout.addWidget(self.view2048)
