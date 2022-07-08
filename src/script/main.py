import sys

sys.path.append("src")

import packages.fbx

packages.fbx.fbx2json("sphere.fbx")

print("Bye :)")
