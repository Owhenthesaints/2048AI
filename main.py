import sys
from PyQt6.QtWidgets import QApplication
from Game.Windowed2048 import Windowed2048

app = QApplication(sys.argv)

window = Windowed2048()

window.show()

sys.exit(app.exec())
