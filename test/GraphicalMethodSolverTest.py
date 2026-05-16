import sys
import os
import unittest
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.graphicalMethodSolver import GraphicalMethodSolver
from model.Constraint import Constraint
from model.ObjectiveFunction import ObjectiveFunction

class TestGraphicalMethodSolver(unittest.TestCase):
    def test_maximize_with_less_than_or_equal_and_nonnegative_constraints(self):
        objective = ObjectiveFunction([3, 2], True)
        constraints = [
            Constraint([1, 1], '<=', 4),
            Constraint([1, 0], '>=', 0),
            Constraint([0, 1], '>=', 0)
        ]

        solver = GraphicalMethodSolver()
        solution = solver.solve(objective, constraints)

        self.assertIsNotNone(solution)
        np.testing.assert_allclose(solution, [4.0, 0.0], atol=1e-6)

    def test_minimize_with_greater_than_or_equal_and_nonnegative_constraints(self):
        objective = ObjectiveFunction([1, 2], False)
        constraints = [
            Constraint([1, 1], '>=', 4),
            Constraint([1, 0], '>=', 0),
            Constraint([0, 1], '>=', 0)
        ]

        solver = GraphicalMethodSolver()
        solution = solver.solve(objective, constraints)

        self.assertIsNotNone(solution)
        np.testing.assert_allclose(solution, [4.0, 0.0], atol=1e-6)

    def test_equal_constraint_selects_the_boundary_point(self):
        objective = ObjectiveFunction([2, 1], True)
        constraints = [
            Constraint([1, 1], '=', 4),
            Constraint([1, 0], '>=', 0),
            Constraint([0, 1], '>=', 0)
        ]

        solver = GraphicalMethodSolver()
        solution = solver.solve(objective, constraints)

        self.assertIsNotNone(solution)
        np.testing.assert_allclose(solution, [4.0, 0.0], atol=1e-6)

    def test_mixed_relations_with_less_equal_greater_equal_and_equal(self):
        objective = ObjectiveFunction([1, 3], True)
        constraints = [
            Constraint([1, 1], '<=', 5),
            Constraint([2, 1], '>=', 2),
            Constraint([1, 0], '>=', 0),
            Constraint([0, 1], '>=', 0)
        ]

        solver = GraphicalMethodSolver()
        solution = solver.solve(objective, constraints)

        self.assertIsNotNone(solution)
        np.testing.assert_allclose(solution, [0.0, 5.0], atol=1e-6)

if __name__ == '__main__':
    unittest.main()
