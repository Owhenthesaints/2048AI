import numpy as np
import random
from enum import Enum
from typing import Tuple
import time


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Game2048:

    def __init__(self, size: tuple = (4, 4)):
        self._score = 0
        self._board: np.ndarray = np.zeros(size, dtype=int)
        self._lost: bool = False
        self.add_random_square()

    def set_board(self, board: np.ndarray):
        self._board = board.copy()

    def has_lost(self):
        return self._lost

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

    def is_game_over(self):
        if self._lost:
            return True
        elif np.all(self.get_board() != 0):
            temp_board = self.get_board()
            temp_board_t = self.get_board().T
            for i in range(1, len(temp_board)):
                if np.any(temp_board[i] == temp_board[i - 1]) or np.any(temp_board_t[i] == temp_board_t[i - 1]):
                    self._lost = False
                    return False
            self._lost = True
            return True
        else:
            self._lost = False
            return False

    def move_up(self):
        board = self.__board_update(self._board.T)
        if not np.array_equal(self._board, board.T):
            self._board = board.T
            self.add_random_square()

    def move_down(self):
        board = self.__board_update(self._board.T[::, ::-1])[::, ::-1].T
        if not np.array_equal(self._board, board):
            self._board = board
            self.add_random_square()

    def move_left(self):
        board = self.__board_update(self._board.copy())
        if not np.array_equal(board, self._board):
            self._board = board
            self.add_random_square()

    def move_right(self):
        board = self.__board_update(self._board[::, ::-1])[::, ::-1]
        if not np.array_equal(board, self._board):
            self._board = board
            self.add_random_square()

    def __board_update(self, board: np.ndarray) -> np.ndarray:
        board = board.copy()
        for row in board:
            if np.all(row == 0):
                continue
            next_free_spot = 0
            merged_limit = 0
            for index in range(len(row)):
                if row[index] != 0:
                    # check whether to merge or move elements sequentially
                    if (next_free_spot != 0 and merged_limit <= next_free_spot - 1 and
                            row[next_free_spot - 1] == row[index]):
                        row[next_free_spot - 1] <<= 1
                        self._score += row[next_free_spot - 1]
                        row[index] = 0
                        merged_limit += 1
                    elif next_free_spot != index:
                        row[next_free_spot] = row[index]
                        row[index] = 0
                        next_free_spot += 1
                    else:
                        next_free_spot += 1
        return board

    def __str__(self):
        return np.array_str(self._board)
