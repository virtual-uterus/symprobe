# Symprobe
# Table of contents
1. [General description](#general)
2. [Requirements](#requirements)
3. [Usage](#usage)
	1. [Setup](#setup)
	2. [Running the code](#code)
		1. [***simulation-sweep.py*** script](#sweep)
		2. [***extract-data.py*** script](#data)
		3. [***extract-plot.py*** script](#plot)


<a id="general"></a>
## General description
This package provides tools to run simulations in Chaste and extract and plot the outputs.

The project is structure as follows:
```
symprobe/ (top-level directory)
|-- scripts/ (contains the Python scripts)
|-- symprobe/ (contains the symprobe module)
|-- tests/ (contains tests)
```

<a id="requirements"></a>
## Requirements
The code was run on Linux Ubuntu 22.04.2 LTS\
The code was developed in [Python](https://www.python.org/) version 3.10.12\
The required packages for Python are found in requirements.txt
For the extraction of the data, [Paraview 5.13](https://www.paraview.org/) or any other version using Python 3.10 is required to be installed.
For using the simulation-sweep script, Chaste and the [uterine-modelling](https://github.com/virtual-uterus/uterine-modelling) need to be installed.


<a id="usage"></a>
## Usage
<a id="setup"></a>
### Setup
First clone the project into *symprobe* and enter the new directory:
```bash
$ git clone git@github.com/virtual-uterus/symprobe.git
```

It is recommended to create a virtual environment in which to run the code. Create a virtual environment and activate it:
```bash
$ python3 -m venv ~/venv/symprobe-env
$ source ~/venv/symprobe-env/bin/activate
```

To be able to include the Paraview Python packages, a path file needs to be added in the site-packages folder in the virtual environment. First navigate to the Paraview Python site-package, where /path/to/ParaView/ is the path to the installation location:
```bash
$ cd /path/to/ParaView/paraview-5.13.1/lib/python3.10/site-packages
```
Then, copy the path to a .pth file in the Python site-packages in the virtual environment:
```bash
$ pwd >> ~/venv/symprobe-env/lib/python3.10/site-packages/paraview.pth
```

Return to the symprobe folder and install the module with the following commands:
```bash
$ cd /path/to/symprobe
$ pip3 install -e .
```

Due to conflicts between Paraview and pyvista using different versions of the vtk package, it must be uninstalled for the package to work properly.
```bash
$ pip uninstall vtk
```

**Update the BASE variable in the symprobe/constants.py file to the path you need, otherwise the paths will not be correct.**

Run the test to make sure that the code is working properly:
```bash
$ pytest
```

<a id="code"></a>
### Running the code

There are three scripts that can be run, contained in the *scripts/* directory: 
* ***simulation-sweep.py***
* ***extract-data.py***
* ***extract-plot.py***

<a id="sweep"></a>
#### ***simulation-sweep.py*** script
The ***simulation-sweep.py*** is a wrapper for Chaste that allows to easily run multiple simulations. Three types of sweeps are available:
* **parameter**, run multiple simulations with different values of a given parameter,
* **resolution**, run multiple simulations on different resolution meshes, and
* **estrus**, runs one simulation for each stage of the estrus cycle.

Run the following command from inside the *scripts/* directory to view the help message:
```bash
$ python3 simulation-sweep.py -h
```

**Note:** the estrus stages are always in the same order: proestrus, estrus, metestrus, diestrus.

<a id="data"></a>
#### ***extract-data.py*** script
The ***extract-data.py*** script extracts the data from a single simulation or multiple simulations.
To extract from a single simulation provide an integer value for the sim-numbers argument. Otherwise provide a range like 1-5 to extract the data from simulations 1, 2, 3, 4, and 5.

To extract the data, the PTS_DICT values need to be updated in the symprobe/constants.py file. The key needs to be the name of the mesh used and the values need to be three points in the mesh. The recommendation is to take one from the ovarian end, one from the centre, and one from the cervical end of the uterine horn.

Run the following command from inside the *scripts/* directory to view the help message:
```bash
$ python3 extract-data.py -h
```

<a id="plot"></a>
#### ***extract-plot.py*** script

The ***extract-plot.py*** script will plot the data extracted with ***extract-data.py***. Four plotting options are available:
* **cell**, plots the extracted data for each cell,
* **resolution**, plot the comparison metric from simulations with meshes at different resolutions,
* **parameter**, plot the comparison metric for simulations with different values of a given parameter, and
* **comparison**, compare the extracted data from two different simulations.

**Note:** the RES_DICT values need to be updated in the symprobe/constants.py file for the resolution plot to function. The key needs to be the name of the mesh used and the value needs to be the number of elements in the mesh.

Run the following command from inside the *scripts/* directory to view the help message:
```bash
$ python3 extract-plot.py -h
```
