import sys
import string
import os

# Project defined classes
from packages.mesh import Mesh
 
def fbx2json(input:str, output:str, force:bool=False):
    """
    Converts a FBX file to json, using external C++ package.
    """

    output_path = "../../data/med/"
    input_path = "../../data/int/"

    # Change working directory
    os.chdir("src/script")

    # If exit output.txt, we delete it
    if os.path.exists(output_path + output):
        if force:
            os.remove(output_path + output)
        else:
            raise FileExistsError(f"{output} already exists.")

    # Complete the command with input file name
    input = "readFbxInfo.exe " + input_path + input + " >> " + output_path + output

    # Execute the readFbxInfo.exe
    os.system(input)

def readFBX(fbx_path: str, json_path: str=None, overwrite: bool=False) -> list(Mesh):
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
    pass
