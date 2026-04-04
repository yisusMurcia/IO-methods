class ObjectiveFunction:
    def __init__(self, coefficients, isMax):
        self.__coefficients = coefficients
        self.__isMax = isMax
        self.__varNames = [f"x{i+1}" for i in range(len(coefficients))]

    @property
    def coefficients(self):
        return self.__coefficients
    @property
    def isMax(self):
        return self.__isMax
    @property
    def varNames(self):
        return self.__varNames