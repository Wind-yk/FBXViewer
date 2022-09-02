import numpy
from numpy import matrix, sqrt
from enum import Enum

class Axis(Enum):
        X = 0
        Y = 1
        Z = 2

class Camera:
    def __init__(self):

        # http://citmalumnes.upc.es/~julianp/lina/section-20.html
        self.transform =  matrix([
            [-2/sqrt(8), -2/sqrt(24),  1/sqrt(3), 3],
            [         0, -4/sqrt(24), -1/sqrt(3), 4],\
            [ 2/sqrt(8), -2/sqrt(24),  1/sqrt(3), 5],
            [         0,           0,          0, 1]])

        self.focal = 5

        self.angle  = [0,0,0]
        self.scale  = [0,0,0]
        self.center = [0,0,0]

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

    def rotate(self, axis:Axis = Axis.X, angle:float = 0.0):
        
        rotateMatrix = []

        if axis == Axis.X:
            rotateMatrix = [
                [numpy.cos(angle), -numpy.sin(angle), 0, 0],
                [numpy.sin(angle), numpy.cos(angle), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
            pass

        elif axis == Axis.Y:
            rotateMatrix = [
                [numpy.cos(angle), 0, numpy.sin(angle), 0],
                [0, 1, 0, 0],
                [-numpy.sin(angle), 0, numpy.cos(angle), 0],
                [0, 0, 0, 1],
            ]    

        elif axis == Axis.Z:
            rotateMatrix = [
                [1, 0, 0, 0],
                [0, numpy.cos(angle), -numpy.sin(angle), 0],
                [0, numpy.sin(angle), numpy.cos(angle), 0],
                [0, 0, 0, 1],
            ]        
        pass

        # Generate rotateMatrix -> reference: https://es.wikipedia.org/wiki/F%C3%B3rmula_de_rotaci%C3%B3n_de_Rodrigues

        # return transform * rotateMatrix