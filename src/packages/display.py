from telnetlib import X3PAD
from tracemalloc import start
from matplotlib.axis import Axis
import matplotlib.pyplot as plt
from matplotlib.widgets import Button,Slider
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

        self.rot_x_slider:Slider()

        self.rot_y_slider:Slider()

        self.mov_x_slider:Slider()

        self.started = False

        self.fig, self.defaultPlt = plt.subplots()

        # Adjust the main plot to make room for the sliders
        plt.subplots_adjust(left=0.25, bottom=0.25)

    def start(self):
        # Configurate window size
        # plt.figure(figsize=(self.winSize[0], self.winSize[1]))
                
        # apply meshes transform with camera
        for mesh in self.meshes:
            mesh.applyTransform(self.camera,angle=[0,45,0])

        self.updateMeshes()
     
        # Create test slider mov X
        axSliderMovX = plt.axes([0.35, 0.92, 0.5, 0.03])  
        self.mov_x_slider = Slider(
        ax=axSliderMovX,
        label='Camera mov x',
        valmin=-10.0,
        valmax=10.0,
        valinit=0.0,
        )
        self.mov_x_slider.on_changed(self.slider_movement_x_callback)

        # Create test slider rot X
        axSliderRotX = plt.axes([0.1, 0.3, 0.03, 0.5])  
        self.rot_x_slider = Slider(
        ax=axSliderRotX,
        label='Camera rot x',
        valmin=0.0,
        valmax=360.0,
        valinit=0.0,
        orientation="vertical"
        )
        self.rot_x_slider.on_changed(self.slider_rotation_x_callback)

        # Create test slider rot Y
        axSliderRotY = plt.axes([0.35, 0.1, 0.5, 0.03])  
        self.rot_y_slider = Slider(
        ax=axSliderRotY,
        label='Camera rot y',
        valmin=0.0,
        valmax=360.0,
        valinit=0.0,
        )
        self.rot_y_slider.on_changed(self.slider_rotation_y_callback)

        # Start render
        plt.show(block=True) 

    def slider_movement_x_callback(self, event):
        '''
        Test slider callback func
        '''
        for mesh in self.meshes:
            movement_val = self.mov_x_slider.val - self.camera.shift.x
            self.camera.applyTransform(shift=[movement_val,0,0])
            mesh.applyTransform(self.camera)
        self.updateMeshes()

    def slider_rotation_y_callback(self, event):
        '''
        Test slider callback func
        '''
        for mesh in self.meshes:
            rotation_angle = 3.14159265/180 * self.rot_y_slider.val - self.camera.angle.y
            self.camera.applyTransform(angle = [0, rotation_angle ,0])
            mesh.applyTransform(self.camera)
        self.updateMeshes()

    def slider_rotation_x_callback(self, event):
        '''
        Test slider callback func
        '''
        for mesh in self.meshes:
            rotation_angle = 3.14159265/180 * self.rot_x_slider.val - self.camera.angle.x
            self.camera.applyTransform(angle = [rotation_angle, 0 ,0])
            mesh.applyTransform(self.camera)
        self.updateMeshes()

    def updateMeshes(self):
        '''
        Update mehes with current camera transform, then show in the canvas
        '''
        # clear canvas
        self.defaultPlt.clear()
        
        # fix screen limit
        self.defaultPlt.set_xlim(-10,10)
        self.defaultPlt.set_ylim(-10,10)

        pointsX = zeros(2)
        pointsY = zeros(2)
        printed_edges = [] # tp print text
        
        for mesh in self.meshes:
            for edge in mesh.edges:
                # get vertex
                pointsX[0] = mesh.get2DVertex(edge[0])[0]
                pointsX[1] = mesh.get2DVertex(edge[1])[0]
                pointsY[0] = mesh.get2DVertex(edge[0])[1]
                pointsY[1] = mesh.get2DVertex(edge[1])[1]

                self.defaultPlt.plot(pointsX,pointsY, mesh.color+'-')
                
                '''
                # draw text
                sep = .1 # separation
                if edge[0] not in printed_edges:
                    self.defaultPlt.text(pointsX[0]+(2*random()-1)*sep, pointsY[0]+(2*random()-1)*sep, edge[0], fontsize=12, color='r')
                    printed_edges.append(edge[0])
                if edge[1] not in printed_edges:
                    self.defaultPlt.text(pointsX[1]+(2*random()-1)*sep, pointsY[1]+(2*random()-1)*sep, edge[1], fontsize=12, color='r')
                    printed_edges.append(edge[1])
                '''

    def add_mesh(self,mesh):
        self.meshes.append(mesh)
