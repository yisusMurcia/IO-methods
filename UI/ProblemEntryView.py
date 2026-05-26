from __future__ import annotations
from PySide6.QtWidgets import QHBoxLayout, QLabel, QComboBox, QPushButton, QWidget, QVBoxLayout
from UI.ConstraitView import ConstraintView
from UI.ObjectiveFunctionView import ObjectiveFunctionView
from core.Simplex import SimplexStrategy
from core.graphicalMethodSolver import GraphicalMethodSolver
from services.SolverService import SolverService

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from MainWindow import MainWindow


class ProblemEntryView(QWidget):
    def __init__(self, mainWindow: MainWindow):
        super().__init__()

        self.__solverService: SolverService = SolverService()
        self.__variablesNames = ["x1"]
        self.__mainWindow = mainWindow
        self.__ObjFuncView: ObjectiveFunctionView = ObjectiveFunctionView(self.__variablesNames)
        self.__constraintsViews: list[ConstraintView] = [ConstraintView(self.__variablesNames)]

        self.__constraintLayout = QWidget()
        self.__constraintLayout.setLayout(QVBoxLayout())
        self.__constraintLayout.layout().addWidget(self.__constraintsViews[0])

        self.__variableNamesView = QLabel()
        self.__addConstraintButton = QPushButton("Add constraint")
        self.__addVariableButton = QPushButton("Add variable")
        self.__addVariableButton.clicked.connect(self.addVariable)
        self.__addConstraintButton.clicked.connect(self.addConstraint)

        self.__addWidget = QWidget()
        self.__addWidget.setLayout(QHBoxLayout())
        self.__addWidget.layout().addWidget(self.__addVariableButton)
        self.__addWidget.layout().addWidget(self.__addConstraintButton)

        self.__strategySelection = QComboBox()
        self.__strategySelection.addItems(["Graphical Method", "Simplex Method (Big M)"])
        self.__strategySelection.currentTextChanged.connect(self.defineStrategy)
        self.__solveButton = QPushButton("Solve")
        self.__solveButton.clicked.connect(self.solveProblem)

        self.__solveWidget = QWidget()
        self.__solveWidget.setLayout(QHBoxLayout())
        self.__solveWidget.layout().addWidget(self.__strategySelection)
        self.__solveWidget.layout().addWidget(self.__solveButton)


        central_widget = QWidget()

        layout = QVBoxLayout(central_widget)
        self.setLayout(layout)
        layout.addWidget(self.__variableNamesView)
        layout.addWidget(self.__ObjFuncView)
        layout.addWidget(self.__constraintLayout)
        layout.addWidget(self.__addWidget)
        layout.addWidget(self.__solveWidget)


        self.setWindowTitle("Problem Entry")
        self.resize(400, 200)

    def addVariable(self):
        if(len(self.__variablesNames) == 2):
            self.__strategySelection.setCurrentText("Simplex Method (Big M)")
            self.__strategySelection.setEnabled(False)
        varname: str = "x"+str(len(self.__variablesNames)+1)
        self.__variablesNames.append(varname)
        self.__ObjFuncView.addVariable(varname)
        self.updateVariableNamesView()
        for constraintView in self.__constraintsViews:
            constraintView.addVariable(varname)

    def updateVariableNamesView(self):
        self.__variableNamesView.setText("Variables: "+", ".join(self.__variablesNames))

    def addConstraint(self):
        constraintView = ConstraintView(self.__variablesNames)
        self.__constraintsViews.append(constraintView)
        self.__constraintLayout.layout().addWidget(constraintView)

    def solveProblem(self):
        objectiveFunction = self.__ObjFuncView.buildObjectiveFunction()
        constraints = [constraintView.buildConstraint() for constraintView in self.__constraintsViews]
        solution = self.__solverService.solve(objectiveFunction, constraints)
        solution.closeButton.clicked.connect(lambda: self.__mainWindow.changeViewToProblemEntry())
        self.__mainWindow.changeView(solution)

    def defineStrategy(self, strategy: str):
        if strategy == "Graphical Method":
            self.__solverService.setSolverStrategy(GraphicalMethodSolver())
        elif strategy == "Simplex Method (Big M)":
            self.__solverService.setSolverStrategy(SimplexStrategy())
