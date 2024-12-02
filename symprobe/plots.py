#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plots.py

Plot functions used in the symprobe package
Author: Mathias Roesler
Date: 11/24
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_cell_data(V, t):
    """Plots the membrane potential of cells

    Arguments:
    V -- ndarray, array with data from N cells to be plotted.
    t -- ndarray, time vector.

    Return:

    Raises:
    ValueError -- if the shapes do not agree.

    """
    # Create figure and plot
    fig, ax = plt.subplots(dpi=300)

    if not V.shape[0] == t.shape[0]:
        raise ValueError("dimensions must agree.")

    for j in range(V.shape[1]):
        plt.plot(t, V[:, j])

    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (mV)")

    plt.xlim([0, max(t)])

    # Assume that cells are organised from ovaries to cervix
    plt.legend(["Ovarian end", "Centre", "Cervical end"])
    plt.tight_layout()
    plt.show()


def plot_resolution_convergence(comp_data, density_data, metric):
    """Plots the convergence for different resolution meshes

    Arguments:
    comp_data -- np.array, comparison data.
    density_data -- np.array, number of elements in each mesh.
    metric -- str, metric used for the comparison.

    Return:

    Raises:

    """
    # Create figure and plot
    fig, ax = plt.subplots(dpi=300)

    plt.plot(density_data, comp_data, "k.-")

    plt.xlabel("Mesh resolution")
    plt.ylabel("{}".format(metric.upper()))

    plt.show()


def plot_single_mesh_quality(quality_data, metric, mesh_name):
    """Plots the quality data for a mesh as a boxplot

    Arguments:
    quality_data -- np.array, quality data.
    metric -- str, name of the quality metric.
    mesh_name -- str, name of the mesh for title.

    Return:

    Raises:

    """
    # Create figure and plot
    fig, ax = plt.subplots(dpi=300)

    ax.boxplot(quality_data)

    ax.set_xticks([])  # Remove xticks
    plt.ylabel("{}".format(metric))

    plt.title(mesh_name)
    plt.show()


def plot_multi_mesh_quality(quality_dict, density_data, metric):
    """Plots the quality data for multiple meshes as single points with
    error bars

    Arguments:
    quality_dict -- dict, dictionnary with the quality data as value
    and mesh number as key.
    density_data -- np.array, number of elements in each mesh.
    metric -- str, name of the quality metric.

    Return:

    Raises:

    """
    # Create figure and plot
    fig, ax = plt.subplots(dpi=300)
    data = np.zeros(len(quality_dict.keys()))  # Empty list for data
    yerr = np.zeros(len(quality_dict.keys()))  # Empty list for error
    cpt = 0  # Loop counter

    for sim_nb, quality_data in quality_dict.items():
        data[cpt] = np.mean(quality_data)
        yerr[cpt] = np.std(quality_data)

        cpt += 1

    ax.errorbar(
        density_data,
        data,
        yerr=yerr,
        fmt=".-",
        color="black",
        capsize=5,
        label="Mean ± Std",
    )

    plt.xlabel("Mesh resolution")
    plt.ylabel("{}".format(metric))
    plt.show()
