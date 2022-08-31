import os
import json
from math import radians
from pathlib import Path

# Project defined classes
from packages.mesh import Mesh


class FBXReaderError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, *kwargs)

 
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


def getKeyIndices(input_dict: dict, list_name_key: str, dict_name_key: str):
    """
    Returns a dictionary of kind {dict[list_name_key][dict_name_key]: [indices]}
    and remove the dict_name_key in the original dict
    
    # Example
    ```
    input:
    {
        'list_name': [
            { 'dict_name': 'Geometry' },
            { 'dict_name': 'Geometry' },
            { 'dict_name': 'Model' }
        ]
    }
    output:
    {
        'Geometry': [0,1],
        'Model': [2]
    }
    ```
    """
    key_indices = {}
    for idx, child in enumerate(input_dict[list_name_key]):
        key = child.pop(dict_name_key)
        if key in key_indices:
            key_indices[key].append(idx)
        elif key == '' and child == {}:
            continue
        else:
            key_indices[key] = [idx]
    return key_indices


def preprocessFBXjson(data: dict, rec: int = 1):
    """
    The original json is quite difficult to read as dict.
    Using this function we recursively convert the list 
    of children names to key of a new list/dictionary.

    Warning: the process might not be reversible, as some 
    content may be erased. 
    
    # Example
    ```
    {
        "version": 0,
        "children": [
            { "name": "Geometry", "x": {...}, "y": {...} },
            { "name": "Geometry", "x": {...}, "z": {...} },
            { "name": "" },
            { 
              "name": "P",
              "properties": [
                    { "type": "S", "value": "string1" },
                    { "type": "S", "value": "string2" },
                    { "type": "D", "value": 0.000000 },
                    { "type": "D", "value": 0.000000 },
                    { "type": "D", "value": 0.000000 }
                ]
            }
        ]
    }
    ```
    is converted to:
    ```
    {
        "version": 0,
        "Geometry": [
            {"x": {...}, "y": {...}},
            {"x": {...}, "z": {...}},
        ],
        "P": {
            "S": ["string1", "string2"],
            "D": [0.000000, 0.000000, 0.000000]
        }
    }
    ```
    """
    list_keys = [('children', 'name'), ('properties', 'type')]
    for list_name_key, dict_name_key in list_keys:
        if list_name_key in data:
            for key, indices in getKeyIndices(data, list_name_key, dict_name_key).items():
                if len(indices) == 1:
                    data[key] = preprocessFBXjson(data[list_name_key][indices[0]], rec+1) \
                                if list_name_key == 'children' \
                                else data[list_name_key][indices[0]]['value']
                else:
                    data[key] = [preprocessFBXjson(data[list_name_key][idx], rec+1) for idx in indices] \
                                if list_name_key == 'children' \
                                else [data[list_name_key][idx]['value'] for idx in indices]
            data.pop(list_name_key)
    return data


def list2edges(l: list):
    """
    Converts the list of FBX edges to a list tuples of 2 vertices.
    
    This may reduce the performance when drawing.

    # Example
    `[0, 4, 6, -3]` is converted to `[(0, 4), (4, 6), (6, 2), (2, 0)]`.
    """
    i = 0
    out = []
    first_index = 0
    while i < len(l)-1:
        x = l[i]   if l[i]   >= 0 else -l[i]   - 1
        y = l[i+1] if l[i+1] >= 0 else -l[i+1] - 1
        out.append((x,y))
        if l[i+1] < 0:
            out.append((y,l[first_index]))
            i += 2
            first_index = i
        else:
            i += 1
    return out

def getProperties(objs: dict):
    """
    Given the preprocessed objects of the FBX,
    return the properties:
        verts, edges, shifts, angles, scales
    as lists.
    """
    # Get vertices and edges
    geoms = objs['Geometry'] if isinstance(objs['Geometry'], list) else [objs['Geometry']]
    verts = [geom['Vertices']['d'] for geom in geoms]
    verts = [[vert[i:i+3] for i in range(0,len(vert),3)] for vert in verts]
    edges = [list2edges(geom['PolygonVertexIndex']['i']) for geom in geoms]
    
    # Get translation, rotation and scaling. 
    # Default values are set as they might not exist in the data.
    shifts, angles, scales = [], [], []
    models = objs['Model'] if isinstance(objs['Model'], list) else [objs['Model']]
    for model in models:
        sh, an, sc = 0, 0, 1
        for prop in model['Properties70']['P']:
            if prop['S'][0] == 'Lcl Translation':
                sh = prop['D']
            elif prop['S'][0] == 'Lcl Rotation':
                an = [radians(angle) for angle in prop['D']]
            elif prop['S'][0] == 'Lcl Scaling':
                sc = [scale/100 for scale in prop['D']]
        shifts.append(sh)
        angles.append(an)
        scales.append(sc)
    
    # Check that the length of the variables matches
    if not len(verts) == len(edges) == len(shifts) == len(angles) == len(scales):
        raise FBXReaderError(
            f"""The length of the properties are not the same:
            verts:  {len(verts)},
            edges:  {len(edges)},
            shifts: {len(shifts)},
            angles: {len(angles)},
            scales: {len(scales)}"""
        )

    return verts, edges, shifts, angles, scales


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
    # Convert fbx file to json
    if json_path is None:
        json_path = Path(fbx_path)
        json_path = json_path.parent.parent / "med" / json_path.stem + ".json"

    try:
        fbx2json(fbx_path, json_path, overwrite)
    except FileExistsError as e:
        print(f'readFBX: {e}')

    # Open the created json file for data and read objects from it
    with open(json_path, 'r') as file:
        data = preprocessFBXjson(json.load(file))
    
    # Build the list of Mesh
    mesh_list = [
        Mesh(vertex, edge, shift, angle, scale) 
        for vertex, edge, shift, angle, scale
        in zip(*getProperties(data['Objects']))
    ]
    
    return mesh_list

