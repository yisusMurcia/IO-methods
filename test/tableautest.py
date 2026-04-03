import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.tableau import Tableau
import unittest
import numpy as np

class TestTableau(unittest.TestCase):
    def setUp(self):
        # Sample tableau for maximization: max 3x + 2y, s.t. x+y<=4, 2x+y<=5
        self.max_tableau = [
            [3, 2, 0, 0, 0],  # objective
            [1, 1, 1, 0, 4],  # constraint 1
            [2, 1, 0, 1, 5]   # constraint 2
        ]
        self.tableau_max = Tableau(self.max_tableau, True)

        # For minimization: min x + y, s.t. x+y>=1, x>=0, y>=0
        # But need to convert to standard form, but for test, simple
        self.min_tableau = [
            [1, 1, 0, 0],  # will be negated to [-1,-1,0,0]
            [1, 1, 1, 1]   # constraint
        ]
        self.tableau_min = Tableau(self.min_tableau, False)

    def test_init_max(self):
        expected = np.array(self.max_tableau, dtype=float)
        np.testing.assert_array_equal(self.tableau_max.tableau, expected)

    def test_init_min(self):
        expected = np.array(self.min_tableau, dtype=float)
        expected[-1, :-1] *= -1  # negate objective
        np.testing.assert_array_equal(self.tableau_min.tableau, expected)

    def test_get_incoming_variable_max(self):
        self.assertEqual(self.tableau_max.getIncomingVariable(), 0)

    def test_get_leaving_variable(self):
        incoming = self.tableau_max.getIncomingVariable()
        leaving = self.tableau_max.getLeavingVariable(incoming)
        self.assertEqual(leaving, 2)  # row 2 (0-based)

    def test_pivot(self):
        # Before pivot
        original = self.tableau_max.tableau.copy()
        self.tableau_max.pivot(2, 0)
        # Check pivot element is 1
        self.assertEqual(self.tableau_max.tableau[2, 0], 1.0)
        # Check other elements in column 0 are 0
        self.assertEqual(self.tableau_max.tableau[0, 0], 0.0)
        self.assertEqual(self.tableau_max.tableau[1, 0], 0.0)

    def test_is_optimal_not(self):
        self.assertFalse(self.tableau_max.isOptimal())

    def test_is_optimal_yes(self):
        # Create optimal tableau
        optimal_tableau = [
            [-1, -2, 0, 0, 10],  # all negative
            [1, 1, 1, 0, 4],
            [2, 1, 0, 1, 5]
        ]
        tableau_opt = Tableau(optimal_tableau, True)
        self.assertTrue(tableau_opt.isOptimal())

if __name__ == '__main__':
    unittest.main()