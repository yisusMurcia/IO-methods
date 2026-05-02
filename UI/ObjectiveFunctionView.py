import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.ObjectiveFunction import ObjectiveFunction
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,  QLabel, QLineEdit, QComboBox
from PySide6.QtGui import QDoubleValidator

class ObjectiveFunctionView(QWidget):
    def __init__(self, variableNames):
        super().__init__()
        self.__variableNames = []
        self.__LineEdits = []
        self.__validator = QDoubleValidator()
        

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.objectiveInput = QWidget()
        self.objectiveInput.setLayout(QHBoxLayout())

        self.maxMinComboBox = QComboBox()
        self.maxMinComboBox.addItems(["Maximize", "Minimize"])
        self.layout.addWidget(self.objectiveInput)
        self.layout.addWidget(self.maxMinComboBox)

        for varName in variableNames:
            self.addVariable(varName)


    def addVariable(self, varName):
        self.__variableNames.append(varName)
        label = QLabel(f"{varName}:")
        line = QLineEdit()
        line.setFixedWidth(60)
        line.setPlaceholderText(varName)
        line.setValidator(self.__validator)
        self.__LineEdits.append(line)
        self.objectiveInput.layout().addWidget(label)
        self.objectiveInput.layout().addWidget(line)

    def buildObjectiveFunction(self):
        coefficients = []
        for lineEdit in self.__LineEdits:
            text = lineEdit.text()
            if text == "":
                coefficients.append(0.0)
            else:
                coefficients.append(float(text))
        isMaximize = self.maxMinComboBox.currentText() == "Maximize"
        return ObjectiveFunction(coefficients, isMaximize)