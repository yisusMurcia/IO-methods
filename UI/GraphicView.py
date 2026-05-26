from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout
from model.Constraint import Constraint
from model.ObjectiveFunction import ObjectiveFunction
from UI.GraphView import GraphView
from core.GraphicMethodSensibilityAnalizer import GraphicMethodSensibilityAnalizer

class GraphicView(QMainWindow):
    def __init__(self, constraints: list[Constraint], objectiveFunction: ObjectiveFunction, optimalPoint: list[float] = None, optimalValue: float = None):
        super().__init__()
        self.__constraints = constraints
        self.__optimalVarsValues = optimalPoint
        self.__optimalVal = optimalValue
        self.__objectiveFunction = objectiveFunction
        self.__analysisBtn = QPushButton("Sensibility analysis")
        self.closeButton = QPushButton("<")
        valueView = QLabel(f"Optimal Value: {self.__optimalVal} \n with x1 {self.__optimalVarsValues[0]} and x2 {self.__optimalVarsValues[1]}") if self.__optimalVal is not None else QLabel("No optimal value")
        layout = QVBoxLayout()
        layout.addWidget(self.closeButton)
        if self.__optimalVal is not None and len(self.__optimalVarsValues) == 2:
            graphView = GraphView(self.__constraints)
            layout.addWidget(graphView)
        layout.addWidget(valueView)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)
        layout.addWidget(self.__analysisBtn)
        self.__analysisBtn.clicked.connect(lambda: self.sensitibilityAnalysis(layout))
        self.setWindowTitle("Graph View")
        self.resize(400, 300)


    def sensitibilityAnalysis(self, layout):
        analizer = GraphicMethodSensibilityAnalizer(self.__optimalVal, self.__optimalVarsValues, self.__constraints, self.__objectiveFunction.coefficients)
        analyzedVarsLabel = QLabel(analizer.analyzeVars())
        analyzedResourcesLabel = QLabel(analizer.analyzeResources())
        layout.addWidget(analyzedVarsLabel)
        layout.addWidget(analyzedResourcesLabel)
        self.__analysisBtn.setEnabled(False)