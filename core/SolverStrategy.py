from abc import abstractmethod
from PySide6.QtWidgets import QWidget

class SolverStrategy:
    @abstractmethod
    def solve(self, objectiveFunction, constraints)-> QWidget:
        pass
