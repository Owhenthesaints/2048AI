import numpy as np

from Game2048 import Game2048
from Window2048 import Window2048
from PyQt6.QtCore import Qt


class Windowed2048(Game2048, Window2048):

    def __init__(self):
        Game2048.__init__(self)
        Window2048.__init__(self)
        self.set_board(self.get_board())

    def set_board(self, board: np.ndarray):
        Window2048.set_board(self, board)
        Game2048.set_board(self, board)

    def keyPressEvent(self, a0):
        print("keyPressEvent")
        key = a0.key()

        if key == Qt.Key.Key_Z:
            self.move_up()
            print(self._board)
        if key == Qt.Key.Key_S:
            self.move_down()
            print(self._board)
        if key == Qt.Key.Key_Q:
            self.move_left()
            print(self._board)
        if key == Qt.Key.Key_D:
            self.move_right()
            print(self._board)
        if key == Qt.Key.Key_Escape:
            self.close()

        Window2048.set_board(self, self._board)
