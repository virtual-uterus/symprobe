#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sweeps.py

Contains function used for changing parameters when running multiple
simulations
Author: Mathias Roesler
Date: 11/24
"""

import os
import subprocess

from symprobe.constants import CONFIG_ENV_VAR, ESTRUS
from symprobe.constants import RESISTANCE, DIST_DICT


def modify_config(config_file, param, value):
    """Modifies the parameter in the configuration file

    Arguments:
    config_file -- str, path to the configuration file.
    param -- str, parameter to modify.
    value -- str, new value.

    Return:

    Raises:
    FileNotFoundError -- if the cell configuration file is not found.
    ValueError -- if the parameter is not found.

    """
    # Read and modify config file
    try:
        with open(config_file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError as e:
        raise e

    found = False  # To check param is found

    for i, line in enumerate(lines):
        if param in line:
            found = True
            if param == "conductivities_2d":
                lines[i] = f"{param} = [{value}, {value}] \n"
                break
            if param == "conductivities_3d":
                lines[i] = f"{param} = [{value}, {value}, {value}] \n"
                break
            if param == "magnitude":
                lines[i] = f"{param} = {value} \n"
                break
            if param == "mesh_name":
                lines[i] = f'mesh_name = "{value}"\n'
                break
            if param == "estrus":
                lines[i] = f'estrus = "{value}"\n'
                break
            else:
                lines[i] = f"   {param} = {value} \n"
                break
    if not found:
        # If the parameter was not found
        raise ValueError(
            f"the parameter '{param}' was not found in the configuration file."
        )

    with open(config_file, "w") as f:
        f.writelines(lines)


def get_config_dir():
    """Returns the directory with the configuration files are stored

    Arguments:

    Return:
    config_dir -- str, path to the configuration directory.

    Raises:
    OSError -- if the CONFIG_ENV_VAR is not set.

    """
    config_dir = os.getenv(CONFIG_ENV_VAR)
    if not config_dir:
        raise OSError(f"{CONFIG_ENV_VAR} environment variable is not set")

    return config_dir


def get_dim_config(dim):
    """Returns the dimension configuration file

    Arguments:
    dim -- int, dimension of the simulation {2, 3}.

    Return:
    dim_config_file -- path to the dimension configuration file.

    Raises:
    OSError -- if the CONFIG_ENV_VAR is not set.

    """
    try:
        config_dir = get_config_dir()

    except OSError as e:
        raise e
    return os.path.join(config_dir, "general", f"{dim}d_params.toml")


def get_cell_config(dim_config_file):
    """Gets the correct cell configuration file path

    Arguments:
    dim_config_file -- path to the dimension configuration file.

    Returns:

    Raises:
    OSError -- if the CONFIG_ENV_VAR is not set.
    FileNotFoundError -- if the cell configuration file is not found.
    ValueError -- if the parameter is not found in the configuration file.

    """
    try:
        config_dir = get_config_dir()

    except OSError as e:
        raise e

    type_found = False
    estrus_found = False

    try:
        with open(dim_config_file, "r") as f:
            for line in f:
                if "cell_type" in line:
                    cell_type = line.split('"')[1]
                    type_found = True

                if "estrus" in line:
                    # Get estrus if the cell type is Roesler
                    estrus = line.split('"')[1]
                    estrus_found = True
    except FileNotFoundError as e:
        raise e

    if not type_found:
        raise ValueError("cell_type not found in config file")

    if not estrus_found and cell_type == "Roesler":
        raise ValueError("estrus not found in config file")

    if cell_type == "Roesler":
        return os.path.join(config_dir, "estrus", f"{cell_type}_{estrus}.toml")

    else:
        return os.path.join(config_dir, "cell", f"{cell_type}.toml")


def resolution_sweep(dim, mesh_name, start_val, end_val):
    """Performs several simulations with different resolution meshes

    The meshes should be named like mesh_name_X.{ele, node, face}, where
    X is a number.

    Arguments:
    dim -- int, dimension of the simulation {2, 3}.
    mesh_name -- str, base name of the mesh.
    start_val -- float, start value for X.
    end_val -- float, end value for X.

    Return:

    Raises:
    OSError -- if the CONFIG_ENV_VAR is not set.
    ValueError -- if the start value is greater than the end value.
    FileNotFoundError -- if the cell configuration file is not found.
    ValueError -- if the parameter is not found in the configuration file.

    """
    # Get the config files
    try:
        dim_config_file = get_dim_config(dim)
        cell_config_file = get_cell_config(dim_config_file)

    except Exception as e:
        raise e

    # Check if start value is greater than end value
    if start_val > end_val:
        raise ValueError("the start value is greater than the end value")

    for j in range(start_val, end_val + 1):
        # Read and modify config file
        cur_mesh = f"{mesh_name}_{j}"
        conduct_val = 1 / (RESISTANCE * DIST_DICT[cur_mesh] ** 2)
        try:
            modify_config(dim_config_file, "mesh_name", cur_mesh)
            modify_config(
                cell_config_file,
                f"conductivities_{dim}d",
                conduct_val,
            )
        except ValueError as e:
            raise e
        except FileNotFoundError as e:
            raise e

        # Run the chaste simulation
        subprocess.run(["uterine-simulation", str(dim)])


def parameter_sweep(dim, param, start_val, end_val, step):
    """Performs several simulations with different values of a parameter

    Arguments:
    dim -- int, dimension of the simulation {2, 3}.
    param -- str, name of the parameter to change in the configuration file.
    start_val -- float, start value for the parameter.
    end_val -- float, end value for the parameter.
    step -- float, increase step between two simulations.

    Return:

    Raises:
    OSError -- if the CONFIG_ENV_VAR is not set.
    FileNotFoundError -- if the param configuration file is not found.
    ValueError -- if cell_type is not found in configuration file.
    ValueError -- if the start value is greater than the end value.
    FileNotFoundError -- if the cell configuration file is not found.
    ValueError -- if the parameter is not found in the configuration file.

    """
    # Initial setup
    value = float(start_val)
    end = float(end_val)
    step = float(step)

    # Get the config files
    try:
        dim_config_file = get_dim_config(dim)
        cell_config_file = get_cell_config(dim_config_file)

    except Exception as e:
        raise e

    # Check if start value is greater than end value
    if value > end:
        raise ValueError("the start value is greater than the end value")

    while True:
        # Read and modify config file
        try:
            modify_config(cell_config_file, param, value)
        except ValueError as e:
            raise e
        except FileNotFoundError as e:
            raise e

        # Run the chaste simulation
        subprocess.run(["uterine-simulation", str(dim)])

        # Update value for next iteration
        value += step

        # Check termination condition
        if value > end:
            break


def estrus_sweep(dim):
    """Performs simulations over all four stages of the estrus cycle

    Arguments:
    dim -- int, dimension of the simulation {2, 3}.

    Return:

    Raises:
    OSError -- if the CONFIG_ENV_VAR is not set.
    ValueError -- if the start value is greater than the end value.
    FileNotFoundError -- if the cell configuration file is not found.
    ValueError -- if the parameter is not found in the configuration file.

    """
    # Get the config files
    try:
        dim_config_file = get_dim_config(dim)

    except Exception as e:
        raise e

    dim_config_file = get_dim_config(dim)

    for j in range(4):
        # Read and modify config file
        try:
            modify_config(dim_config_file, "estrus", ESTRUS[j])
        except ValueError as e:
            raise e
        except FileNotFoundError as e:
            raise e

        # Run the chaste simulation
        subprocess.run(["uterine-simulation", str(dim)])
