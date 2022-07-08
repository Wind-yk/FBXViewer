class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    # x getter and setter
    @property
    def x(self):
        return self.x

    @x.setter
    def x(self, value):
        try:
            # check correct input
            self.x = float(value)
        except:
            raise ValueError
   
    # y getter and setter
    @property
    def y(self):
        return self.y

    @y.setter
    def y(self, value):
        try:
            self.y = float(value)
        except:
            raise ValueError

    # z getter and setter
    @property
    def z(self):
        return self.z

    @z.setter
    def z(self, value):
        try:
            self.z = float(value)
        except:
            raise ValueError

    # coordinates' getter and setter
    def coordinates(self):
        # return a list instead of a tuple
        return [self.x, self.y, self.z]

    @coordinates.setter
    def coordinates(self, valuex, valuey, valuez):
        try:
            self.x = float(valuex)
            self.y = float(valuey)
            self.z = float(valuez)
        except:
            raise ValueError