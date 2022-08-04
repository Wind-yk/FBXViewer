import matplotlib.pyplot as plt
from numpy import matrix

class Display:
    """Displays several geometric bodies"""
    pass

    def __init__(self):
        self.meshes = []

        self.camera = matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.focal = matrix([
            [1, 0, 0, 0], # f 0 0 0
            [0, 1, 0, 0], # 0 f 0 0
            [0, 0, 1, 0], # 0 0 1 0
        ])
        pass

    def show(self):
        """
        Show all the enable meshes and handle the interaction.
        """
        pointsX = []
        pointsY = []

        for mesh in self.meshes:
            for edge in mesh.edges:
                pointsX.append(mesh.vertices[edge[0]][0])
                pointsX.append(mesh.vertices[edge[1]][0])

                pointsY.append(mesh.vertices[edge[0]][1])
                pointsY.append(mesh.vertices[edge[1]][1])

                plt.plot(pointsX,pointsY)
            pass

        plt.show(block=True)

        pass

    def add_mesh(self,mesh):

        self.meshes.append(mesh)

        pass