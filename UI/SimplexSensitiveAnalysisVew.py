import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,  QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QDoubleValidator
from core.SimlexSensitivilityAnalyzer import SimlexSensitivilityAnalyzer
from model.tableau import Tableau

class SimplexSensitiveAnalysisView(QWidget):
    def __init__(self, tableau: Tableau, varNames: list[str], cb: list[int]):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.__newResourceZValue = QWidget()
        self.__newResourceZValue.setLayout(QHBoxLayout())
        self.__newResourceZValue.layout().addWidget(QLabel("New Resource Z Value:"))
        self.__newResourceZValueInput = QLineEdit()
        self.__newResourceZValueInput.setValidator(QDoubleValidator())
        self.__newResourceConstraints : list[QWidget] = []
        self.__newResourceConstraintsValue : list[QLineEdit] = []
        self.__newResourceAnalysis = QLabel("Input the coefficients of the new resource to analyze its impact on the objective function.")


        for i in range(len(cb)):
            constraintWidget = QWidget()
            constraintWidget.setLayout(QHBoxLayout())
            constraintWidget.layout().addWidget(QLabel(f"New Resource Coefficient for {varNames[cb[i]]}:"))
            constraintInput = QLineEdit()
            constraintInput.setValidator(QDoubleValidator())
            constraintWidget.layout().addWidget(constraintInput)
            self.__newResourceConstraints.append(constraintWidget)
            self.__newResourceConstraintsValue.append(constraintInput)

        self.__newResourceWidget = QWidget()
        self.__newResourceWidget.setLayout(QHBoxLayout())
        for constraintWidget in self.__newResourceConstraints:
            self.__newResourceWidget.layout().addWidget(constraintWidget)
        self.__newResourceWidget.layout().addWidget(self.__newResourceZValue)
        self.__newResourceWidget.layout().addWidget(self.__newResourceAnalysis)

        self.__analyzer = SimlexSensitivilityAnalyzer(tableau, varNames, cb)
        self.__basicVarsAnalysis = QLabel(self.__analyzer.analyzeBasicVars())
        self.__nonBasicVarsAnalysis = QLabel(self.__analyzer.analyzeNonBasicVars())
        self.__resourcesAnalysis = QLabel(self.__analyzer.analyzeResources())
        self.__analyzeNewResourceBtn = QPushButton("Analyze New Resource")
        self.__analyzeNewResourceBtn.clicked.connect(self.analyzeNewResource)
        self.layout.addWidget(self.__basicVarsAnalysis)
        self.layout.addWidget(self.__nonBasicVarsAnalysis)
        self.layout.addWidget(self.__resourcesAnalysis)
        self.layout.addWidget(self.__analyzeNewResourceBtn)

    def analyzeNewResource(self):
        resourceData = [float(self.__newResourceZValueInput.text())]
        for constraintInput in self.__newResourceConstraintsValue:
            resourceData.append(float(constraintInput.text()))
        isBeneficial = self.__analyzer.analyzeNewResource(resourceData)
        resultText = "The new resource is beneficial to the objective function." if isBeneficial else "The new resource is not beneficial to the objective function."
        self.__newResourceAnalysis.setText(resultText)

