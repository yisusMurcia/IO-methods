import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.Constraint import Constraint
from UI.GraphView import GraphView
from PySide6.QtWidgets import QApplication


def test_graph_view_display():
    """Test GraphView with sample constraints and display the widget"""
    
    # Create sample constraints for a linear programming problem
    # Example: 2x + 3y <= 12
    constraint1 = Constraint([2, 3], "<=", 12)
    
    # Example: x - y <= 5
    constraint2 = Constraint([1, -1], ">=", 5)
    
    # Example: 3x + y <= 10
    constraint3 = Constraint([3, 0], "<=", 10)
    
    # Create list of constraints
    constraints = [constraint1, constraint2, constraint3]
    
    # Initialize QApplication
    app = QApplication(sys.argv)
    
    # Create GraphView with constraints
    graph_view = GraphView(constraints)
    
    # Display the widget
    graph_view.setWindowTitle("Linear Programming Graph")
    graph_view.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    test_graph_view_display()
