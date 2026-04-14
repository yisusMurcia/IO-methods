from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout
from UI.ObjectiveFunctionView import ObjectiveFunctionView

class ProblemEntryView(QMainWindow):
    def __init__(self, solverService):
        super().__init__()
        self.__solverService = solverService
        self.__variablesNames = []
        self.__ObjFuncView = ObjectiveFunctionView(self.__variablesNames)

        self.__variableNamesView = QLabel()
        self.__variableNamesButton = QPushButton("Add Constraint")
        self.__variableNamesButton.clicked.connect(self.addVariable)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.__variableNamesView)
        layout.addWidget(self.__variableNamesButton)
        layout.addWidget(self.__ObjFuncView)
        self.setCentralWidget(central_widget)


        self.setWindowTitle("Problem Entry")
        self.resize(400, 200)

    def addVariable(self):
        self.__variablesNames.append("x"+str(len(self.__variablesNames)+1))
        self.updateVariableNamesView()

    def updateVariableNamesView(self):
        self.__variableNamesView.setText(", ".join(self.__variablesNames))

    