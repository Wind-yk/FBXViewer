class Point:
    """
    Represents a 3D point in space.
    
    # Example:
    >>> p1 = Point( -3.1 , 2.0 , 4.5 )
    >>> p1.x
    -3.1
    >>> p1.y = 3
    >>> p1
    Point(-3.1, 2.0, 4.5)
    >>> Point(1, 2)
    Point(1, 2, 0)
    """

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"
        
    # x getter and setter
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
   
    # y getter and setter
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    # z getter and setter
    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value


