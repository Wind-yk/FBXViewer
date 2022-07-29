import json
from src.packages.display import Display

class Mesh:
    
    """
    This class will handle a geometric body and
    send it to the Display class for render.
    """

    def __init__(self, vertices, edges, center, angle, scale) -> None:
        self.vertices = vertices
        self.edges = edges
        self.transform_matrix = self.getTranform(center, angle, scale)


    def getTransform(self, center, angle, scale):
        """
        Get the transformation matrix.
        
        Params:
            - center: for translation
            - angle: in radians, for rotation
            - scale: for scale
        """
        pass


    def applyTransformation(self, transition, rotation, scaling):
        """
        Update the transformation matrix taking into account the order of:
        first transition, then rotation and last scale.
        """
        pass


    def send2render(self, display: Display):
        """
        Send the actual geometric body to render.
        """
        pass
