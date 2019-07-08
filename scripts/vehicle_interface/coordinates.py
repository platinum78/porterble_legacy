import numpy as np

class Coordinate:
    def __init__(self, ref_coord, rotation, ref_global_rotation=None, is_static=False, is_global=False):
        """
        * Reference is an coordinate object.
        * Rotation should be given in radians.
        * is_static: True if reference, False if not.
        * is_global: True if global, False if not.
        """
        self.ref_coord = ref_coord      # None, if the coordinate is fundamental one.
        self.rotation = rotation
        self.is_static = is_static
        self.is_global = is_global

        if ref_global_rotation == None:
            self.rotation_ = self.
    
    def generate_rotated_coordinate(self, angle):
        """
        Computes coordinate rotation, and returns new coordinate object.
        """
        coordinate = Coordinate(self, angle, is_static=False, is_global=False)
        return coordinate