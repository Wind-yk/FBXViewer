import sys
import string
import os


def fbx2txt(input="cube.fbx"):

    # Change working directory
    os.chdir("src/fbxInfo/")

    # If exit output.txt, we delete it
    if(os.path.exists("output.txt")):
        os.remove("output.txt")

    # Complete the command with input file name
    input = "readFbxInfo.exe " + input + " >> output.txt"

    # Execute the readFbxInfo.exe
    os.system(input)

    print("Successfully converted fbx to txt!")
