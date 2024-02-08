import numpy as np
import warnings

SAVE_TYPE = np.uint8

class GameSaver:
    def __init__(self, filename: str = './Logs/game2048.csv'):
        if not isinstance(filename, str):
            raise TypeError('filename should be string')
        self.FILENAME = filename

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
            np.savetxt(f, np.array([['']*9]), delimiter=',', fmt='%s')

