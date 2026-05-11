from PySide6.QtWidgets import QMainWindow, QLabel, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout

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