import yaml
from yaml.loader import SafeLoader
import numpy as np
import matplotlib.pyplot as plt

# Project packages
from packages.fbx import readFBX
from packages.display import Display

CONFIG_PATH = "config/config.yaml"

if __name__ == '__main__':
    with open(CONFIG_PATH) as f:
        config = yaml.load(f, Loader=SafeLoader)
    list_mesh = readFBX(config["file_path"])

    display = Display()
    for mesh in list_mesh:
        mesh.send2render(display)

    display.show()