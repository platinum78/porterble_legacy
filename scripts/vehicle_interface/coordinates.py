import numpy as np

class Coordinate:
    def __init__(self, ref_frame, offset, rotation):
        """
        * Reference is an coordinate object.
        * Rotation should be given in radians.
        """
        self.ref_coord = ref_coord      # None, if the coordinate is fundamental one.
        self.rotation = rotation
    
    def generate_derived_coordinate(self, angle, offset):
        """
        Computes coordinate rotation, and returns new coordinate object.
        """
        coordinate = Coordinate(self, angle)
        return coordinate