import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.Constraint import Constraint
from UI.GraphView import GraphView
from PySide6.QtWidgets import QApplication


def test_graph_view_display():
    """Test GraphView with sample constraints and display the widget"""
    
    # Create sample constraints for the tables-and-chairs maximization problem
    # Materials used per unit:
    #   Table  (x1): 1 m^2 wood, 2.5 m pipe, 2 hr labor, 0 kg foam
    #   Chair  (x2): 0.25 m^2 wood, 4 m pipe, 1.5 hr labor, 0.2 kg foam
    # Available resources:
    #   wood 160, pipe 800, labor 360, foam 50
    constraint1 = Constraint([1, 0.25], "<=", 160)
    constraint2 = Constraint([2.5, 4], "<=", 800)
    constraint3 = Constraint([2, 1.5], "<=", 360)
    constraint4 = Constraint([0, 0.2], "<=", 50)

    # Create list of constraints
    constraints = [constraint1, constraint2, constraint3, constraint4]
    
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
