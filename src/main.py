import yaml
from yaml.loader import SafeLoader
import numpy as np
from numpy import cos, sin, pi
import matplotlib.pyplot as plt

# Project packages
from packages.fbx import readFBX
from packages.display import Display
from packages.mesh import Mesh

CONFIG_PATH = "config/config.yaml"

if __name__ == '__main__':


    # with open(CONFIG_PATH) as f:
    #     config = yaml.load(f, Loader=SafeLoader)["configuration"]
    # list_mesh = readFBX(**config['readFBX'])

    # print(list_mesh[0].vertices, list_mesh[0].edges, sep='-'*30 + '\n')
    display = Display()

    m = 21; n = 2;
    a = 5; b = 1;
    n_pts = 500;
    torus_knot = [
        ((a+b*cos(m*s))*cos(n*s), (a+b*cos(m*s))*sin(n*s), b*sin(m*s))
                    for s in np.arange(0,2*pi,2*pi/n_pts)
    ]
    vertices = [
        [ 1.,  1.,  1.,  1., -1., -1., -1., -1.],
        [ 1.,  1., -1., -1.,  1.,  1., -1., -1.],
        [ 1., -1.,  1., -1.,  1., -1.,  1., -1.],
        [ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.]
    ]

    # vertices = torus_knot
    def foo(l):
        out = []
        i = 0
        first_index = 0
        while i < len(l)-1:
            x = l[i] if l[i] >= 0 else -l[i] - 1
            y = l[i+1] if l[i+1] >= 0 else -l[i+1] - 1
            out.append((x,y))
            if l[i+1] < 0:
                out.append((y,l[first_index]))
                i += 2
                first_index = i
            else:
                i += 1
        return out

    edges = foo([0, 4, 6, -3, 3, 2, 6, -8, 7, 6, 4, -6, 5, 1, 3, -8, 1, 0, 2, -4, 5, 4, 0, -2])
    # edges = [(i,i) for i in range(500)] 
    center = [0,0,0]

    angle = [0,0,0]

    #scale = [0,0,0]
    scale = 1

    m = Mesh(vertices,edges,center,angle,scale)

    m.send2render(display)

    # for mesh in list_mesh:
    #     mesh.send2render(display)

    display.start()

    display.show()

pass
