from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout
from UI.ConstraitView import ConstraintView
from UI.ObjectiveFunctionView import ObjectiveFunctionView

class ProblemEntryView(QMainWindow):
    def __init__(self, solverService):
        super().__init__()
        self.__solverService = solverService
        self.__variablesNames = ["x1"]
        self.__ObjFuncView = ObjectiveFunctionView(self.__variablesNames)
        self.__constraintsViews = [ConstraintView(self.__variablesNames)]

        self.__constraintLayout = QWidget()
        self.__constraintLayout.setLayout(QVBoxLayout())
        self.__constraintLayout.layout().addWidget(self.__constraintsViews[0])

        self.__variableNamesView = QLabel()
        self.__variableNamesButton = QPushButton("Add variable")
        self.__addConstraintButton = QPushButton("Add constraint")
        self.__variableNamesButton.clicked.connect(self.addVariable)
        self.__addConstraintButton.clicked.connect(self.addConstraint)
        central_widget = QWidget()

        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.__variableNamesView)
        layout.addWidget(self.__ObjFuncView)
        layout.addWidget(self.__constraintLayout)
        layout.addWidget(self.__variableNamesButton)
        layout.addWidget(self.__addConstraintButton)
        self.setCentralWidget(central_widget)


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
