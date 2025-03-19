# Symprobe
## Installation
Requires Paraview 5.11.1
To install the symprobe package create a virtual environment and activate it:
```bash
$ python3 -m venv path/to/venv/symprobe-env
$ source path/to/venv/symprobe-env/bin/activate
```
Include the path to Paraview as a .pth file
Navigate to the package location and install it with pip
```bash
$ cd path/to/symprobe
$ pip install -e .
```
Due to conflicts between Paraview and pyvista using different versions of the vtk package, it must be uninstalled for the package to work properly.
```bash
$ pip uninstall vtk
```
