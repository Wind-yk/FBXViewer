import numpy
from numpy import matrix, sqrt, sin , cos, identity
from enum import Enum
from typing import Union

from packages.point import Point

class Axis(Enum):
        X = 0
        Y = 1
        Z = 2

class Camera:
    def __init__(self):

        # http://citmalumnes.upc.es/~julianp/lina/section-20.html
        
        '''
        self.transform =  matrix([
            [-2/sqrt(8), -2/sqrt(24),  1/sqrt(3), 3],
            [         0, -4/sqrt(24), -1/sqrt(3), 4],\
            [ 2/sqrt(8), -2/sqrt(24),  1/sqrt(3), 5],
            [         0,           0,          0, 1]])
        '''
        self.transform = identity(4)

        self.shift =  [0,0,-4]

        self.focal = 6

        self.angle  = [0,0,0]
        self.scale  = [0,0,0]
        self.center = [0,0,0]

        # Init transform
        self.applyTransform()

    @property
    def focal(self) -> matrix:
        return self._focal

    @focal.setter
    def focal(self, f: float):
        self._focal = matrix([
            [f, 0, 0, 0], 
            [0, f, 0, 0],  
            [0, 0, 1, 0], 
        ])

    @property
    def transform(self) -> matrix:
        return self._transform

    @transform.setter
    def transform(self, t: matrix):
        self._transform = t

    @property
    def angle(self) -> Point:
        return self._angle

    @angle.setter
    def angle(self, angle: Union[Point, float, int, list, tuple]):
        if isinstance(angle, Point):
            self._angle = angle
        elif isinstance(angle, (int, float)):
            self._angle = Point(angle, angle, angle)
        elif isinstance(angle, (list, tuple)):
            self._angle = Point(*angle)
        else:
            raise TypeError("angle must be set using one of: float, int, list, tuple, Point.")

    @property
    def shift(self) -> Point:
        return self._shift

    @shift.setter
    def shift(self, shift: Union[Point, float, int, list, tuple]):
        if isinstance(shift, Point):
            self._shift = shift
        elif isinstance(shift, (int, float)):
            self._shift = Point(shift, shift, shift)
        elif isinstance(shift, (list, tuple)):
            self._shift = Point(*shift)
        else:
            raise TypeError("center must be set using one of: float, int, list, tuple, Point.")

    def _rotation_matrix(self) -> matrix:
        """
        Get the matrix for the rotation.

        # Parameters
            - `rotation` (list|tuple): list-like of (yaw, pitch, roll).

        # Returns
            - `rotation_matrix` (matrix): 4×4 matrix

        https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
        """

        alfa, beta, gamma = self._angle
        c_a, c_b, c_c = cos(alfa), cos(beta), cos(gamma)
        s_a, s_b, s_c = sin(alfa), sin(beta), sin(gamma)

        rotation_matrix = matrix([
            [c_b*c_c, s_a*s_b*c_c - c_a*s_c, c_a*s_b*c_c + s_a*s_c, 0],
            [c_b*s_c, s_a*s_b*s_c + c_a*c_c, c_a*s_b*s_a - s_a*c_c, 0],
            [   -s_b,               s_a*c_b,               c_a*c_b, 0],
            [      0,                     0,                     0, 1]
        ])

        return rotation_matrix

    def _shift_matrix(self) -> matrix:
        """
        Get the matrix that shifts all components by the vector `shift`.

        # Parameters
            - `shift` (Point): represents the vector of shift.

        # Output:
            - `shift_matrix` (matrix): 4×4 matrix
        """
        x, y, z = self._shift
        shift_matrix = matrix([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])
        return shift_matrix

    def applyTransform(self,
        angle: Union[Point, float, int, list, tuple] = 0,
        shift: Union[Point, float, int, list, tuple] = 0):
        
        self.angle += angle
        self.shift += shift

        shift_matrix    = self._shift_matrix()
        rotation_matrix = self._rotation_matrix()

        self.transform = rotation_matrix @ shift_matrix

        # Generate rotateMatrix -> reference: https://es.wikipedia.org/wiki/F%C3%B3rmula_de_rotaci%C3%B3n_de_Rodrigues

        # return transform * rotateMatrix