from PyQt6.QtWidgets import QMainWindow, QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout, QGraphicsRectItem, \
    QGraphicsTextItem, QGraphicsItem, QSizePolicy
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt
import numpy as np

DEFAULT_WINDOW_SIZE = (300, 300, 300, 300)


class BackgroundGrid(QWidget):

    def __init__(self, size: tuple = (4, 4), parent=None):
        super().__init__(parent)
        print("Background initialized")
        self._SIZE = size

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))

        if self.height() <= self._SIZE[0] or self.width() <= self._SIZE[0]:
            return

        for i in range(0, self.width(), self.width() // self._SIZE[0]):
            painter.drawLine(i, 0, i, self.height())

        for j in range(0, self.height(), self.height() // self._SIZE[0]):
            painter.drawLine(0, j, self.width(), j)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()


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
    def __init__(self, board: np.ndarray = None, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)


class Window2048(QMainWindow):
    def __init__(self, size: tuple = (4, 4), window_size: tuple = DEFAULT_WINDOW_SIZE) -> None:
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
        self.background_widget = BackgroundGrid(size, self.central_widget)
        self.background_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scene = QGraphicsScene(self.central_widget)
        scene.setSceneRect(0, 0, 1, 1)
        view = QGraphicsView(scene)
        view.setStyleSheet("background-color: transparent;")
        view.setSceneRect(0,0, 0, 0)

        # intialize layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.background_widget)
        self.layout.addWidget(view)
        self.layout.setStretch(0, 1)
        self.layout.setStretch(1, 0)