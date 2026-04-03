import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.tableau import Tableau

class Simplex:
    def __init__(self, tableau, isMax, varNames, cb):
        self.__tableau = Tableau(tableau, isMax)
        self.__varNames = varNames
        self.__cb = cb

    def getSolution(self):
        while not self.__tableau.isOptimal():
            incoming = self.__tableau.getIncomingVariable()
            leaving = self.__tableau.getLeavingVariable(incoming)
            self.__cb[leaving - 1] = self.__varNames[incoming]
            self.__tableau.pivot(leaving, incoming)
        coef = self.__tableau.getVariablesCoefficients()
        solution = "".join(f"{self.__cb[i]} = {coef[i]} " for i in range(len(coef)))
        return solution