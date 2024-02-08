import numpy as np
import warnings


class GameSaver:
    def __init__(self, filename: str = './Logs/game2048.csv'):
        if not isinstance(filename, str):
            raise TypeError('filename should be string')
        self.FILENAME = filename

    def append_board(self, board: np.ndarray) -> None:
        with open(self.FILENAME, 'a') as f:
            warnings.catch_warnings()
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            powers_of_two = np.log2(board)
            warnings.filterwarnings("default", category=RuntimeWarning)
            powers_of_two[powers_of_two == -np.inf] = 0
            np.savetxt(f, powers_of_two.reshape(1, -1).astype(np.uint8), delimiter=',', fmt='%d')

    def wipe_board(self) -> None:
        open(self.FILENAME, 'w').close()


