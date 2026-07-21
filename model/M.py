class M: #Form of Mx+ b
    def __init__(self): 
        self.__x = 1
        self.__b = 0

    @property
    def x(self):
        return self.__x
    
    @property
    def b(self):
        return self.__b
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            self.__b += other
        elif isinstance(other, M):
            self.__x += other.x
            self.__b += other.b
        return self
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            self.__b -= other
        elif isinstance(other, M):
            self.__x -= other.x
            self.__b -= other.b
        return self
    
    def __rsub__(self, other):
        self.__x = -self.x
        self.__b = - self.b
        return self.__add__(other)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            self.__b *= other
            self.__x *= other
        return self
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __ge__(self, other):
        if isinstance(other, (int, float)):
            return self.__x > 0
        elif isinstance(other, M):
            return self.x > other.x or (self.x == other.x and self.b >= other.b)
        return self
    
    def __gt__(self, other):
        if isinstance(other, (int, float)):
            return self.x > 0
        elif isinstance(other, M):
            return self.x > other.x or (self.x == other.x and self.b > other.b)
        return self
    
    def __lt__(self, other):
        if isinstance(other, (int, float)):
            return self.x < 0
        elif isinstance(other, M):
            return self.x < other.x or (self.x == other.x and self.b < other.b)
        return self
    
    def __le__(self, other):
        if isinstance(other, (int, float)):
            return self.x < 0
        elif isinstance(other, M):
            return self.x < other.x or (self.x == other.x and self.b <= other.b)
        return self
    
    def __neg__(self):
        self.__x = -self.x
        self.__b = -self.b
        return self