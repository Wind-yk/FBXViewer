import sys
import string
import os


def fbx2json(input, output="output.json", force=False):

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
