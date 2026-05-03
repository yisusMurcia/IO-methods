import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.Constraint import Constraint
from PySide6.QtWidgets import QWidget, QHBoxLayout,  QLabel, QLineEdit, QComboBox
from PySide6.QtGui import QDoubleValidator

class ConstraintView(QWidget):
    def __init__(self, variableNames):
        super().__init__()
        self.__variableNames = []
        self.__LineEdits = []
        self.__validator = QDoubleValidator()
        self.__limitValueEdit = QLineEdit()
        self.__limitValueEdit.setFixedWidth(60)
        self.__limitValueEdit.setPlaceholderText("Value")
        self.__limitValueEdit.setValidator(self.__validator)
        

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.constraintInput = QWidget()
        self.constraintInput.setLayout(QHBoxLayout())

        self.lessGreaterComboBox = QComboBox()
        self.lessGreaterComboBox.addItems(["<=", ">=", "="])
        self.lessGreaterComboBox.setFixedWidth(60)
        self.layout.addWidget(self.constraintInput)
        self.layout.addWidget(self.lessGreaterComboBox)
        self.layout.addWidget(self.__limitValueEdit)

        for varName in variableNames:
            self.addVariable(varName)


    def addVariable(self, varName):
        self.__variableNames.append(varName)
        label = QLabel(f"{varName}")
        line = QLineEdit()
        line.setFixedWidth(60)
        line.setPlaceholderText(varName)
        line.setValidator(self.__validator)
        self.__LineEdits.append(line)
        if(varName != self.__variableNames[0]):
            self.constraintInput.layout().addWidget(QLabel("+"))
        self.constraintInput.layout().addWidget(line)
        self.constraintInput.layout().addWidget(label)

    def buildConstraint(self):
        coefficients = []
        for lineEdit in self.__LineEdits:
            text = lineEdit.text()
            if text == "":
                coefficients.append(0.0)
            else:
                coefficients.append(float(text))
        limitValueText = self.__limitValueEdit.text()
        limitValue = float(limitValueText) if limitValueText != "" else 0.0
        relation = self.lessGreaterComboBox.currentText()
        return Constraint(coefficients, relation, limitValue)
