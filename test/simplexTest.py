import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.Simplex import Simplex
import unittest

class TestSimplex(unittest.TestCase):
    def test_simplex_maximization(self):
        # Maximize 3x + 2y subject to x + y <= 4, 2x + y <= 5, x >= 0, y >= 0
        tableau = [
            [3, 2, 0, 0, 0],  # objective
            [1, 1, 1, 0, 4],  # constraint 1
            [2, 1, 0, 1, 5]   # constraint 2
        ]
        varNames = ['x', 'y', 's1', 's2']
        cb = ['s1', 's2']
        simplex = Simplex(tableau, True, varNames, cb)
        solution = simplex.getSolution()
        print(solution)
        # Optimal solution: x = 1, y = 3, objective = 9
        self.assertIn('x = 1', solution)
        self.assertIn('y = 3', solution)

if __name__ == '__main__':
    unittest.main()

