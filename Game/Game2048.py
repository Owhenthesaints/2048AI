import numpy as np
import random
from enum import Enum
from typing import Tuple
import time
import csv
import warnings
from FileWriter.GameSaver import GameSaver


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Game2048:
    """
    A class to handle all base class logic to move the board
    """

    def __init__(self, size_board: tuple = (4, 4), write_filename: str = "./Logs/game2048.csv", overwrite: bool = True):
        """
        :param size_board: the size of the board for the game 4*4 etc...
        :type size_board: tuple
        :param write_filename: where to write game if None does not write game
        :type write_filename: str
        """
        self._score = 0
        self._board: np.ndarray = np.zeros(size_board, dtype=int)
        self._lost: bool = False
        self.add_random_square()

        # add writing state
        self.__writing = True
        if write_filename is None:
            self.__writing = False

        # setup the writer
        if self.__writing:
            if not write_filename.endswith(".csv"):
                warnings.warn("filename must end with csv writing disabled", UserWarning)
                self.__writing = False
            else:
                # initialising the writer
                self.__writer = GameSaver(write_filename)
                if isinstance(overwrite, bool) and overwrite:
                    self.__writer.wipe_board()
                elif not isinstance(overwrite, bool):
                    raise TypeError("overwrite should be of type bool")

        if self.__writing:
            self.write_to_csv()

    def set_board(self, board: np.ndarray):
        self._board = board.copy()

    def write_to_csv(self):
        if self.__writing:
            self.__writer.append_board(self._board)
        else:
            warnings.warn("writer is not initialised")

    def write_new_game_indication(self):
        if self.__writing:
            self.__writer.indicate_new_game()
        else:
            warnings.warn("writer is not initialised")

    def has_lost(self):
        return self._lost

    def get_last_board_csv(self):
        if self.__writing:
            print(self.__writer.get_last_board())
        else:
            warnings.warn("No Writer initialised", UserWarning)

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
            for i in range(1, len(temp_board)):
                if np.any(temp_board[i] == temp_board[i - 1]) or np.any(temp_board.T[i] == temp_board.T[i - 1]):
                    self._lost = False
                    return False
            self._lost = True
            return True
        else:
            self._lost = False
            return False

    def move_up(self):
        self.__move(Direction.UP)

    def move_down(self):
        self.__move(Direction.DOWN)

    def move_left(self):
        self.__move(Direction.LEFT)

    def move_right(self):
        self.__move(Direction.RIGHT)

    def __move(self, direction: Direction):
        # move
        if direction == Direction.UP:
            self.__move_up()
        elif direction == Direction.DOWN:
            self.__move_down()
        elif direction == Direction.LEFT:
            self.__move_left()
        elif direction == Direction.RIGHT:
            self.__move_right()

        # write
        if self.__writing:
            self.write_to_csv()

        #update game over state
        self.is_game_over()

    def __move_up(self):
        board = self.__board_update(self._board.T)
        if not np.array_equal(self._board, board.T):
            self._board = board.T
            self.add_random_square()

    def __move_down(self):
        board = self.__board_update(self._board.T[::, ::-1])[::, ::-1].T
        if not np.array_equal(self._board, board):
            self._board = board
            self.add_random_square()

    def __move_left(self):
        board = self.__board_update(self._board.copy())
        if not np.array_equal(board, self._board):
            self._board = board
            self.add_random_square()

    def __move_right(self):
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
