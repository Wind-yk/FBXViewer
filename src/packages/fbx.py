import sys
import string
import os
import json
import math

# Project defined classes
from packages.mesh import Mesh
 
def fbx2json(input:str, output:str, force:bool=False):
    """
    Converts a FBX file to json, using external C++ package.
    """

    # Change working directory
    os.chdir("src/script")

    # If exit output.txt, we delete it
    if os.path.exists(output):
        if force:
            os.remove(output)
        else:
            raise FileExistsError(f"{output} already exists.")

    # Complete the command with input file name
    input = "readFbxInfo.exe " + input + " >> " + output
    # Execute the readFbxInfo.exe
    os.system(input)

def readFBX(fbx_path: str, json_path: str=None, overwrite: bool=False):
    """
    Return a list of Mesh from the FBX file.

    # Parameters:
      * `fbx_path` (str): path of the file.
      * `json_path` (str): output json file path. If None, then the name of FBX is used.
      * `overwrite` (bool): converts it to json even if the `json_path` file already exists.

    # Output:
        A list of Mesh that each of them represents a geometric body to display.
        The list can be empty.

    ⚠ In case that overwrite is set, then converts anyway.
    """
    # Check if the file exists, if it is already in json. If it is not,
    # then first use fbx2json to convert it to json and read it as so.

    # Create empty mesh list
    mesh_list = []

    # Convert fbx file to json
    try:
        fbx2json(fbx_path, json_path, overwrite)
    except FileExistsError as e:
        print(e)

    # Open the created json file for data
    with open(json_path, 'r') as file:
        data = json.load(file)

    counter = 0
    # Assign predetermined values for center, angle, scale
    center = [0, 0, 0]
    angle = [0, 0, 0]
    scale = [1, 1, 1]

    for i,v in enumerate(data['children'][8]['children']):
        # Create the list of mesh according to the number of geometries there are
        if v['name'] == "Geometry":
            vertices = v['children'][2]['properties'][0]['value']
            vertices = [vertices[i:i+3] for i in range(0, len(vertices), 3)]
            vertices = [[*v, 1.0] for v in vertices]
            edges = v['children'][3]['properties'][0]['value']
            new_mesh = Mesh(vertices, edges, center, angle, scale)
            mesh_list.append(new_mesh)

        # Fill up the information in each mesh acording to its respective model
        elif v['name'] == "Model":
            for i2, v2 in enumerate(v['children'][1]['children']):
                # Necessary information is allocated at most at ['children'][2]
                if i2 <= 2:
                    # Reminder: there will not always be data about Translation or Rotation, but we assume that there will always be Scaling info
                    if v2['properties'][0]['value'] == "Lcl Translation":
                        center = []
                        for idx in range(4, 7):
                            center.append(v2['properties'][idx]['value'])
                    elif v2['properties'][0]['value'] == "Lcl Rotation":
                        angle = []
                        for idx in range(4, 7):
                            # Convert angles to radians
                            angle.append(math.radians(v2['properties'][idx]['value']))
                    elif v2['properties'][0]['value'] == "Lcl Scaling":
                        scale = []
                        for idx in range(4, 7):
                            # Convert percentage to scale
                            scale.append(v2['properties'][idx]['value']/100)
            
            mesh_list[counter] = Mesh(mesh_list[counter].vertices, mesh_list[counter].edges, center, angle, scale)
            center = [0, 0, 0]
            angle = [0, 0, 0]
            counter += 1

    return mesh_list

