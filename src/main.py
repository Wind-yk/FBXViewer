import yaml
from yaml.loader import SafeLoader
import numpy as np
import matplotlib.pyplot as plt

# Project packages
from packages.fbx import readFBX
from packages.display import Display
from packages.mesh import Mesh

CONFIG_PATH = "config/config.yaml"

if __name__ == '__main__':
    
    '''
    with open(CONFIG_PATH) as f:
        config = yaml.load(f, Loader=SafeLoader)
    list_mesh = readFBX(config['configuration']['file_src']['input'], config['configuration']['file_src']['output'])
    '''
    
    display = Display()

    vertices = [[0,0,0],[1,0,0],[1,1,0],[0,1,0]]

    edges = [ [0,1],[1,2],[2,3],[3,0]]

    center = [0,0,0]

    angle = [0,0,0]

    scale = [0,0,0]

    m = Mesh(vertices,edges,center,angle,scale)

    m.send2render(display)

    '''
    for mesh in list_mesh:
        mesh.send2render(display)
    '''
    display.show()

pass