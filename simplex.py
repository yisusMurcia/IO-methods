import numpy as np
class Simplex:
    _isMax = True
    _z = []
    _table = []
    _cb = []

    def __init__(self, isMax, z, restrictions):
        self._isMax = isMax
        self._z = z
        self._table = restrictions
        self._setCb(restrictions)


    @property
    def cb(self):
        return self._cb

    def _setCb(self, restrictions):
        self._cb = np.zeros(len(restrictions))
        for i in range(len(restrictions)):
            print('i', i)
            for j in range(len(restrictions[i]) - 1, -1, -1):
                print('j', j)
                if restrictions[i][j] == 1:
                    self._cb[i] = j
                    break
