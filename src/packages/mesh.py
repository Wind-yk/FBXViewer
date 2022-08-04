from math import isclose
from numpy import matrix, identity, sin, cos, pi, asmatrix

# Project packages
from packages.point import Point
from packages.display import Display


# TODO: add setter for each point of vertices
class Mesh:
    """
    This class will handle a geometric body and
    send it to the Display class for render.
    """
    # ------------------------- internal methods ------------------------- #
    def __init__(self, vertices: list[Point], edges: list, center: Point, angle: list[float], scale: list[float]):
        self.vertices = vertices # matrix of shape 4×|V|
        self.edges = edges       # 
        self.show = True
        
        self.transform_matrix = identity(4)  # identity matrix of size 4×4
        self.applyTransform(center, angle, scale)
        self._transform_matrix_backup = self.transform_matrix


    # TODO: change the assert to exception
    def _scale(self, scale: list[float]|float) -> matrix:
        """
        Get the matrix that multiplies all the components by a factor of `s`.

        # Parameters
            - `s` (float): factor of product

        # Output:
            - `scale_matrix` (matrix): 4×4 matrix
        """
        if isinstance(scale, (tuple, list)):
            assert all(scale)  # check all values are non-zero
            x, y, z = scale
        elif isinstance(scale, (float, int)):
            assert not isclose(scale, 0)
            x = y = z = scale
        
        scale_matrix = matrix([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]
        ])
        return scale_matrix


    def _shift(self, shift: Point) -> matrix:
        """
        Get the matrix that shifts all components by the vector `shift`.

        # Parameters
            - `shift` (Point): represents the vector of shift.
        
        # Output:
            - `shift_matrix` (matrix): 4×4 matrix
        """
        x, y, z = shift
        shift_matrix = matrix([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])
        return shift_matrix


    # TODO: change the assert to exception
    def _rotation(self, rotation: list or tuple) -> matrix:
        """
        Get the matrix for the rotation.

        # Parameters
            - `rotation` (list|tuple): list-like of (yaw, pitch, roll).

        # Returns
            - `rotation_matrix` (matrix): 4×4 matrix

        https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
        """
        assert all(0 <= angle < 2*pi for angle in rotation)
        
        alfa, beta, gamma = rotation
        c_a, c_b, c_c = cos(alfa), cos(beta), cos(gamma)
        s_a, s_b, s_c = sin(alfa), sin(beta), sin(gamma)

        rotation_matrix = matrix([
            [c_b*c_c, s_a*s_b*c_c - c_a*s_c, c_a*s_b*c_c + s_a*s_c, 0],
            [c_b*s_c, s_a*s_b*s_c + c_a*c_c, c_a*s_b*s_a - s_a*c_c, 0],
            [   -s_b,               s_a*c_b,               c_a*c_b, 0],
            [      0,                     0,                     0, 1]
        ])
        return rotation_matrix

    # ------------------------- properties ------------------------- # 
    @property
    def vertices(self):
        return self._vertices


    # TODO: change assert to exception
    # TODO: change the all equal to 1 -> allclose
    @vertices.setter
    def vertices(self, values):
        if not isinstance(values, matrix):
            values = asmatrix(values)

        if values.shape[0] != 4:         # check if the input is inverted
            assert values.shape[1] == 4  # ensure that it will have 4 rows
            values = values.T

        if not (values[3,:] == 1).all():
            assert values.shape[1] == 4  # ensure that it will have 4 rows
            values = values.T

        self._vertices = values


    @property
    def edges(self):
        return self._edges


    @edges.setter
    def edges(self, values): 
        self._edges = values


    @property
    def show(self):
        return self._show


    @show.setter
    def show(self, values): 
        self._show = values


    @property
    def transform_matrix(self):
        return self._transform_matrix


    @transform_matrix.setter
    def transform_matrix(self, values): 
        self._transform_matrix = values


    @property
    def transform_matrix_backup(self):
        return self._transform_matrix_backup


    @transform_matrix_backup.setter
    def transform_matrix_backup(self, values): 
        self._transform_matrix_backup = values


    # ------------------------- methods ------------------------- #
    def send2render(self, display: Display) -> None:
        """
        Send the actual geometric body to render.
        """
        display.add_mesh(self)


    # TODO: add camera as parameter
    def to2D(self) -> tuple[matrix]:
        """
        Return the vertices mapped to 2D.
        """
        mapped_points = self.transform_matrix @ self.vertices
        return mapped_points[:2,:]
    

    def toFBX(self, path: str, force: bool=False):
        """
        Save as fbx file.
        """
        pass

    
    # TODO: change assert to exception
    # TODO: dynamic mapped point instead of calculating on-line
    def get2DVertex(self, i):
        """Given index `i`, return the `i`th mapped point."""
        assert isinstance(i, int)
        return self.to2D()[:,i]


    # TODO: change assert to exception
    def getVertex(self, i):
        """Given index `i`, return the i'th vertex."""
        assert isinstance(i, int)
        return self.vertices[:,i]


    def reset(self) -> None:
        """Reset to the initial transformation."""
        self.transform_matrix = self.transform_matrix_backup


    def disable(self) -> None:
        """Hide the geometric body."""
        self.show = False

    
    def enable(self) -> None:
        """Display the geometric body."""
        self.show = True


    def applyTransform(self, center: Point=Point(0,0,0), angle: list or tuple=(0,0,0), scale: float=1.) -> None:
        """
        Update the tranform matrix. First shift, then rotate and at the end scale.
        
        # Parameters
            - `center` (Point): for translation
            - `angle` (list | tuple): 3-length in radians (yaw, pitch, roll)
            - `scale` (float): for scale

        https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
        """
        shift_matrix = self._shift(center)
        rotation_matrix = self._rotation(angle)
        scale_matrix = self._scale(scale)
        self.transform_matrix = scale_matrix @ rotation_matrix @ shift_matrix @ self.transform_matrix
