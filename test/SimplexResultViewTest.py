import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PySide6.QtWidgets import QApplication
from UI.simplexResultView import SimplexResultView

# Sample data for testing
varNames = ["x1", "x2", "s1", "s2"]
tableau = [
    [-1.0, 0.0, 0.0, 0.0],  # objective row
    [0.0, 1.0, 0.0, 4.0],   # constraint 1
    [0.0, 0.0, 1.0, 6.0]    # constraint 2
]
isFeasible = True
cb = ["x2", "x1"]  # basic variables

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = SimplexResultView(varNames, tableau, isFeasible, cb)
    view.show()
    sys.exit(app.exec())

