import sys
import os
import copy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from model.tableau import Tableau
class TableauCaretaker:
    def __init__(self) -> None:
        self.mementos: list[Tableau] = []

    def saveMemento(self, tableau: Tableau):
        memento = copy.deepcopy(tableau)
        self.mementos.insert(0, memento)