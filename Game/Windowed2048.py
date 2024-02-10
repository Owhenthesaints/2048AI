import numpy as np

from Game.Game2048 import Game2048
from GUI.Window2048 import Window2048
from PyQt6.QtCore import Qt

DEFAULT_DIVS = (4, 4)


class Windowed2048(Game2048, Window2048):

    def __init__(self, size_board: tuple = DEFAULT_DIVS, filename: str = None, overwrite: bool = True, agent=None):
        Game2048.__init__(self, size_board, filename, overwrite)
        Window2048.__init__(self, np.zeros(size_board))
        self.set_board(self.get_board())

    def _set_window_board(self, board: np.ndarray):
        Window2048.set_board(self, board)

    def show_board_with_agent(self, agent):
        agent.play()


    def keyPressEvent(self, a0):
        key = a0.key()
        if self.is_game_over():
            print("Final score ", self._score)

        if self.has_lost():
            if key == Qt.Key.Key_Escape:
                self.write_new_game_indication()
                self.get_last_board_csv()
                self.close()
            return

        if key == Qt.Key.Key_Z:
            super().move_up()
        elif key == Qt.Key.Key_S:
            super().move_down()
        elif key == Qt.Key.Key_Q:
            super().move_left()
        elif key == Qt.Key.Key_D:
            super().move_right()
        elif key == Qt.Key.Key_Escape:
            self.close()

        self._set_window_board(self._board)

    def set_board(self, board: np.ndarray):
        Window2048.set_board(self, board)
        Game2048.set_board(self, board)

    def move_up(self):
        super().move_up()
        Window2048.set_board(self, self._board)

    def move_right(self):
        super().move_right()
        Window2048.set_board(self, self._board)

    def move_left(self):
        super().move_left()
        Window2048.set_board(self, self._board)

    def move_down(self):
        super().move_down()
        Window2048.set_board(self, self._board)
