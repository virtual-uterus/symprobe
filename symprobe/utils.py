#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py

Utility functions used for Python code
Author: Mathias Roesler
Date: 11/24
"""

import re

import numpy as np
import pandas as pd

from symprobe.constants import CONVERSION_IDX


def get_print_timestep(log_path):
    """Extracts the print timestep value from the log file

    Arguments:
    log_path -- str, path to the log file.

    Return:
    timestep -- float, print timestep value in ms.

    Raises:
    FileNotFoundError -- if the log file is not found.
    RuntimeError -- if there was a problem reading the log file
    ValueError -- if the print timestep value is not found or cannot be parsed.

    """
    try:
        with open(log_path, "r") as log_file:
            for line in log_file:
                if "print timestep" in line:
                    # Use regex to extract numerical value
                    match = re.search(
                        r"print timestep:\s*(\d+\.*\d*)\s*ms",
                        line,
                    )
                    if match:
                        return float(match.group(1))
    except FileNotFoundError as e:
        raise FileNotFoundError(f"log file at {log_path} not found.") from e
    except Exception as e:
        raise RuntimeError(f"error reading log file: {e}") from e

    # If no valid line is found
    raise ValueError("print timestep not found in the log file.")


def load_data(data_path, log_path, delimiter=","):
    """Loads the data from a csv file

    Arguments:
    data_path -- str, path to the data file.
    log_path -- str, path to the log file of the simulation.
    delimiter -- str, delimiter for the csv file, default value ,.

    Return:
    V -- ndarray, membrane potential values.
    t -- ndarray, timestep values.

    Raises:
    FileNotFoundError -- if the data file is not found.
    FileNotFoundError -- if the log file is not found.
    pd.errors.EmptyDataError -- if the data file is empty.
    pd.errors.ParserError -- if the data file cannot be parsed.
    RuntimeError -- if an error occurs during parsing.
    RuntimeError -- if there was a problem reading the log file
    ValueError -- if the print timestep value is not found or cannot be parsed.

    ValueError -- if the required column is missing in the CSV file.

    """
    try:
        df = pd.read_csv(data_path, delimiter=delimiter)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"data file at {data_path} not found.") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("file is empty.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("could not parse file.") from e
    except Exception as e:
        raise RuntimeError(f"an unexpected error occurred: {e}") from e

    # Get print timestep
    try:
        timestep = get_print_timestep(log_path)
    except FileNotFoundError as e:
        raise FileNotFoundError from e
    except RuntimeError as e:
        raise RuntimeError from e
    except ValueError as e:
        raise ValueError from e

    # Get column names
    columns = df.columns

    # Extract time and membrane potential
    time_vals = df[columns[0]].to_numpy()
    V = df[columns[1]].to_numpy()

    if len(columns) < 3:
        raise IndexError("missing point IDs in vtu file.")

    if columns[2] == "vtkOriginalPointIds":
        # Paraview export of single cell data
        cell_ids = np.unique(df[columns[2]].to_numpy())
        nb_cells = len(cell_ids)
        nb_timesteps = time_vals.size // nb_cells
        tmp_V = np.zeros((nb_timesteps, nb_cells))  # Temporary placeholder

        for i in range(nb_cells):
            # Get the output of each cell
            idx = np.arange(i, V.size, nb_cells)
            tmp_V[:, i] = V[idx]

    else:
        raise ValueError(f"incorrect column {columns[2]}")

    V = tmp_V  # Reset V for plotting
    # Create correct timesteps in seconds
    t = np.linspace(0, (nb_timesteps - 1) * timestep * 1e-3, nb_timesteps)

    return V, t


def get_range(num_range):
    """Converts the input range into a list of numbers

    Arguments:
    num_range -- str, range of number from the input argument.

    Return:
    num_list -- list[int], list of numbers extracted from the range.

    """
    if len(num_range) == 1:
        split = num_range[0].split("-")
        if len(split) == 1:
            # Single number
            num_list = int(num_range[0])
        else:
            # Range
            num_list = [i for i in range(int(split[0]), int(split[1]) + 1)]
    else:
        # Convert to list to int
        num_list = [int(i) for i in num_range]

    return num_list


def convert_connections(cube_node_list):
    """Converts the connections of the cubic element to six tetrahedra
    connections

    Arguments:
    cube_node_list -- list[int], list of nodes for the cubic element.

    Return:
    tet_node_list -- list[list[int]], list of the six node lists for the
            tetrahedral elements.

    """
    tet_node_list = []
    for idx_list in CONVERSION_IDX:
        tet_list = [cube_node_list[idx] for idx in idx_list]
        tet_node_list.append(tet_list)

    return tet_node_list


def print_quality(quality_array, metric_name):
    """Prints statistical information about the quality metric

    Arguments:
    quality_array -- np.array, quality data for mesh nodes.
    metric_name -- str, name of the quality metric.

    Return:

    """
    print("{} quality data:".format(metric_name))
    print(
        "Mean: {:.2f} \u00b1 {:.2f}".format(
            np.mean(quality_array),
            np.std(quality_array),
        )
    )
    print(
        "Min-Max: [{:.2f} - {:.2f}]".format(
            np.min(quality_array),
            np.max(quality_array),
        )
    )
    print("25th percentile: {:.2f}".format(np.percentile(quality_array, 25)))
    print("Median: {:.2f}".format(np.median(quality_array)))
    print("75th percentile: {:.2f}".format(np.percentile(quality_array, 75)))
