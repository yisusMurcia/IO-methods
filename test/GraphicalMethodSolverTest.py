import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from PySide6.QtWidgets import QApplication
from core.graphicalMethodSolver import GraphicalMethodSolver
from model.Constraint import Constraint
from model.ObjectiveFunction import ObjectiveFunction


def display_graphical_solution():
    objective = ObjectiveFunction([300, 200], True)
    constraints = [
        Constraint([1, 0.25], '<=', 160),   # madera
        Constraint([2.5, 4], '<=', 800),    # tubería
        Constraint([2, 1.5], '<=', 360),    # horas de trabajo
        Constraint([0, 0.2], '<=', 50)      # hule espuma
    ]

    app = QApplication(sys.argv)
    solver = GraphicalMethodSolver()
    result_view = solver.solve(objective, constraints)
    result_view.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    display_graphical_solution()
