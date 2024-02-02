from typing import List, Tuple
from PyQt6.QtWidgets import QMainWindow, QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout, QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtGui import QPainter, QColor
import numpy as np

DEFAULT_WINDOW_SIZE = (300, 300, 300, 300)


class BackgroundGrid(QWidget):

    def __init__(self, size: tuple = (4, 4), parent=None):
        super().__init__(parent)
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


class Box2048(QGraphicsView):
    def __init__(self, board: np.ndarray = None, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        # set the boxes
        self.black_boxes: List[List[QGraphicsRectItem, QGraphicsTextItem]] = []
        black_box = QGraphicsRectItem(0, 0, 100, 100)
        black_box.setBrush(QColor(0, 0, 0))


class Window2048(QMainWindow):
    def __init__(self, size: tuple = (4, 4), window_size: tuple = DEFAULT_WINDOW_SIZE) -> None:
        """
        A class to instantiate a Window which can host a 2048 game.
        :param window_size: x, y and initial width and height of the window
        :type window_size: tuple
        :param size: n then m representing size of playable area
        :return: None
        :rtype: None
        :type size: tuple
        """
        super().__init__()
        self.setWindowTitle("2048 Game")
        self.setGeometry(*window_size)

        # setting up different widgets
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.background_widget = BackgroundGrid(size, self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        self.layout.addWidget(self.background_widget)
        self.setWindowTitle('2048 Game')
        self.setStyleSheet('background-color:grey; color: black')
