from abc import abstractmethod


class SolverStrategy:
    @abstractmethod
    def solve(self, objectiveFunction, constraints):
        pass
