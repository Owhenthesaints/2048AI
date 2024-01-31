import sys

import numpy as np
from pynput import keyboard
from Windowed2048 import Windowed2048
from PyQt6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

game = Windowed2048()

game.show()

game.set_board(np.array([[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [4, 4, 8, 2]]))

sys.exit(app.exec())