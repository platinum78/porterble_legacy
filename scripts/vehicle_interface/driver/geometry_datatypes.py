import numpy as np

class Pose2D:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t

    def _check_type(self, obj):
        if type(self) != type(obj):
            raise TypeError("Improper operation between %s and %s." % (type(self), type(obj)))

    def __eq__(self, obj):
        self._check_type(obj)
        if (self.x, self.y, self.t) == (obj.x, obj.y, obj.t):
            return True
        return False
    
    def __add__(self, obj):
        self._check_type(obj)
        return Pose2D(self.x + obj.x, self.y + obj.y, self.t + obj.t)
    
    def __sub__(self, obj):
        self._check_type(obj)
        return Pose2D(self.x - obj.x, self.y - obj.y, self.t - obj.t)
    
    def __mul__(self, num):
        if type(num) not in [int, float]:
            raise TypeError("%s type given, while multiplication only supports scalar argument." % type(num))
        return Pose2D(self.x * num, self.y * num, self.t * num)
    
    def __div__(self, num):
        if type(num) not in [int, float]:
            raise TypeError("%s type given, while division only supports scalar argument." % type(num))
        return Pose2D(self.x / num, self.y / num, self.t / num)
    
    def __pow__(self, num):
        if type(num) not in [int, float]:
            raise TypeError("%s type given, while power only supports scalar argument." % type(num))
        return self.x ** 2 + self.y ** 2
    
    def __str__(self):
        return "Pose2D([" + self.x + ", " + self.y + ", " + self.z + "])"