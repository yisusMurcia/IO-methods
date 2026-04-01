import numpy as np
from simplex import Simplex
z=[3,5, 0, 0]
# restriction format: x1,x2, slack/excess/artificial..., RHS
# we'll choose restrictions where extra vars start at index3 and 4
restrictions=[[1,0,1,0,16],[0,2,0,1,0,10]]
# Note _buildTable behavior: j>len(z) (strict) so j>=3 will be extra vars
s= Simplex(True,z,restrictions)
print('cb', s._cb)