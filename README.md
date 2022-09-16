# 3D

## Desription

This is the description of this project ;).

## Build

1. Clone the repository to your local disc with following command:

```bash
git clone https://github.com/Wind-yk/3D.git
```

2. Install conda or miniconda.
3. From terminal and under the `3D` project folder, use:

```bash
conda env create -f environment.yaml
```

4. After the installation, activate the Python environment with:

```bash
conda activate 3D
```

5. Check that you are running with the right interpreter from your IDE.

## Quickstart

Include here some code, screenshots or gifs.

### Configuration

Configure yaml file inside the config folder. It is primarily as follows:

```bash
configuration:

  name: "3D project"

  version: 0.1.0

  readFBX:
    fbx_path: ../../data/int/output.fbx
    overwrite: false
  
  Camera:
    shift: [0,0,-4]
    focal: 12
    angle: [100,200,300]
    scale: 1

  Display:
    winSize: [5, 5]
```

You can edit the path to the fbx file by changing the "fbx_path" that is under the section of "readFBX"; just keep in mind that the
operating directory is 3D/src/main.py. The predetermined fbx_path is set to be a sphere's graph that is included within the package.

The "overwrite" parameter is set to be "false" since it won't modify the already existing json output file.

For more needs you can even modify the camera or the output windows size.

Remember that you shall **only** modify this "config.yaml" file. 

### Rendering

The units of the output windows is the same as the default unit in the fbx file. The red line marked inside each bar is the
initial value of that parameter when first running the program. You can retouch these values to rotate, move, zoom in or zoom out the graph.

![](https://github.com/Wind-yk/3D/blob/main/docs/sphere.gif)

## References and documentation

* [Development](docs/development.md)

* [FBX Format reference](https://banexdevblog.wordpress.com/2014/06/23/a-quick-tutorial-about-the-fbx-ascii-format/)

* [FBX Format reference](https://web.archive.org/web/20160605023014/https://wiki.blender.org/index.php/User:Mont29/Foundation/FBX_File_Structure)

* [Mathematical base](http://citmalumnes.upc.es/~julianp/lina/section-13.html)
