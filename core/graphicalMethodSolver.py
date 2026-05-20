import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.SolverStrategy import SolverStrategy
from model.Constraint import Constraint
from model.ObjectiveFunction import ObjectiveFunction
from PySide6.QtWidgets import QWidget
from UI.GraphicView import GraphicView
import numpy as np

class GraphicalMethodSolver(SolverStrategy):
    def __init__(self, objectiveFunction: ObjectiveFunction, constraints: list[Constraint]):
        self.__objectiveFunction = objectiveFunction
        self.__constraints = constraints
        self.epsilon = 1e-6

    def __init__(self, epsilon: float = 1e-6):
        self.epsilon = epsilon

    def solve(self, objectiveFunction: ObjectiveFunction, constraints: list[Constraint]) -> QWidget:
        self.__objectiveFunction = objectiveFunction
        self.__constraints = constraints
        fasiableIntersections = [intersection for intersection in self.__buildIntersections() if self.__evaluateFasiabilityIntersection(intersection)]
        maxValue = None
        optimalPoint = None
        for intersection in fasiableIntersections:
            value = self.__evaluateInZ(intersection)
            if maxValue is None or (self.__objectiveFunction.isMax and value > maxValue) or (not self.__objectiveFunction.isMax and value < maxValue):
                maxValue = value
                optimalPoint = intersection
        return GraphicView(self.__constraints, objectiveFunction, optimalPoint.tolist() if optimalPoint is not None else None, maxValue)

    def __buildIntersections(self)-> list[np.ndarray]:
        intersections = []
        for i in range(len(self.__constraints)):
            for j in range(i + 1, len(self.__constraints)):
                intersection = self.__calculateIntersection(self.__constraints[i], self.__constraints[j])
                if intersection is not None:
                    intersections.append(intersection)
        return intersections

    def __calculateIntersection(self, constraint1: Constraint, constraint2: Constraint)-> np.ndarray:
        A = np.array([constraint1.coefficients, constraint2.coefficients])
        b = np.array([constraint1.value, constraint2.value])
        try:
            solution = np.linalg.solve(A, b)
            if np.all(solution >= -self.epsilon):  # Check if the solution is in the first quadrant (non-negative)
                return solution
            else:
                return None
        except np.linalg.LinAlgError:
            return None

    def __evaluateFasiabilityIntersection(self, intersection: np.ndarray) -> bool:
        for constraint in self.__constraints:
            val = np.dot(constraint.coefficients, intersection)
            if constraint.relation == "<=" and val > constraint.value + self.epsilon:
                return False
            elif constraint.relation == ">=" and val < constraint.value - self.epsilon:
                return False
            elif constraint.relation == "=" and abs(val - constraint.value) > self.epsilon:
                return False
        return True
    
    def __evaluateInZ(self, intersection: np.ndarray) -> float:
        return np.dot(self.__objectiveFunction.coefficients, intersection)