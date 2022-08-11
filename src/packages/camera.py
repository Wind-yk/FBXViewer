import numpy
from numpy import matrix
from enum import Enum

class Axis(Enum):
        X = 0
        Y = 1
        Z = 2

class Camera:
    def __init__(self):

        self.transform =  matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.focal = matrix([
            [1, 0, 0, 0],  # f 0 0 0
            [0, 1, 0, 0],  # 0 f 0 0
            [0, 0, 1, 0],  # 0 0 1 0
        ])

        self.angle  = [0,0,0]
        self.scale  = [0,0,0]
        self.center = [0,0,0]

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