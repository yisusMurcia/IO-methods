import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.SimlexSensitivilityAnalyzer import SimlexSensitivilityAnalyzer
from model.tableau import Tableau
import unittest

class TestSimplexSensitivityAnalyzer(unittest.TestCase):
    def test_analyze_new_resource(self):
        """
        Test sensitivity analysis with new resource values: z=30, constraints=[6, 8, 4]
        """
        # Final tableau: Maximize 16x + 24y
        # With z=30, constraints=[6, 8, 4]
        tableau_data = [
            [0, 0, -2, 0, -4, -208],      # objective function row (z row)
            [0, 1, 1/4, 0, -1/2, 6],    # x₂ row
            [0, 0, 2, 1, -10, 0],         # s₂ row (slack variable)
            [1, 0, -1/4, 0, 1, 4]       # x₁ row
        ]
        
        varNames = ['x1', 'x2', 's1', 's2', 's3']
        cb = ['x2', 's2', 'x1']  # basic variables names
        
        tableau = Tableau(tableau_data, True)
        analyzer = SimlexSensitivilityAnalyzer(tableau, varNames, cb)
        
        # Test new resource with z=30, constraint coefficients [6, 8, 4]
        resourceData = [30, 6, 8, 4]
        result = analyzer.analyzeNewResource(resourceData)
        
        # The result should be a boolean indicating if the new resource is feasible
        self.assertFalse(result)
        print(f"New resource analysis result with z=30 and constraints [6, 8, 4]: {result}")
        print(analyzer.analyzeVars())
        print(analyzer.analyzeResources())

if __name__ == '__main__':
    unittest.main()
