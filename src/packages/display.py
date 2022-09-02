from telnetlib import X3PAD
from tracemalloc import start
from matplotlib.axis import Axis
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from numpy import matrix, size, zeros
from matplotlib.widgets import TextBox
from packages.camera import Camera
from random import random

class Display:
    """Displays several geometric bodies"""
    pass

    def __init__(self):
        self.meshes = []

        self.camera = Camera()

        self.winSize = [5, 5]

        self.MoveXBtn:Button()

        self.started = False

        self.fig, self.defaultPlt = plt.subplots()

    def start(self):
        '''Configurate window size'''
        # plt.figure(figsize=(self.winSize[0], self.winSize[1]))

        # apply transform with camera
        for mesh in self.meshes:
            mesh.applyTransform(self.camera)

        self.updateMeshes()

        axnext = plt.axes([0.85, 0.90, 0.1, 0.075])

        self.MoveXBtn = Button(axnext, "MoveX")

        self.MoveXBtn.on_clicked(self.MoveX)

        plt.show(block=True) 

    def MoveX(self, event):
        for mesh in self.meshes:
            self.camera.transform[0,3] += 1
            mesh.applyTransform(self.camera)
        self.updateMeshes()

    def updateMeshes(self):

        # clear canvas
        self.defaultPlt.clear()
        
        # fix screen limit
        self.defaultPlt.set_xlim(-10,10)
        self.defaultPlt.set_ylim(-10,10)

        pointsX = zeros(2)
        pointsY = zeros(2)
        printed_edges = []
        
        for mesh in self.meshes:
            for edge in mesh.edges:
                # get vertex
                pointsX[0] = int(mesh.get2DVertex(edge[0])[0])
                pointsX[1] = int(mesh.get2DVertex(edge[1])[0])
                pointsY[0] = int(mesh.get2DVertex(edge[0])[1])
                pointsY[1] = int(mesh.get2DVertex(edge[1])[1])

                self.defaultPlt.plot(pointsX,pointsY, mesh.color+'-o')
                
                # draw text
                sep = .1 # separation
                if edge[0] not in printed_edges:
                    self.defaultPlt.text(pointsX[0]+(2*random()-1)*sep, pointsY[0]+(2*random()-1)*sep, edge[0], fontsize=12, color='r')
                    printed_edges.append(edge[0])
                if edge[1] not in printed_edges:
                    self.defaultPlt.text(pointsX[1]+(2*random()-1)*sep, pointsY[1]+(2*random()-1)*sep, edge[1], fontsize=12, color='r')
                    printed_edges.append(edge[1])

    def add_mesh(self,mesh):
        self.meshes.append(mesh)
