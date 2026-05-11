import sys
import os

from UI.MainWindow import MainWindow
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PySide6.QtWidgets import QApplication


app = QApplication([])
window = MainWindow()
window.show()
app.exec()