from numpy import matrix, identity, sin, cos, pi

# Project packages
from src.packages.point import Point
from src.packages.display import Display

class Mesh:
    """
    This class will handle a geometric body and
    send it to the Display class for render.
    """

    def __init__(self, vertices, edges, center, angle, scale) -> None:
        self.vertices = vertices # matrix of shape 4×|V|
        self.edges = edges
        self.show = True
        
        self.transform_matrix = identity(4)  # identity matrix of size 4×4
        self.applyTranform(center, angle, scale)


    def disable(self):
        """Hide the geometric body."""
        self.show = False

    
    def enable(self):
        """Display the geometric body."""
        self.show = True


    def applyTransform(self, center: Point=Point(0,0,0), angle: list|tuple=(0,0,0), scale: float=1.) -> matrix:
        """
        Update the tranform matrix. First shift, then rotate and at the end scale.
        
        # Params:
            - `center` (Point): for translation
            - `angle` (list | tuple): 3-length in radians (yaw, pitch, roll)
            - `scale` (float): for scale

        https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
        """
        shift_matrix = self._shift(center)
        rotation_matrix = self._rotation(angle)
        scale_matrix = self._scale(scale)
        
        return scale_matrix @ rotation_matrix @ shift_matrix @ self.transform_matrix


    def _scale(self, s: float):
        assert s != 0
        scale_matrix = matrix([
            [s, 0, 0, 0],
            [0, s, 0, 0]
            [0, 0, s, 0]
            [0, 0, 0, 1]
        ])
        return scale_matrix


    def _shift(self, shift: Point):
        x, y, z = shift
        shift_matrix = matrix([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])
        return shift_matrix


    def _rotation(self, rotation: list|tuple):
        """
        https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
        """
        alfa, beta, gamma = rotation

        assert 0 <= alfa < 2*pi and 0 <= beta < 2*pi and 0 <= gamma < 2*pi

        c_a, c_b, c_c = cos(alfa), cos(beta), cos(gamma)
        s_a, s_b, s_c = sin(alfa), sin(beta), sin(gamma)

        rotation_matrix = matrix([
            [c_b*c_c, s_a*s_b*c_c - c_a*s_c, c_a*s_b*c_c + s_a*s_c, 0],
            [c_b*s_c, s_a*s_b*s_c + c_a*c_c, c_a*s_b*s_a - s_a*c_c, 0],
            [   -s_b,               s_a*c_b,               c_a*c_b, 0],
            [      0,                     0,                     0, 1]
        ])
        return rotation_matrix


    def send2render(self, display: Display):
        """
        Send the actual geometric body to render.
        """
        display.add_mesh(self)


    def to2D(self):
        """
        Return the vertices mapped to 2D.
        """
        mapped_points = self.transform_matrix @ self.vertices
        return mapped_points[0,:], mapped_points[1,:]
    

    def to_fbx(self, path: str, force: bool=False):
        """
        Save as fbx file.
        """
        pass

