import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PySide6.QtWidgets import QApplication
from UI.ProblemEntryView import ProblemEntryView


app = QApplication([])
window = ProblemEntryView()
window.show()
app.exec()