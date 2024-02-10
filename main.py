# Example of implementation
import sys
from PyQt6.QtWidgets import QApplication
from Game.Windowed2048 import Windowed2048
from Agents.RandomAgent import RandomAgent

app = QApplication(sys.argv)

window2048 = Windowed2048(filename="./Logs/game2048.csv")

window2048.show()

random_agent = RandomAgent(window2048)

random_agent.play()

sys.exit(app.exec())
