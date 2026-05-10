from PySide6.QtWidgets import QWidget, QHBoxLayout,  QLabel

class VarValueView(QWidget):
    def __init__(self, varName: str, value: float):
        super().__init__()
        self.__varName = varName
        self.__value = value

        self.label = QLabel(f"{varName} = {self.adjustValue()}")

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)

    def adjustValue(self) -> str:
        if self.__value == int(self.__value):
            return str(int(self.__value))
        else:
            return str(self.__value)