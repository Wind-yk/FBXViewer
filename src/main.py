from unicodedata import name
from packages import point
import numpy as np
import matplotlib.pyplot as plt
import yaml

if __name__ == '__main__':
    # while 1:
    #     # first input system, then others. Render last. ç
    # #     pass
    # from matplotlib.widgets import TextBox
    # fig, ax = plt.subplots()
    # plt.subplots_adjust(bottom=0.2)
    # t = np.arange(-2.0, 2.0, 0.001)
    # ydata = t ** 2
    # initial_text = "t ** 2"
    # l, = plt.plot(t, ydata, lw=2)


    # def submit(text):
    #     ydata = eval(text)
    #     l.set_ydata(ydata)
    #     ax.set_ylim(np.min(ydata), np.max(ydata))
    #     plt.draw()

    # axbox = plt.axes([0.1, 0.05, 0.8, 0.075])
    # text_box = TextBox(axbox, 'Evaluate', initial=initial_text)
    # text_box.on_submit(submit)

    # axbox1 = plt.axes([0.5, 0.05, 0.8, 0.075])
    # text_box = TextBox(axbox1, 'This 2', initial=initial_text)
    # text_box.on_submit(submit)

    # Read config from yaml
    config = yaml.save_load(CONFIG_PATH)

    # Read FBX -> list(Mesh)
    list_mesh = readFBX(config["file_path"])
    """
    readFBX(fbx_path:str, overwrite: bool)
      Check if the FBX is already in json. If not, convert it to json.
      !!! In case that overwrite is set, then convert anyway.

      Then read from the json, and call json2mesh for each one of the
      existent geometric bodies.
    """

    display = Display()
    for mesh in list_mesh:
        mesh.send2render(display)

    display.show()