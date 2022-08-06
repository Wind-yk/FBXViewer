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


    with open(CONFIG_PATH) as f:
        config = yaml.load(f, Loader=SafeLoader)["configuration"]
    list_mesh = readFBX(**config['readFBX'])

    print(list_mesh[0].vertices, list_mesh[0].edges, sep='-'*30 + '\n')
    display = Display()

    vertices = [
        [ 1.,  1.,  1.,  1., -1., -1., -1., -1.],
        [ 1.,  1., -1., -1.,  1.,  1., -1., -1.],
        [ 1., -1.,  1., -1.,  1., -1.,  1., -1.],
        [ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.]
    ]

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
