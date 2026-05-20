import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.Constraint import Constraint
import numpy as np
from typing import Optional, Tuple

class GraphicMethodSensibilityAnalizer:
    def __init__(self, maxValue: float, optimalPoint: list[float], constraints: list[Constraint], objectiveValues: list[float]):
        self.__maxValue = maxValue
        self.__optimalPoint = optimalPoint
        self.__constraints = constraints
        self.__objectiveValues = objectiveValues
        self.__activeConstraints = self.__getActiveConstraints(self.__optimalPoint)

    def analyzeVars(self)->str:
        analysis = "Sensitivity Analysis for Decision Variables (in Z):\n"
        if len(self.__activeConstraints) < 2:
            return analysis + "Not enough active constraints at the optimal vertex to perform variable sensitivity analysis.\n"

        slope = self.__getSlope(self.__objectiveValues)
        slopes = [self.__getSlope(c.coefficients) for c in self.__activeConstraints]
        slopes.sort()
        if slope != float('inf'):
            #x1
            c1 = [-s*self.__objectiveValues[1] - self.__objectiveValues[0] for s in slopes]
            if self.__objectiveValues[1] > 0:
                c1.reverse()
            
            analysis+= f"x1: {c1[0] if c1[0] != None else "-∞"} <= d <= {c1[1] if c1[1] != None else "∞"}\n"

            #x2
            c2 = [-self.__objectiveValues[0]/s - self.__objectiveValues[1] if s != 0 else None for s in slopes]

            if self.__objectiveValues[1] > 0:
                c2.reverse()

            analysis+= f"x2: {c2[0] if c2[0] != None else "-∞"} <= d <= {c2[1] if c2[1] != None else "∞"}"
            
        return analysis
    
    def __getActiveConstraints(self, point: list[float])-> list[Constraint]:
        if point is None:
            return []
        return [constraint for constraint in self.__constraints if self.__isActiveConstraint(constraint, point)]

    def __getIntersection(self, value: float)-> list[Constraint]:
        for i in range(len(self.__constraints)):
            for j in range(i + 1, len(self.__constraints)):
                intersection = self.__calculateIntersection(self.__constraints[i], self.__constraints[j])
                if intersection is not None:
                    if np.isclose(np.dot(self.__constraints[0].coefficients, intersection), value, atol=1e-6):
                        return [self.__constraints[i], self.__constraints[j]]
        return None

    def __calculateIntersection(self, constraint1: Constraint, constraint2: Constraint) -> Optional[np.ndarray]:
        A = np.array([constraint1.coefficients, constraint2.coefficients])
        b = np.array([constraint1.value, constraint2.value])
        try:
            return np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            return None
    
    def analyzeResources(self)->str:
        analysis = "Sensitivity Analysis of Resources:\n"
        active_constraints = [constraint for constraint in self.__constraints if self.__isActiveConstraint(constraint, self.__optimalPoint)]
        if len(active_constraints) < 2:
            return analysis + "Not enough active constraints at the optimal vertex to perform RHS sensitivity analysis.\n"

        for index, constraint in enumerate(self.__constraints):
            analysis += self.__analyceResource(index, constraint, active_constraints) + "\n"
        return analysis

    def __getSlope(self, values: list[float])-> float:
        return - values[0] / values[1] if values[1] != 0 else float('inf')
    
    def __analyceResource(self, index: int, analyzed_constraint: Constraint, active_constraints: list[Constraint])->str:
        analysis = f"Constraint {index + 1} + d: "
        if not self.__isActiveConstraint(analyzed_constraint, self.__optimalPoint):
            return analysis + "not active at optimal vertex; range not determined."

        partner = self.__findActivePartner(analyzed_constraint, active_constraints)
        if partner is None:
            return analysis + "no second active constraint found to determine RHS range."

        feasible_range = self.__calculateRhsRange(analyzed_constraint, partner)
        if feasible_range is None:
            return analysis + "no feasible range."

        lower, upper = feasible_range
        lower_text = str(lower) if lower != float("-inf") else "-∞"
        upper_text = str(upper) if upper != float("inf") else "∞"
        return analysis + f"{lower_text} <= d <= {upper_text}"
    
    def __getFasibleIntersection(self, analyzed_constraint: Constraint, partner_constraint: Constraint)-> tuple[np.ndarray, np.ndarray]:
        A = np.array([analyzed_constraint.coefficients, partner_constraint.coefficients])
        b0 = np.array([analyzed_constraint.value, partner_constraint.value])
        b1 = np.array([analyzed_constraint.value + 1, partner_constraint.value])

        try:
            p0 = np.linalg.solve(A, b0)
            p1 = np.linalg.solve(A, b1)
            return p0, p1
        except np.linalg.LinAlgError:
            raise ValueError("Active constraints are parallel or degenerate; cannot compute feasible intersection.")

    def __isActiveConstraint(self, constraint: Constraint, point: list[float])-> bool:
        if point is None:
            return False
        return np.isclose(np.dot(constraint.coefficients, point), constraint.value, atol=1e-9)

    def __findActivePartner(self, analyzed_constraint: Constraint, active_constraints: list[Constraint])-> Optional[Constraint]:
        for constraint in active_constraints:
            if constraint is analyzed_constraint:
                continue
            intersection = self.__solveIntersection(analyzed_constraint, constraint)
            if intersection is not None and np.allclose(intersection, self.__optimalPoint, atol=1e-9):
                return constraint
        for constraint in active_constraints:
            if constraint is not analyzed_constraint:
                return constraint
        return None

    def __solveIntersection(self, constraint1: Constraint, constraint2: Constraint)-> Optional[np.ndarray]:
        A = np.array([constraint1.coefficients, constraint2.coefficients])
        b = np.array([constraint1.value, constraint2.value])
        try:
            return np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            return None

    def __calculateRhsRange(self, analyzed_constraint: Constraint, partner_constraint: Constraint)-> Optional[Tuple[float, float]]:
        try:
            p0, p1 = self.__getFasibleIntersection(analyzed_constraint, partner_constraint)
        except ValueError:
            return None

        direction = p1 - p0
        lower = float("-inf")
        upper = float("inf")
        epsilon = 1e-9

        for constraint in self.__constraints:
            if constraint is analyzed_constraint:
                continue

            K = np.dot(constraint.coefficients, direction)
            R = constraint.value - np.dot(constraint.coefficients, p0)

            if abs(K) < epsilon:
                if constraint.relation == "<=" and R < -epsilon:
                    return None
                if constraint.relation == ">=" and R < -epsilon:
                    return None
                if constraint.relation == "=" and abs(R) > epsilon:
                    return None
                continue

            L = R / K
            if constraint.relation == "<=":
                if K > 0:
                    upper = min(upper, L)
                else:
                    lower = max(lower, L)
            elif constraint.relation == ">=":
                if K > 0:
                    lower = max(lower, L)
                else:
                    upper = min(upper, L)
            else:  # equality
                lower = max(lower, L)
                upper = min(upper, L)

            if upper < lower - epsilon:
                return None

        for coordinate, step in zip(p0, direction):
            if abs(step) < epsilon:
                if coordinate < -epsilon:
                    return None
                continue

            limit = -coordinate / step
            if step > 0:
                lower = max(lower, limit)
            else:
                upper = min(upper, limit)

            if upper < lower - epsilon:
                return None

        return lower, upper
