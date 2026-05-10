from PySide6.QtWidgets import QMainWindow, QLabel, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout

from UI.VarValueView import VarValueView

class SimplexResultView(QMainWindow):
    def __init__(self, varNames: list[str], tableau: list[list[float]], isFeasiable: bool, cb: list[str]):
        super().__init__()
        self.__varNames = varNames
        self.__tableau = tableau
        self.__cb = cb

        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle("Simplex Result")
        self.resize(400, 300)

        layout.addWidget(self.createTable())

        if isFeasiable:
            layout.addWidget(VarValueView("Z", abs(self.__tableau[0][-1])))
            for cb in self.__cb:
                if "x" in cb:
                    varIndex = int(cb[1:]) - 1
                    value = self.__tableau[self.__cb.index(cb) + 1][-1]
                    layout.addWidget(VarValueView(cb, value))
        else:
            layout.addWidget(QLabel("No feasible solution"))


    def createTable(self)-> QTableWidget:
        num_rows = len(self.__tableau) + 1  # +1 for header
        num_cols = len(self.__tableau[0]) + 1  # +1 for CB column
        table = QTableWidget(num_rows, num_cols)
        table.setRowCount(num_rows)
        table.setColumnCount(num_cols)

        # Set header row
        table.setItem(0, 0, QTableWidgetItem("CB"))
        for col in range(1, num_cols):
            idx = col - 1
            if idx < len(self.__varNames):
                item = QTableWidgetItem(self.__varNames[idx])
            else:
                item = QTableWidgetItem(f"S{idx - len(self.__varNames) + 1}")
            table.setItem(0, col, item)

        # Set CB column
        table.setItem(1, 0, QTableWidgetItem("z"))
        for i in range(1, len(self.__cb) + 1):
            item = QTableWidgetItem(self.__cb[i - 1])
            table.setItem(i + 1, 0, item)

        # Set data
        for i in range(len(self.__tableau)):
            for j in range(len(self.__tableau[0])):
                item = QTableWidgetItem(self.adjustValue(self.__tableau[i][j]))
                table.setItem(i + 1, j + 1, item)

        return table
    
    def adjustValue(self, value) -> str:
        if value == int(value):
            return str(int(value))
        else:
            return str(value)