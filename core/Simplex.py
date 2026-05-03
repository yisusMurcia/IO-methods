import sys
import os

from services.Adapter import Adapter
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.SolverStrategy import SolverStrategy
from model.tableau import Tableau

class SimplexStrategy(SolverStrategy):
    def __init__(self, tableau, isMax, varNames, cb):
        self.__tableau = Tableau(tableau, isMax)
        self.__varNames = varNames
        self.__cb = cb

    def __init__(self, tableau, varNames, cb):
        self.__tableau = tableau
        self.__varNames = varNames
        self.__cb = cb
    
    def __init__(self):
        self.__tableau = None
        self.__varNames = []
        self.__cb = []

    def setData(self, ObjectiveFunction, constraints):
        adapter = Adapter(ObjectiveFunction, constraints)
        adapter.buildTable()
        self.__tableau = adapter.getTableau()
        self.__varNames = adapter.varNames
        self.__cb = adapter.getCb()

    def solve(self, objectiveFunction, constraints):
        self.setData(objectiveFunction, constraints)
        while not self.__tableau.isOptimal():
            incoming = self.__tableau.getIncomingVariable()
            leaving = self.__tableau.getLeavingVariable(incoming)
            self.__cb[leaving - 1] = self.__varNames[incoming]
            self.__tableau.pivot(leaving, incoming)
        if not self.__tableau.isOptimal():
            return "No solution"
        else:
            coef = self.__tableau.getVariablesCoefficients()
            solution = "".join(f"{self.__cb[i]} = {coef[i]} " for i in range(len(coef)))
            return solution
