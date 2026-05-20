import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.GraphicMethodSensibilityAnalizer import GraphicMethodSensibilityAnalizer
from model.Constraint import Constraint


class TestGraphicMethodSensitivityAnalyzer(unittest.TestCase):
    def test_rhs_range_respects_non_negative_axes(self):
        constraints = [
            Constraint([1, 0.25], '<=', 160),
            Constraint([2.5, 4], '<=', 800),
            Constraint([2, 1.5], '<=', 360),
            Constraint([0, 0.2], '<=', 50)
        ]
        analyzer = GraphicMethodSensibilityAnalizer(
            53000,
            [150, 40],
            constraints,
            [300, 200]
        )

        analysis = analyzer.analyzeResources()

        self.assertIn("Constraint 1 + d: -62.35294117647059 <= d <= 20.0", analysis)
        self.assertIn("Constraint 3 + d: -40.0 <= d <= 78.51851851851852", analysis)


if __name__ == '__main__':
    unittest.main()
