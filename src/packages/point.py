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
    >>> Point(y=1, z=2)
    Point(0, 1, 2)
    >>> Point(1,2,3) - Point(3,2,1)  # element-wise
    Point(-2, 0, 2)
    >>> Point(1,2,3) * Point(2,3,4)  # element-wise
    Point(2, 6, 12)
    >>> Point(1,2,3) - 3
    Point(-2, -1, 0)
    >>> Point(1,1,1) == Point(1,1,1) and Point(1,1,1) == 1
    True
    >>> Point(1,2,3) != 1
    True
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

    def __iter__(self):
        return iter((self.x, self.y, self.z))


    def __eq__(self, rhs):
        if isinstance(rhs, (list, tuple, Point)):
            if len(rhs) != 3:
                raise ValueError("The length must be 3 for the equality of points.")
            return all(xi == yi for xi, yi in zip(self, rhs))
        elif isinstance(rhs, (float, int)):
            return self.x == rhs and self.y == rhs and self.z == rhs
        else:
            raise TypeError("Can only compare Points with Points, lists or tuples of length 3.")
    
    
    def __ne__(self, rhs):
        return not self.__eq__(rhs)
    

    def __add__(self, rhs):
        if isinstance(rhs, (list, tuple)):
            if len(rhs) != 3:
                raise ValueError("The length must be 3 for the sum of points.")
            return Point(self.x+rhs[0], self.y+rhs[1], self.z+rhs[2])
        elif isinstance(rhs, (float, int)):
            return Point(self.x+rhs, self.y+rhs, self.z+rhs)
        elif isinstance(rhs, Point):
            return Point(self.x+rhs.x, self.y+rhs.y, self.z+rhs.z)
        else:
            raise TypeError("Can only sum up Points with Points, lists or tuples of length 3.")


    def __sub__(self, rhs):
        if isinstance(rhs, (list, tuple)):
            if len(rhs) != 3:
                raise ValueError("The length must be 3 for the subtraction of points.")
            return Point(self.x-rhs[0], self.y-rhs[1], self.z-rhs[2])
        elif isinstance(rhs, (float, int)):
            return Point(self.x-rhs, self.y-rhs, self.z-rhs)
        elif isinstance(rhs, Point):
            return Point(self.x-rhs.x, self.y-rhs.y, self.z-rhs.z)
        else:
            raise TypeError("Can only subtract Points with Points, lists or tuples of length 3.")


    def __mul__(self, rhs):
        if isinstance(rhs, (list, tuple)):
            if len(rhs) != 3:
                raise ValueError("The length must be 3 for the multiplication of points.")
            return Point(self.x*rhs[0], self.y*rhs[1], self.z*rhs[2])
        elif isinstance(rhs, (float, int)):
            return Point(self.x*rhs, self.y*rhs, self.z*rhs)
        elif isinstance(rhs, Point):
            return Point(self.x*rhs.x, self.y*rhs.y, self.z*rhs.z)
        else:
            raise TypeError("Can only multiply Points with Points, lists or tuples of length 3.")


    def __len__(self):
        return 3

