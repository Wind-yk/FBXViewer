from telnetlib import X3PAD
from matplotlib.axis import Axis
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from numpy import matrix, size, zeros
from matplotlib.widgets import TextBox
from packages.camera import Camera

class Display:
    """Displays several geometric bodies"""
    pass

    def __init__(self):
        self.meshes = []

        self.camera = Camera

        self.winSize = [5, 5]

    def start(self):
        '''Configurate window size'''
        plt.figure(figsize=(self.winSize[0], self.winSize[1]))

        # axnext = plt.axes([0.81, 0.05, 0.1, 0.075])

        # btn = Button(axnext, "Next")

        # btn.on_clicked(self.hi)

    def hi(slef):
        print("hello")

    def show(self):
        """
        Show all the enable meshes and handle the interaction.
        """

        pointsX = zeros(2)
        pointsY = zeros(2)

        for mesh in self.meshes:
            for edge in mesh.edges:
                pointsX[0] = int(mesh.get2DVertex(edge[0])[0])
                pointsX[1] = int(mesh.get2DVertex(edge[1])[0])
                pointsY[0] = int(mesh.get2DVertex(edge[0])[1])
                pointsY[1] = int(mesh.get2DVertex(edge[1])[1])
                plt.plot(pointsX,pointsY, mesh.color)

        plt.show(block=True)

    def add_mesh(self,mesh):
        self.meshes.append(mesh)
