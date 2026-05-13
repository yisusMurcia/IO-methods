import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.tableau import Tableau
import numpy as np

class SimlexSensitivilityAnalyzer:
    def __init__(self, tableau: Tableau, varNames: list[str], cb: list[int]):
        self.__tableau: Tableau = tableau
        self.__varNames: list[str] = varNames
        self.__cb: list[int] = cb

    def analyzeBasicVars(self)->str:
        analysis = "Sensitivity Analysis of Basic Variables:\n"
        for i in range(self.__cb):
            if(self.__varNames[self.__cb[i]].startswith("x")):
                analysis += self.__analizeBasicVar(i) + "\n"
        return analysis
    
    def analyzeNonBasicVars(self)->str:
        analysis = "Sensitivity Analysis of Non-Basic Variables:\n"
        for i in range(len(self.__varNames)):
            if(i not in self.__cb and self.__varNames[i].startswith("x")):
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

        for i in range(startIndex, self.__cb):
            if(not self.__varNames[self.__cb[i]].startswith("x")):
                analysis += self.__analyzeResource(i, inverseMatrix) + "\n"
        return analysis
    
    def analyzeNewResource(self, resourceData: list[float])->bool: #ResourceData [z, coinstraint coefficients...]
        inverseMatrix = self.__tableau.getInverseMatrix(0)
        zInInverseMatrix =  inverseMatrix[0]
        zVal =  resourceData[0] + zInInverseMatrix.dot(resourceData[1:])
        return zVal > 0

    def __analizeBasicVar(self, varIndex)->str:
        varName = self.__varNames[varIndex]
        #Get var row
        varRow = self.__tableau.getVariableRow(varIndex +1) #+1 because the first row is the z row
        zRow = self.__tableau.getZRow()

        negativeCoefficients = [zRow[i]/varRow[i] for i in range(len(varRow)-1) if varRow[i] < 0]
        positiveCoefficients = [zRow[i]/varRow[i] for i in range(len(varRow)-1) if varRow[i] > 0]

        return f"{varName}: {max(negativeCoefficients) if negativeCoefficients else '- ∞'} <= d <= {min(positiveCoefficients) if positiveCoefficients else '∞'}\n"
    
    def __analyzeNonBasicVar(self, varIndex)->str:
        varName = self.__varNames[varIndex]
        zRow = self.__tableau.getZRow()
        return f"{varName}: d {"<" if self.__tableau.isMax else ">"}= {- zRow[varIndex]}\n"
    
    def __analyzeResource(self, varIndex: int, inverseMatrix: np.ndarray[float])->str:
        varName = self.__varNames[varIndex]
        varColumn = self.__tableau.getColumn(varIndex) # Get the column for the resource variable
        zRow = self.__tableau.getZRow()

        negativeCoefficients = [zRow[i]/varColumn[i] for i in range(len(varColumn)-1) if varColumn[i] < 0]
        positiveCoefficients = [zRow[i]/varColumn[i] for i in range(len(varColumn)-1) if varColumn[i] > 0]

        return f"{varName}: {max(negativeCoefficients) if negativeCoefficients else '- ∞'} <= d <= {min(positiveCoefficients) if positiveCoefficients else '∞'}\n"
