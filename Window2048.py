from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt6.QtGui import QPainter, QColor


class Window2048(QWidget):
    def __init__(self, size: tuple = (4, 4), window_size: tuple = (300, 300, 300, 300)) -> None:
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
        self._SIZE = size
        self.setGeometry(*window_size)
        self.setWindowTitle('2048 Game')
        self.setStyleSheet('background-color:grey; color: black')

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
