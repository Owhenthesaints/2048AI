import numpy as np
import warnings

SAVE_TYPE = np.uint8


class GameSaver:
    def __init__(self, filename: str = './Logs/game2048.csv', size: tuple = (4, 4)):
        if not isinstance(filename, str):
            raise TypeError('filename should be string')
        self.FILENAME = filename
        self._SIZE = size

    def append_board(self, board: np.ndarray) -> None:
        """
        appends the board to the .csv
        :param board: a numpy array
        :return: None
        """
        with open(self.FILENAME, 'a') as f:
            warnings.catch_warnings()
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            powers_of_two = np.log2(board)
            warnings.filterwarnings("default", category=RuntimeWarning)
            powers_of_two[powers_of_two == -np.inf] = 0
            np.savetxt(f, powers_of_two.reshape(1, -1).astype(SAVE_TYPE), delimiter=',', fmt='%d')

    def wipe_board(self) -> None:
        open(self.FILENAME, 'w').close()

    def indicate_new_game(self) -> None:
        with open(self.FILENAME, 'a') as f:
            np.savetxt(f, np.array([[''] * (self._SIZE[0] * self._SIZE[1])]), delimiter=',', fmt='%s')

    def get_last_board(self):
        size_last_chunck = self._SIZE[0] * self._SIZE[1] * 2 + self._SIZE[1] * self._SIZE[0]
        with open(self.FILENAME, 'r', encoding="ascii") as file:
            file.seek(0, 2)
            file.seek(file.tell() - size_last_chunck, 0)
            last_chunck = file.read(size_last_chunck)
            lines = last_chunck.splitlines()
            for line in reversed(lines):
                if not (line == "" or ',,' in line):
                    split_line = line.split(',')
                    int_array = np.array(split_line, dtype=np.uint8)
                    value_array = np.where(int_array != 0, 2 ** int_array, 0)
                    return value_array.reshape(self._SIZE[0], self._SIZE[1])

