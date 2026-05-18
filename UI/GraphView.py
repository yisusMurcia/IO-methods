import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.Constraint import Constraint
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np

class GraphView(QWidget):
    def __init__(self, constraints: list[Constraint]):
        super().__init__()
        self.constraints = constraints
        self.__graph = Figure()
        self.__graphCanva = FigureCanvasQTAgg(self.__graph)
        layout = QVBoxLayout()
        layout.addWidget(self.__graphCanva)
        self.setLayout(layout)
        self.plot()

    def plot(self):
        xMax = self.getMaxX() * 1.5
        yMax = self.getMaxY() * 1.5
        ax = self.__graph.add_subplot(111)
        ax.set_xlim(0, xMax)
        ax.set_ylim(0, yMax)
        for constraint in self.constraints:
            adaptedConstraint = self.__adaptContraint(constraint)
            if adaptedConstraint is not None:
                m, b = adaptedConstraint
                x = np.linspace(0, xMax, 100)
                y = m * x + b
                ax.plot(x, y, label=f"{constraint.coefficients[0]}x {(f'+{constraint.coefficients[1]}' if constraint.coefficients[1] > 0 else f'-{abs(constraint.coefficients[1])}')}y {constraint.relation} {constraint.value}")

                if(constraint.relation == "<=" and constraint.coefficients[1] > 0) or (constraint.relation == ">=" and constraint.coefficients[1] < 0):
                    ax.fill_between(x, y, 0, alpha=0.3)
                elif(constraint.relation == "<=" and constraint.coefficients[1] < 0) or (constraint.relation == ">=" and constraint.coefficients[1] > 0):
                    ax.fill_between(x, y, yMax, alpha=0.3)
            else:
                x = constraint.value / constraint.coefficients[0]
                ax.axvline(x=x, label=f"{constraint.coefficients[0]}x {constraint.relation} {constraint.value}")
                if (constraint.relation == "<=" and constraint.coefficients[0] > 0) or (constraint.relation == ">=" and constraint.coefficients[0] < 0):
                    ax.fill_betweenx(np.linspace(0, 0, 100), x, x2=xMax, alpha=0.3)
                elif (constraint.relation == "<=" and constraint.coefficients[0] < 0) or (constraint.relation == ">=" and constraint.coefficients[0] > 0):
                    ax.fill_betweenx(np.linspace(0, yMax, 100), x, x2=0, alpha=0.3)
        ax.legend()
        self.__graphCanva.draw()

    def __adaptContraint(self, constraint: Constraint)->list[float]: #m, b
        if constraint.coefficients[1] != 0:
            m = -constraint.coefficients[0] / constraint.coefficients[1]
            b = constraint.value / constraint.coefficients[1]
            return [m, b]
        else:
            return None
    def getMaxX(self)->float:
        maxX = 0
        for constraint in self.constraints:
            if constraint.coefficients[0] != 0:
                x = constraint.value / constraint.coefficients[0]
                if x > maxX:
                    maxX = x
        return maxX
    
    def getMaxY(self)->float:
        maxY = 0
        for constraint in self.constraints:
            if constraint.coefficients[1] != 0:
                y = constraint.value / constraint.coefficients[1]
                if y > maxY:
                    maxY = y
        return maxY