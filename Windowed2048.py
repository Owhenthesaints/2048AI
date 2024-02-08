import numpy as np

from Game2048 import Game2048
from Window2048 import Window2048
from PyQt6.QtCore import Qt


class Windowed2048(Game2048, Window2048):

    def __init__(self):
        Game2048.__init__(self, writing=True)
        Window2048.__init__(self)
        self.set_board(self.get_board())

    def set_board(self, board: np.ndarray):
        Window2048.set_board(self, board)
        Game2048.set_board(self, board)

    def keyPressEvent(self, a0):
        key = a0.key()
        if self.is_game_over():
            print("Final score ", self._score)

        if self.has_lost():
            if key == Qt.Key.Key_Escape:
                self.close()
            return

        if key == Qt.Key.Key_Z:
            self.move_up()
        elif key == Qt.Key.Key_S:
            self.move_down()
        elif key == Qt.Key.Key_Q:
            self.move_left()
        elif key == Qt.Key.Key_D:
            self.move_right()
        elif key == Qt.Key.Key_Escape:
            self.close()

        print(self._score)

        Window2048.set_board(self, self._board)
