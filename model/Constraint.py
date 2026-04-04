class Constraint:
    def __init__(self, coefficients, relation, value):
        self.__coefficients = coefficients
        self.__relation = relation
        self.__value = value

    @property
    def coefficients(self):
        return self.__coefficients
    
    @property
    def relation(self):
        return self.__relation
    
    @property
    def value(self):
        return self.__value