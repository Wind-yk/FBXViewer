from time import time
# from random import random
# from telnetlib import X3PAD
# from tracemalloc import start
# from matplotlib.axis import Axis
from packages.camera import Camera
from numpy import pi, asarray, array
from matplotlib import pyplot as plt
# from matplotlib.widgets import TextBox
from matplotlib.widgets import Button, Slider

import matplotlib.pyplot as plt

class Display:
    """Displays several geometric bodies"""

    # ------------------------- internal methods ------------------------- #
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


    def _slider_movement_x_callback(self, event):
        """Test slider callback func"""
        movement_val = self.mov_x_slider.val - self.camera.shift.x
        self.camera.applyTransform(shift=[movement_val,0,0])
        for mesh in self.meshes:    
            mesh.applyTransform(self.camera)
        self._plotMeshes()

    def _slider_rotation_y_callback(self, event):
        """Test slider callback func"""
        rotation_angle = pi/180 * self.rot_y_slider.val - self.camera.angle.y
        self.camera.applyTransform(angle=[0,rotation_angle,0])
        for mesh in self.meshes:  
            mesh.applyTransform(self.camera)
        self._plotMeshes()

    def _slider_rotation_x_callback(self, event):
        """Test slider callback func"""
        rotation_angle = pi/180 * self.rot_x_slider.val - self.camera.angle.x

        temp_shift = self.camera.shift

        self.camera.applyTransform(shift = (-temp_shift.x,-temp_shift.y,-temp_shift.z), angle=[rotation_angle,0,0])

        self.camera.applyTransform(shift = temp_shift)

        for mesh in self.meshes: 
            mesh.applyTransform(self.camera)
        self._plotMeshes()

    def _plotMeshes(self):
        """Update mehes with current camera transform, then show in the canvas."""
        # Clear canvas
        self.defaultPlt.clear()
        
        # Fix screen limit
        self.defaultPlt.set_xlim(-10,10)
        self.defaultPlt.set_ylim(-10,10)

        # Draw points and vertices
        start = time()
        for mesh in self.meshes:
            edges = array(mesh.edges).T
            x = asarray(mesh._2DVertices[0,:]).reshape(-1)
            y = asarray(mesh._2DVertices[1,:]).reshape(-1)
            self.defaultPlt.plot(x[edges], y[edges], mesh.color+'-')
            # # Draw point numbers
            # sep = .1 # separation
            # self.defaultPlt.text(pointsX[0]+(2*random()-1)*sep, pointsY[0]+(2*random()-1)*sep, edge[0], fontsize=12, color='r')
        print(f"Drawing time: {(time()-start)*1e3:.2f} ms.")


    # ------------------------- methods ------------------------- #
    def start(self):
        # Configurate window size
        # plt.figure(figsize=(self.winSize[0], self.winSize[1]))
                
        # Apply meshes transform with camera
        for mesh in self.meshes:
            mesh.applyTransform(self.camera, angle=[0,45,0])

        self._plotMeshes()
     
        # Create test slider mov X
        axSliderMovX = plt.axes([0.35, 0.92, 0.5, 0.03])  
        self.mov_x_slider = Slider(
            ax=axSliderMovX,
            label="Camera mov x",
            valmin=-10.0,
            valmax=10.0,
            valinit=0.0,
        )
        self.mov_x_slider.on_changed(self._slider_movement_x_callback)

        # Create test slider rot X
        axSliderRotX = plt.axes([0.1, 0.3, 0.03, 0.5])  
        self.rot_x_slider = Slider(
            ax=axSliderRotX,
            label="Camera rot x",
            valmin=0.0,
            valmax=360.0,
            valinit=0.0,
            orientation="vertical"
        )
        self.rot_x_slider.on_changed(self._slider_rotation_x_callback)

        # Create test slider rot Y
        axSliderRotY = plt.axes([0.35, 0.1, 0.5, 0.03])  
        self.rot_y_slider = Slider(
            ax=axSliderRotY,
            label="Camera rot y",
            valmin=0.0,
            valmax=360.0,
            valinit=0.0,
        )
        self.rot_y_slider.on_changed(self._slider_rotation_y_callback)

        # Start render
        plt.show(block=True)


    def add_mesh(self, mesh):
        self.meshes.append(mesh)
