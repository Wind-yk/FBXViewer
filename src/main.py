import yaml
from yaml.loader import SafeLoader

# Project packages
from packages.fbx import readFBX
from packages.display import Display
from packages.camera import Camera

CONFIG_PATH = "config/config.yaml"

if __name__ == '__main__':
    with open(CONFIG_PATH) as f:
        config = yaml.load(f, Loader=SafeLoader)["configuration"]
    
    display = Display(
        meshes=readFBX(**config['readFBX']),
        camera=Camera(**config['Camera']),
        **config['Display']
    )
    
    display.start()