from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout
from model.Constraint import Constraint
from UI.GraphView import GraphView

class GraphicView(QMainWindow):
    def __init__(self, constraints: list[Constraint], optimalPoint: list[float] = None, optimalValue: float = None):
        super().__init__()
        self.__constraints = constraints
        self.__optimalVarsValues = optimalPoint
        self.__optimalVal = optimalValue
        valueView = QLabel(f"Optimal Value: {self.__optimalVal} with x1 {self.__optimalVarsValues[0]} and x2 {self.__optimalVarsValues[1]}") if self.__optimalVal is not None else QLabel("No optimal value")
        layout = QVBoxLayout()
        if self.__optimalVal is not None and len(self.__optimalVarsValues) == 2:
            graphView = GraphView(self.__constraints)
            layout.addWidget(graphView)
        layout.addWidget(valueView)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)
        self.setWindowTitle("Graph View")
        self.resize(400, 300)