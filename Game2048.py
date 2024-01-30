import numpy as np
import random


class Game2048(object):

    def __init__(self):
        self._board = np.zeros((4, 4), dtype=int)

    def add_random_square(self) -> bool:
        num_zeros: int = np.count_nonzero(self._board == 0)
        if not num_zeros:
            return False
        else:
            board_num = random.randint(0, num_zeros - 1)
            input_array = np.zeros(num_zeros)
            input_array[board_num] = 1
            self._board[self._board == 0] = input_array * random.choice([2, 4])
            return True

    def get_board(self) -> np.ndarray:
        return self._board.copy()

    def move_up(self):
        self.__board_update(self._board.T)
        self.add_random_square()

    def move_down(self):
        self.__board_update(self._board.T[::-1])
        self.add_random_square()

    def move_left(self):
        self.__board_update(self._board)
        self.add_random_square()

    def move_right(self):
        self.__board_update(self._board[::-1])
        self.add_random_square()

    @staticmethod
    def __board_update(board: np.ndarray):
        for row in board:
            next_free_spot = 0
            if np.all(row == 0):
                continue
            for index in range(len(row)):
                if row[index] != 0:
                    # check whether to merge or move elements sequentially
                    if next_free_spot != 0 and row[next_free_spot - 1] == row[index]:
                        row[next_free_spot - 1] *= 2
                        row[index] = 0
                    else:
                        row[next_free_spot] = row[index]
                        row[index] = 0
                        next_free_spot += 1

    def __str__(self):
        return np.array_str(self._board)
