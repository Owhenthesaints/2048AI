from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
import sys


class Window2048(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('2048 Game')
        self.setStyleSheet('background-color:grey; color: black')
        grid = QGridLayout()

        for row in range(4):
            for col in range(4):
                button = QPushButton("0")
                button.setFixedSize(75, 75)
                grid.addWidget(button, row, col)
