# 3D

## How to use git

1. In case you have not configured git, follow the instructions at terminal:

    ```
    $ git config --global user.name "your github username"
    $ git config --global user.email "your github email"
    $ git config --global color.ui true
    $ git config --global core.editor code
    ```

2. Clone this repo from terminal. This will create the `3D` project folder under your current directory:

    ```
    $ git clone https://github.com/Wind-yk/3D
    ```

3. The main instructions and workflow of `git`:


## Build the Python environment

A Python environment is a environment such that the Python interpreter, libraries and scripts installed into it are isolated from those installed in other virtual environments. 

Its aim is to ensure that all developers are using the same version of Python and Python libraries, to avoid discrepancies due to different versions.

1. Install conda or miniconda.
2. From terminal and under the `3D` project folder, use:

```
conda env create -f environment.yaml
```

3. After the installation, activate the Python environment with:

```
conda activate 3D
```

4. Check that you are running with the right interpreter from your IDE.

5. If you installed some new packages, remember to refresh the `environment.yaml` using:

```
conda env export > environment.yml
```
