import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.Constraint import Constraint
from model.ObjectiveFunction import ObjectiveFunction
from services.Adapter import Adapter

class TestAdapter(unittest.TestCase):
    
    def test_adapter_with_less_than_or_equal_constraint(self):
        """Test Adapter with <= constraint (should add slack variable)"""
        # Maximize: 3x1 + 2x2
        obj_func = ObjectiveFunction([3, 2], isMax=True)
        # Constraint: x1 + x2 <= 4
        constraints = [Constraint([1, 1], "<=", 4)]
        
        adapter = Adapter(obj_func, constraints)
        tableau = adapter.buildTable()
        
        # Verify tableau structure
        self.assertEqual(len(tableau), 2)  # 1 constraint + 1 objective function row
        self.assertEqual(len(tableau[0]), 4)  # 2 original vars + 1 slack + 1 RHS
        
        # Verify variable names include slack variable
        self.assertIn("s1", adapter.varNames)
        self.assertEqual(adapter.varNames, ["x1", "x2", "s1"])
        
        # Verify slack variable is in basis
        self.assertEqual(adapter.getCb(), ["s1"])
        
        # Verify slack variable column
        self.assertEqual(tableau[1][2], 1)  # s1 coefficient in constraint
        
    def test_adapter_with_greater_than_or_equal_constraint(self):
        """Test Adapter with >= constraint (should add excess and artificial variables)"""
        # Maximize: x1 + x2
        obj_func = ObjectiveFunction([1, 1], isMax=True)
        # Constraint: 2x1 + x2 >= 5
        constraints = [Constraint([2, 1], ">=", 5)]
        
        adapter = Adapter(obj_func, constraints)
        tableau = adapter.buildTable()
        
        # Verify variable names include excess and artificial variables
        self.assertIn("e1", adapter.varNames)
        self.assertIn("a1", adapter.varNames)
        self.assertEqual(adapter.varNames, ["x1", "x2", "e1", "a1"])
        
        # Verify artificial variable is in basis
        self.assertEqual(adapter.getCb(), ["a1"])
        
        # Verify excess variable coefficient (should be -1)
        self.assertEqual(tableau[1][2], -1)
        
        # Verify artificial variable coefficient (should be 1)
        self.assertEqual(tableau[1][3], 1)
        
        # Verify M penalty in objective function for artificial variable
        # For maximization, penalty should be -M (negative)
        self.assertTrue(tableau[0][3] < 0)  # Should be -M
    
    def test_adapter_with_multiple_constraints_mixed(self):
        """Test Adapter with multiple constraints of different types"""
        # Maximize: 2x1 + 3x2
        obj_func = ObjectiveFunction([2, 3], isMax=True)
        constraints = [
            Constraint([1, 1], "<=", 4),    # Slack s1
            Constraint([2, 1], ">=", 5),    # Excess e2 and Artificial a2
        ]
        
        adapter = Adapter(obj_func, constraints)
        tableau = adapter.buildTable()
        
        # Verify tableau dimensions
        self.assertEqual(len(tableau), 3)  # 2 constraints + 1 objective
        
        # Verify variable names
        expected_vars = ["x1", "x2", "s1", "e2", "a2"]
        self.assertEqual(adapter.varNames, expected_vars)
        
        # Verify basis variables
        self.assertEqual(adapter.getCb(), ["s1", "a2"])
        
        # Verify constraint 1 (<=): should have slack variable
        self.assertEqual(tableau[1][2], 1)  # s1 in first constraint
        self.assertEqual(tableau[1][3], 0)  # e2 not in first constraint
        self.assertEqual(tableau[1][4], 0)  # a2 not in first constraint
        
        # Verify constraint 2 (>=): should have excess and artificial
        self.assertEqual(tableau[2][2], 0)   # s1 not in second constraint
        self.assertEqual(tableau[2][3], -1)  # e2 (excess) in second
        self.assertEqual(tableau[2][4], 1)   # a2 (artificial) in second
    
    def test_adapter_objective_function_coefficients(self):
        """Test that objective function coefficients are correctly set"""
        obj_func = ObjectiveFunction([3, 2], isMax=True)
        constraints = [Constraint([1, 1], "<=", 4)]
        
        adapter = Adapter(obj_func, constraints)
        tableau = adapter.buildTable()
        
        # Verify objective function coefficients
        self.assertEqual(tableau[0][0], 3)   # x1 coefficient
        self.assertEqual(tableau[0][1], 2)   # x2 coefficient
        self.assertEqual(tableau[0][2], 0)   # s1 coefficient (slack has 0 cost)
        self.assertEqual(tableau[0][-1], 0)  # RHS should be 0 initially
    
    def test_adapter_minimization_problem(self):
        """Test Adapter with minimization (isMax=False)"""
        # Minimize: 4x1 + 3x2
        obj_func = ObjectiveFunction([4, 3], isMax=False)
        # Constraint: x1 + x2 >= 2
        constraints = [Constraint([1, 1], ">=", 2)]
        
        adapter = Adapter(obj_func, constraints)
        tableau = adapter.buildTable()
        
        # For minimization with artificial variables, M should be positive
        # (penalty for artificial variables is +M)
        self.assertTrue(tableau[0][3] > 0)  # a1 coefficient should be +M
    
    def test_adapter_constraint_rhs_values(self):
        """Test that constraint RHS values are correctly added"""
        obj_func = ObjectiveFunction([1, 1], isMax=True)
        constraints = [
            Constraint([1, 2], "<=", 8),
            Constraint([2, 1], "<=", 6),
        ]
        
        adapter = Adapter(obj_func, constraints)
        tableau = adapter.buildTable()
        
        # Verify RHS values in constraints
        self.assertEqual(tableau[1][-1], 8)  # First constraint RHS
        self.assertEqual(tableau[2][-1], 6)  # Second constraint RHS


if __name__ == '__main__':
    unittest.main()
