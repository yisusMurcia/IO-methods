from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QScrollArea

from UI.SimplexSensitiveAnalysisVew import SimplexSensitiveAnalysisView
from UI.VarValueView import VarValueView
from model.TableauCaretaker import TableauCaretaker
from model.tableau import Tableau

class SimplexResultView(QMainWindow):
    def __init__(self, varNames: list[str], careTaker: TableauCaretaker, isFeasiable: bool, cbList: list[str]):
        super().__init__()
        self.__varNames = varNames
        self.__tableau = careTaker.mementos[0]
        self.__tableauList = self.__tableau.tableau.tolist()
        self.__cb = cbList
        self.__sensitivityAnalysisBtn = QPushButton("Sensitivity Analysis")
        self.closeButton = QPushButton("<")

        self.__tableContainter = QWidget()
        self.__table_layout = QVBoxLayout(self.__tableContainter)
        self.__scroll_table_view = QScrollArea()


        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle("Simplex Result")
        self.resize(400, 300)

        layout.addWidget(self.closeButton)
        for table in careTaker.mementos:
            self.__table_layout.addWidget(self.createTable(table))

        self.__scroll_table_view.setWidget(self.__tableContainter)

        layout.addWidget(self.__scroll_table_view)



        if isFeasiable:
            layout.addWidget(VarValueView("Z", abs(self.__tableauList[0][-1])))
            for cb in self.__cb:
                if "x" in cb:
                    value = self.__tableauList[self.__cb.index(cb) + 1][-1]
                    layout.addWidget(VarValueView(cb, value))
            layout.addWidget(self.__sensitivityAnalysisBtn)
            self.__sensitivityAnalysisBtn.clicked.connect(lambda: self.operateSensitivityAnalysis(layout))
        else:
            layout.addWidget(QLabel("No feasible solution"))


    def createTable(self, tableau: Tableau)-> QTableWidget:
        tableauList = tableau.tableau.tolist()

        num_rows = len(tableauList) + 1  # +1 for header
        num_cols = len(tableauList[0]) + 1  # +1 for CB column
        table = QTableWidget(num_rows, num_cols)
        table.setRowCount(num_rows)
        table.setColumnCount(num_cols)

        table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only
        table.verticalHeader().setVisible(False)  # Hide row numbers
        table.horizontalHeader().setVisible(False)  # Hide column numbers

        # Set header row
        table.setItem(0, 0, QTableWidgetItem("CB"))
        for col in range(1, num_cols - 1):
            idx = col - 1
            if idx < len(self.__varNames):
                item = QTableWidgetItem(self.__varNames[idx])
            else:
                item = QTableWidgetItem(f"S{idx - len(self.__varNames) + 1}")
            table.setItem(0, col, item)

        #Last item for B
        table.setItem(0, num_cols - 1, QTableWidgetItem("B"))

        # Set CB column
        table.setItem(1, 0, QTableWidgetItem("z"))
        for i in range(len(self.__cb)):
            item = QTableWidgetItem(self.__cb[i])
            table.setItem(i + 2, 0, item)

        # Set data
        for i in range(len(self.__tableauList)):
            for j in range(len(self.__tableauList[0])):
                item = QTableWidgetItem(self.adjustValue(self.__tableauList[i][j]))
                table.setItem(i + 1, j + 1, item)

        return table
    
    def adjustValue(self, value) -> str:
        if value == int(value):
            return str(int(value))
        else:
            return str(value)
        
    def operateSensitivityAnalysis(self, layout: QVBoxLayout):
        analysisView = SimplexSensitiveAnalysisView(self.__tableau, self.__varNames, self.__cb)
        layout.addWidget(analysisView)
        self.__sensitivityAnalysisBtn.setEnabled(False)