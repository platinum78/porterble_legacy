import numpy as np

class State2D:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t

    def __eq__(self, obj):
        if type(obj) != type(self):
            raise TypeError("Improper comparison between %s and %d." % \
                            (type(obj), type(self)))
        if self.x == obj.x:
            if self.y == obj.y:
                if self.t == self.t:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    
    def __str__(self):
        return "State2D([" + self.x + ", " + self.y + ", " + self.z + "])"