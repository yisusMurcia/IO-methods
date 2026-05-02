import sys
import os

from core.Simplex import SimplexStrategy
from core.SolverStrategy import SolverStrategy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class SolverService:
    def __init__(self, problemEntryView):
        self.__problemEntryView = problemEntryView
        self.__solverStrategy: SolverStrategy = SimplexStrategy()

    def setSolverStrategy(self, solverStrategy):
        self.__solverStrategy = solverStrategy

    def solve(self, objectiveFunction, constraints):
        self.__solverStrategy.setData(objectiveFunction, constraints)
        if not self.__solverStrategy:
            raise ValueError("No solver strategy set")
        result = self.__solverStrategy.solve(objectiveFunction, constraints)
        print(result)
        return result
