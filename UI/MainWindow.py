import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget
from UI.ProblemEntryView import ProblemEntryView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stack = QStackedWidget()

        self.problemEntryView = ProblemEntryView(self)

        self.stack.addWidget(self.problemEntryView)

        self.setCentralWidget(self.stack)
        self.setWindowTitle("Linear Programming Solver")
        self.resize(600, 400)

    def openProblemEntryView(self):
        self.problem_entry_view = ProblemEntryView(self)
        self.problem_entry_view.show()

    def changeView(self, view: QWidget):
        self.stack.addWidget(view)
        self.stack.setCurrentWidget(view)

    def changeViewToProblemEntry(self):
        self.stack.setCurrentWidget(self.problemEntryView)
        self.stack.removeWidget(self.stack.currentWidget())