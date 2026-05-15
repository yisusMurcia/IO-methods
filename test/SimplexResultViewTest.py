import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PySide6.QtWidgets import QApplication
from UI.simplexResultView import SimplexResultView

# Sample data for testing
tableau = [
            [0, 0, -2, 0, -4, -208],      # objective function row (z row)
            [0, 1, 1/4, 0, -1/2, 6],    # x₂ row
            [0, 0, 2, 1, -10, 0],         # s₂ row (slack variable)
            [1, 0, -1/4, 0, 1, 4]       # x₁ row
        ]
        
varNames = ['x1', 'x2', 's1', 's2', 's3']
cb = ['x2', 's2', 'x1']  # basic variables names
isFeasible = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = SimplexResultView(varNames, tableau, isFeasible, cb)
    view.show()
    sys.exit(app.exec())

