import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.ObjectiveFunction import ObjectiveFunction
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,  QLabel, QLineEdit, QComboBox
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
        label = QLabel(f"{varName}:")
        line = QLineEdit()
        line.setFixedWidth(60)
        line.setPlaceholderText(varName)
        line.setValidator(self.__validator)
        self.__LineEdits.append(line)
        self.constraintInput.layout().addWidget(label)
        self.constraintInput.layout().addWidget(line)
