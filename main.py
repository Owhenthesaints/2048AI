import sys
from Window2048 import Window2048
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)
window = Window2048()

window.show()

app.exec()
