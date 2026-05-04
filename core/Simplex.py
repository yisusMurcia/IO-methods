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
        iterations = 0
        while not self.__tableau.isOptimal() and iterations < 1000:  # Prevent infinite loops
            incoming = self.__tableau.getIncomingVariable()
            leaving = self.__tableau.getLeavingVariable(incoming)
            self.__cb[leaving - 1] = self.__varNames[incoming]
            self.__tableau.pivot(leaving, incoming)
            iterations += 1
        
        coef = self.__tableau.getVariablesCoefficients()
        if not self.__checkFasiability(coef) or iterations == 1000:
            return "No solution"
        else:
            solution = "".join(f"{self.__cb[i]} = {coef[i]} " for i in range(len(coef)))
            solution += f"\nOptimal value: {abs(self.__tableau.getObjectiveFunctionValue())}"
            return solution
        
    def __checkFasiability(self, coefficients):
        return all(coef >= 0 for coef in coefficients) and not any("a" in self.__cb[i] for i in range(len(coefficients)))
