import yaml
from yaml.loader import SafeLoader

# Project packages
from packages.fbx import readFBX
from packages.display import Display
from packages.mesh import Mesh

CONFIG_PATH = "config/config.yaml"

if __name__ == '__main__':

    from packages.fbx import preprocessFBXjson
    import json

    with open('data/med/cube2.json') as f:
        data = json.load(f)
        data = preprocessFBXjson(data)
    
    with open('data/int/temp.json', 'w') as f:
        json.dump(data, f, indent=2)

    with open(CONFIG_PATH) as f:
        config = yaml.load(f, Loader=SafeLoader)["configuration"]
    list_mesh = readFBX(**config['readFBX'])
    display = Display()
    for mesh in list_mesh:
        mesh.send2render(display)
    display.start()

    # print(list_mesh[0].vertices, list_mesh[0].edges, sep='-'*30 + '\n')
    
    # def foo(l):
    #     i = 0
    #     out = []
    #     first_index = 0
    #     while i < len(l)-1:
    #         x = l[i]   if l[i]   >= 0 else -l[i]   - 1
    #         y = l[i+1] if l[i+1] >= 0 else -l[i+1] - 1
    #         out.append((x,y))
    #         if l[i+1] < 0:
    #             out.append((y,l[first_index]))
    #             i += 2
    #             first_index = i
    #         else:
    #             i += 1
    #     print(out)
    #     return out

    # Mesh(
    #     vertices=[
    #         [ 1.,  1., -1., -1.,  1.,  1., -1., -1.],
    #         [ 1.,  1.,  1.,  1., -1., -1., -1., -1.],
    #         [ 1., -1.,  1., -1.,  1., -1.,  1., -1.],
    #         [ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.]
    #     ],
    #     edges=foo([0, 4, 6, -3, 3, 2, 6, -8, 7, 6, 4, -6, 5, 1, 3, -8, 1, 0, 2, -4, 5, 4, 0, -2]),
    #     shift=0,
    #     angle=0,
    #     scale=1,
    #     color='b'
    # ).send2render(display)

    # Mesh(
    #     vertices=[[0,0,0],[1,0,0],[0,1,0],[0,0,1]],
    #     edges=[(0,i) for i in range(1,4)],
    #     angle=0,
    #     shift=0,
    #     scale=1,
    #     color='r'
    # ).send2render(display)

    # # for mesh in list_mesh:
    # #     mesh.send2render(display)

    # display.start()
