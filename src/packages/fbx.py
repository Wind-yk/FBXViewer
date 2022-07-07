import sys
import string
import os


def fbx2json(input, output="output.json", force=False):

    output_dir = "../../data/med/"

    # Change working directory
    os.chdir("../../data/int")

    # If exit output.txt, we delete it
    if os.path.exists(output_dir + output):
        if force:
            os.remove(output_dir + output)
        else:
            raise FileExistsError(f"{output} already exists.")

    # Complete the command with input file name
    input = "readFbxInfo.exe " + input + " >> " + output_dir + output

    # Execute the readFbxInfo.exe
    os.system(input)
