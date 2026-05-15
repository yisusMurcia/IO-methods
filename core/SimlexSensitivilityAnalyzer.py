import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.tableau import Tableau
import numpy as np

class SimlexSensitivilityAnalyzer:
    def __init__(self, tableau: Tableau, varNames: list[str], cb: list[str]):
        self.__tableau: Tableau = tableau
        self.__varNames: list[str] = varNames
        self.__cb: list[str] = cb

    def analyzeVars(self)->str:
        analysis = "Sensitivity Analysis of Variables:\n"
        for i in self.__varNames:
            if not i.startswith("x"):
                break
            if i in self.__cb:
                analysis += self.__analyzeBasicVar(self.__cb.index(i)) + "\n"
            else:
                analysis += self.__analyzeNonBasicVar(i) + "\n"
        return analysis
    
    def analyzeResources(self)->str:
        analysis = "Sensitivity Analysis of Resources:\n"
        startIndex = 0
        for i in range(len(self.__varNames)):
            if not self.__varNames[i].startswith("x"):
                startIndex = i
                break
        inverseMatrix = self.__tableau.getInverseMatrix(startIndex)

        for i in range(len(self.__cb)):
                analysis += self.__analyzeResource(i, inverseMatrix) + "\n"
        return analysis
    
    def analyzeNewResource(self, resourceData: list[float])->bool: #ResourceData [z, coinstraint coefficients...]
        startIndex = 0
        for i in range(len(self.__varNames)):
            if not self.__varNames[i].startswith("x"):
                startIndex = i
                break
        inverseMatrix = self.__tableau.getInverseMatrix(startIndex)
        zInInverseMatrix: np.ndarray[float] =  inverseMatrix[0]
        zVal =  resourceData[0] + zInInverseMatrix.dot(resourceData[1:])
        return zVal <= 0

    def __analyzeBasicVar(self, varIndex)->str:
        varName = self.__cb[varIndex]
        #Get var row
        varRow = self.__tableau.getVariableRow(varIndex +1) #+1 because the first row is the z row
        zRow = self.__tableau.getZRow()
        negativeCoefficients = [zRow[i]/varRow[i] for i in range(len(varRow)-1) if varRow[i] < 0]
        positiveCoefficients = [zRow[i]/varRow[i] for i in range(len(varRow)-1) if varRow[i] > 0]

        return f"{varName} + d: {min(positiveCoefficients) if positiveCoefficients else '- ∞'} <= d <= {abs((min(negativeCoefficients))) if negativeCoefficients else '∞'}\n"
    
    def __analyzeNonBasicVar(self, varIndex)->str:
        varName = self.__varNames[varIndex]
        zRow = self.__tableau.getVariablesCoefficients()
        return f"{varName} + d: d {"<" if self.__tableau.isMax else ">"}= {- zRow[varIndex]}\n"
    
    def __analyzeResource(self, cbIndex: int, inverseMatrix: np.ndarray[float])->str:
        index = self.__varNames.index(self.__cb[cbIndex])
        varColumn = inverseMatrix[1:, cbIndex]
        varValue: float = self.__tableau.getVariablesCoefficients()

        negativeCoefficients = [varValue[i]/varColumn[i] * -1 for i in range(len(varColumn)) if varColumn[i] < 0]
        positiveCoefficients = [varValue[i] / varColumn[i] * -1 for i in range(len(varColumn)) if varColumn[i] > 0]

        return f"B{cbIndex + 1} + d: {max(positiveCoefficients) if positiveCoefficients else '- ∞'} <= d <= {abs(min(negativeCoefficients)) if negativeCoefficients else '∞'}\n"
