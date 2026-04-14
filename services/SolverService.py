import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from UI.ProblemEntryView import ProblemEntryView

class SolverService:
    def __init__(self):
        self.__problemEntryView = ProblemEntryView(self)
        