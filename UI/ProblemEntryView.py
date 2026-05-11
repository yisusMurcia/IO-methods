from __future__ import annotations
from PySide6.QtWidgets import QLabel, QMessageBox, QPushButton, QWidget, QVBoxLayout
from UI.ConstraitView import ConstraintView
from UI.ObjectiveFunctionView import ObjectiveFunctionView
from services.SolverService import SolverService

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from MainWindow import MainWindow


class ProblemEntryView(QWidget):
    def __init__(self, mainWindow: MainWindow):
        super().__init__()
        self.__solverService: SolverService = SolverService(self)
        self.__variablesNames = ["x1"]
        self.__mainWindow = mainWindow
        self.__ObjFuncView: ObjectiveFunctionView = ObjectiveFunctionView(self.__variablesNames)
        self.__constraintsViews: list[ConstraintView] = [ConstraintView(self.__variablesNames)]

        self.__constraintLayout = QWidget()
        self.__constraintLayout.setLayout(QVBoxLayout())
        self.__constraintLayout.layout().addWidget(self.__constraintsViews[0])

        self.__variableNamesView = QLabel()
        self.__variableNamesButton = QPushButton("Add variable")
        self.__addConstraintButton = QPushButton("Add constraint")
        self.__variableNamesButton.clicked.connect(self.addVariable)
        self.__addConstraintButton.clicked.connect(self.addConstraint)

        self.__solveButton = QPushButton("Solve")
        self.__solveButton.clicked.connect(self.solveProblem)


        central_widget = QWidget()

        layout = QVBoxLayout(central_widget)
        self.setLayout(layout)
        layout.addWidget(self.__variableNamesView)
        layout.addWidget(self.__ObjFuncView)
        layout.addWidget(self.__constraintLayout)
        layout.addWidget(self.__variableNamesButton)
        layout.addWidget(self.__addConstraintButton)
        layout.addWidget(self.__solveButton)


        self.setWindowTitle("Problem Entry")
        self.resize(400, 200)

    def addVariable(self):
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
        self.__mainWindow.changeView(solution)
