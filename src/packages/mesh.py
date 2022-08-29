from math import isclose
from multiprocessing.sharedctypes import Value
from numpy.linalg import inv
from numpy import matrix, identity, sin, cos, asmatrix, sqrt, append, ones
from typing import Union # this shouldn't be necessary for Python > 3.9

# Project packages
from packages.point import Point
from packages.display import Display


# TODO: add setter for each point of vertices
class Mesh:
    """
    This class will handle a geometric body and
    send it to the Display class for render.

    ⚠ Angles in radians
    """
    # ------------------------- internal methods ------------------------- #
    def __init__(
        self,
        vertices: Union[list, matrix],
        edges:   'list[int]',
        shift:    Union[Point, float, int, list, tuple],
        angle:    Union[Point, float, int, list, tuple],
        scale:    Union[Point, float, int, list, tuple],
        color:    str='b'
    ):
        self.vertices = vertices    # matrix of shape 4×|V|
        self.edges    = edges       # need discussion
        self.shift    = shift
        self.angle    = angle
        self.scale    = scale

        # print('-'*30, 'vertices')
        # print(self.vertices)

        self.transform_matrix = identity(4)  # identity matrix of size 4×4
        # self.camera = matrix([
        #     [ 1, 0, 0, 1],
        #     [ 0, 1, 0, 0],
        #     [ 0, 0, 1, 0],
        #     [ 0, 0, 0, 1]
        # ])

        # http://citmalumnes.upc.es/~julianp/lina/section-20.html
        
        self.camera = matrix([
            [-2/sqrt(8), -2/sqrt(24),  1/sqrt(3), 3],
            [         0, -4/sqrt(24), -1/sqrt(3), 4],\
            [ 2/sqrt(8), -2/sqrt(24),  1/sqrt(3), 5],
            [         0,           0,          0, 1]])
        # self.camera = matrix([
        # [1, 0, 0, 1],
        # [0, 1, 0, 4],
        # [0, 0, 1, 5],
        # [0, 0, 0, 1]])

        self.focal = matrix([
            [5, 0, 0, 0], # f 0 0 0
            [0, 5, 0, 0], # 0 f 0 0
            [0, 0, 1, 0], # 0 0 1 0
        ])

        self.applyTransform(shift, angle, scale)

        self.show = True
        self.color = color


    # TODO: change the assert to exception
    def _scale_matrix(self) -> matrix:
        """
        Get the matrix that multiplies all the components by a factor of `s`.

        # Parameters
            - `s` (float): factor of product

        # Output:
            - `scale_matrix` (matrix): 4×4 matrix
        """
        x, y, z = self._scale
        scale_matrix = matrix([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]
        ])
        return scale_matrix


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


    # TODO: add camera as parameter
    def _to2D(self) -> matrix:
        """
        Return the vertices mapped to 2D.
        """
        # print(self.vertices)

        mapped_points = self.focal @ inv(self.camera) @ self.transform_matrix @ self.vertices
        # print('-'*30, 'mapped points 1')
        # print(self.transform_matrix @ self.vertices)
        # print('-'*30, 'mapped points 2')
        # print(inv(self.camera) @ self.transform_matrix @ self.vertices)
        # print('-'*30, 'mapped points 3')
        # print(mapped_points)
        return mapped_points[:2, :] / mapped_points[2,:]  # homogeneous coordinates


    # ------------------------- properties ------------------------- #
    @property
    def vertices(self):
        return self._vertices

    # TODO: optimize the process
    @vertices.setter
    def vertices(self, values: Union[matrix, list]):
        """
        Sets the vertices.

        Automatically sets the tail coordinates (all 1's) as the last row in case that it appears as the last column:
        ```
        [[2,3,4,1],      -->     [[2,5],
         [5,6,7,1]]               [3,6],
                                  [4,7],
                                  [1,1]]

        [[0,1,0,1],             [[0,0,0,1],
         [0,0,0,1],      -->     [1,0,0,1],
         [0,0,0,1],              [0,0,0,1],
         [1,1,1,1]]              [1,1,1,1]]

        [[0,0,0,1],             [[0,0,0,1],
         [0,0,0,1],      -->     [0,0,0,1],
         [0,0,0,0],              [0,0,0,0],
         [1,1,1,1]]              [1,1,1,1]]
         ```
        """
        if not isinstance(values, matrix):
            values = asmatrix(values)
        # check if we should add a final row/column of 1s to ensure that it is homogeneous.
        if (values.shape[0] == 3 and (values.shape[1] != 4 or (values.shape[1] == 4 and not (values[:,3] == 1).all()))) or \
           (values.shape[1] == 3 and (values.shape[0] != 4 or (values.shape[0] == 4 and not (values[3,:] == 1).all()))):

            point_axis = int(values.shape[1] == 3)  # same as 0 if values.shape[0] == 3 else 1
            new_axs_shape = [values.shape[0], 1] if values.shape[1] == 3 else [1, values.shape[1]]
            # print('values:', values.shape, point_axis, dim_axis)
            # print('ones', asmatrix([ones(values.shape[dim_axis])]))
            # print('ones:',)
            values = append(values, ones(new_axs_shape), axis=point_axis)

        if not (values.shape[0] == 4 or values.shape[1] == 4):
            raise ValueError(f"At least one of the dimensions has to be 4 to set the vertices. {values.shape} is given.")

        if (values.shape[0] == 4 and values.shape[1] != 4 and not (values[3,:] == 1).all()) or \
           (values.shape[0] != 4 and values.shape[1] == 4 and not (values[:,3] == 1).all()) or \
           (values.shape == (4,4) and not ((values[:,3] == 1).all() or (values[3,:] == 1).all())) :
            raise ValueError("Every vertex must end with 1 (homogeneous coordinates).")

        if values.shape[0] != 4 or (values.shape[1] == 4 and (values[:,3] == 1).all()):
            values = values.T

        self._vertices = values
        # print(self._vertices[:5,:5])


    @property
    def edges(self) -> list:
        return self._edges

    @edges.setter
    def edges(self, values: list):
        self._edges = values


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
    def scale(self) -> Point:
        return self._scale

    @scale.setter
    def scale(self, scale: Union[Point, float, int, list, tuple]):

        if (isinstance(scale, (list, tuple, Point)) and any(v == 0 for v in scale) ) or \
           (isinstance(scale, (int, float))         and isclose(scale, 0)):
            raise ValueError(f"All values in scale must be non zero: ({scale})")

        if isinstance(scale, Point):
            self._scale = scale
        elif isinstance(scale, (int, float)):
            self._scale = Point(scale, scale,scale)
        elif isinstance(scale, (list, tuple)):
            self._scale = Point(*scale)
        else:
            raise TypeError("scale must be set using one of: float, int, list, tuple, Point.")


    @property
    def show(self) -> bool:
        return self._show

    @show.setter
    def show(self, value:bool):
        self._show = value


    @property
    def transform_matrix(self) -> matrix:
        return self._transform_matrix

    @transform_matrix.setter
    def transform_matrix(self, values: matrix):
        self._transform_matrix = values


    @property
    def color(self) -> str:
        return self._color

    # TODO: check if the color is valid
    @color.setter
    def color(self, value: str):
        self._color = value


    # ------------------------- methods ------------------------- #
    def send2render(self, display: Display) -> None:
        """
        Send the actual geometric body to render.
        """
        display.add_mesh(self)


    def toFBX(self, path: str, force: bool=False):
        """
        Save as fbx file.
        """
        pass


    def get2DVertex(self, i: int):
        """Given index `i`, return the `i`th mapped point."""
        if not isinstance(i, int):
            raise TypeError(f"Index must be int, {type(i)} is given.")
        return self._2DVertices[:,i]


    def getVertex(self, i: int):
        """Given index `i`, return the i'th vertex."""
        if not isinstance(i, int):
            raise TypeError(f"Index must be int, {type(i)} is given.")
        return self.vertices[:,i]


    def disable(self) -> None:
        """Hide the geometric body."""
        self.show = False


    def enable(self) -> None:
        """Display the geometric body."""
        self.show = True


    def applyTransform(
        self,
        shift: Union[Point, float, int, list, tuple] = 0,
        angle: Union[Point, float, int, list, tuple] = 0,
        scale: Union[Point, float, int, list, tuple] = 1.
    ) -> None:
        """
        Update the 2D Vertices. First shift, then rotate and at the end scale.

        # Parameters
            - `center` (Point): for translation
            - `angle` (list | tuple): 3-length in radians (yaw, pitch, roll)
            - `scale` (float): for scale

        https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
        """
        # Update internal parameters
        self.scale *= scale
        self.shift += shift
        self.angle += angle

        # Update transoform matrix
        shift_matrix    = self._shift_matrix()
        rotation_matrix = self._rotation_matrix()
        scale_matrix    = self._scale_matrix()
        self.transform_matrix = scale_matrix @ rotation_matrix @ shift_matrix @ self.transform_matrix
        
        self._2DVertices = self._to2D()
