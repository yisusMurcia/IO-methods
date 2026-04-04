import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.Constraint import Constraint
from model.ObjectiveFunction import ObjectiveFunction
from model.tableau import Tableau

M = 1e6

class Adapter:
    def __init__(self, objectiveFunction, constraints):
        self.__objectiveFunction = objectiveFunction
        self.__constraints = constraints
        self.__varNames = objectiveFunction.varNames
        self.__cb = []

    def buildTable(self):
        constraints = [self.__constraints[i].coefficients for i in range(len(self.__constraints))]
        objectiveFunction = self.__objectiveFunction.coefficients

        for i in range(len(constraints)):
            if self.__constraints[i].relation == "<=":
                constraints[i].append(1)
                for j in range(len(constraints)):
                    if j != i:
                        constraints[j].append(0)
                self.__varNames.append(f"s{i+1}")
                objectiveFunction.append(0)
                self.__cb.append(f"s{i+1}")
            else:
                if self.__constraints[i].relation == ">=":
                    constraints[i].append(-1)
                    for j in range(len(constraints)):
                        if j != i:
                            constraints[j].append(0)
                    self.__varNames.append(f"e{i+1}")
                    objectiveFunction.append(0)

                #Artifical variable
                constraints[i].append(1)
                for j in range(len(constraints)):
                    if j != i:
                        constraints[j].append(0)
                self.__varNames.append(f"a{i+1}")
                objectiveFunction.append(-M if self.__objectiveFunction.isMax else M)
                self.__cb.append(f"a{i+1}")

        # add the values
        for i in range(len(constraints)):
            constraints[i].append(self.__constraints[i].value)
        objectiveFunction.append(0)

        return [objectiveFunction] + constraints
    
    def getTableau(self):
        return Tableau(self.buildTable())
    
    @property
    def varNames(self):
        return self.__varNames
    
    def getCb(self):
        return self.__cb