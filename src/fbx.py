import sys
import string
import os


def fbx2json(input, output="output.json", force=False):

    # Change working directory
    os.chdir("src/fbxInfo/")

    # If exit output.txt, we delete it
    if os.path.exists(output):
        if force:
            os.remove(output)
        else:
            raise FileNotExist(f"{output} already exists!")
    

    # Complete the command with input file name
    input = "readFbxInfo.exe " + input + " >> " + output

    # Execute the readFbxInfo.exe
    os.system(input)
