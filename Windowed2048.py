from Game2048 import Game2048, Direction
from Window2048 import Window2048
from PyQt6.QtCore import Qt


class Windowed2048(Game2048, Window2048):

    def __init__(self):
        Game2048.__init__(self)
        Window2048.__init__(self)

    def keyPressEvent(self, a0):
        print("keyPressEvent")
        key = a0.key()

        if key == Qt.Key.Key_Up:
            self.move_up()
            print("moving up")
        if key == Qt.Key.Key_Down:
            self.move_down()
        if key == Qt.Key.Key_Left:
            self.move_left()
        if key == Qt.Key.Key_Right:
            self.move_right()
