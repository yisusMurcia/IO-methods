import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.ObjectiveFunction import ObjectiveFunction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox
from PySide6.QtGui import QDoubleValidator

class ObjectiveFunctionView(QWidget):
    def __init__(self, variableNames):
        super().__init__()
        self.__variableNames = variableNames
        self.__constraints = []
        self.__validator = QDoubleValidator()
        self.__validator.setNotation(QDoubleValidator.StandardNotation)
        
        for var in variableNames:
            self.addConstraint(var)

        self.__ObjectiveFunction = ObjectiveFunction(self.__constraints, True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.objectiveLabel = QLabel("Objective Function:")
        self.layout.addWidget(self.objectiveLabel)

        self.objectiveInput = QWidget()

        self.maxMinComboBox = QComboBox()
        self.maxMinComboBox.addItems(["Maximize", "Minimize"])
        self.layout.addWidget(self.maxMinComboBox)

    @property
    def variableNames(self):
        return self.__variableNames

    def addConstraint(self, constraint):
        line = QLineEdit()
        line.setPlaceholderText(f"Coefficient for {constraint}")
        line.setValidator(self.__validator)
        line.textChanged.connect(self.updateView)
        self.__constraints.append(line)
        self.__variableNames.append(constraint)
    
    def updateView(self):
        for i in range(len(self.__constraints)):
            self.objectiveInput.layout().addWidget(QLabel(f"{self.__variableNames[i]}:"))
            self.objectiveInput.layout().addWidget(self.__constraints[i])