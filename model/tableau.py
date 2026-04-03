import numpy as np
class Tableau:
    def __init__(self, tableau, isMax):
        self.__tableau = np.array(tableau, dtype=float) #Last row is the objective function, the rest are the constraints
        if not isMax:
            self.__tableau[-1, :-1] *= -1

    @property
    def tableau(self):
        return self.__tableau
    
    def pivot(self, row, col):
        pivot = self.__tableau[row, col]
        self.__tableau[row] /= pivot

        for i in range(len(self.__tableau)):
            if i != row:
                factor = self.__tableau[i, col]
                self.__tableau[i] -= factor * self.__tableau[row]

    def getIncomingVariable(self):
        zRow = self.__tableau[0]
        return np.argmax(zRow[:-1])
    
    def getLeavingVariable(self, incomingCol):
        col = self.__tableau[1:, incomingCol]
        b = self.__tableau[1:, -1]

        ratios = np.where((col > 0), b / col, np.inf)
        return 1 + np.argmin(ratios)
    
    def isOptimal(self):
        zRow = self.__tableau[0]
        return np.all(zRow[:-1] <= 0)
    
    def getVariablesCoefficients(self):
        return self.__tableau[1:, -1]