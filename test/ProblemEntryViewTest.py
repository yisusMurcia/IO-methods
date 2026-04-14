import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from UI.ProblemEntryView import ProblemEntryView

from PySide6.QtWidgets import QApplication

app = QApplication([])      # inicia la app

window = ProblemEntryView(None)       # instancia tu clase
window.show()               # 👈 muestra la ventana

app.exec()                  # loop de la app