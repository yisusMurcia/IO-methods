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
        from UI.ProblemEntryView import ProblemEntryView
        self.problem_entry_view = ProblemEntryView(self)
        self.problem_entry_view.show()

    def changeView(self, view: QWidget):
        self.stack.addWidget(view)
        self.stack.setCurrentWidget(view)