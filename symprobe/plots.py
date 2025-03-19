#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plots.py

Plot functions used in the symprobe package
Author: Mathias Roesler
Date: 11/24
"""

import matplotlib.pyplot as plt

from .constants import LEFT, RIGHT, BOTTOM, COLOURS, PARAM, UNITS


def plot_cell_data(V, t, estrus="estrus"):
    """Plots the membrane potential of cells

    Arguments:
    V -- ndarray, array with data from N cells to be plotted.
    t -- ndarray, time vector.
    estrus -- str, estrus phase, default value "estrus".

    Return:

    Raises:
    ValueError -- if the shapes do not agree.

    """
    # Create figure and plot

    if not V.shape[0] == t.shape[0]:
        raise ValueError("dimensions must agree.")

    for j in range(V.shape[1]):
        fig, ax = plt.subplots(dpi=300)
        plt.plot(t, V[:, j], COLOURS[estrus], linestyle="-")

        plt.xlabel("Time (s)", fontsize=15)
        plt.ylabel("Amplitude (mV)", fontsize=15)

        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        plt.xlim([0, max(t)])
        plt.ylim([-70, 15])

        plt.subplots_adjust(left=LEFT, right=RIGHT, bottom=BOTTOM)
        plt.show()


def plot_cell_comparison(V1, V2, t, estrus="estrus"):
    """Plots the membrane potential of cells from two simulations

    Arguments:
    V1 -- ndarray, array with data from N cells to be plotted.
    V2 -- ndarray, array to compare with N cells to be plotted.
    t -- ndarray, time vector.
    estrus -- str, estrus phase, default value "estrus".

    Return:

    Raises:
    ValueError -- if the shapes do not agree.

    """
    # Create figure and plot

    if not V1.shape[0] == t.shape[0] or not V1.shape[0] == V2.shape[0]:
        raise ValueError("dimensions must agree.")

    fig, ax = plt.subplots(dpi=300)
    plt.plot(t, V1, COLOURS[estrus], linestyle="-")
    plt.plot(t, V2, "grey", linestyle="--")

    plt.xlabel("Time (s)", fontsize=15)
    plt.ylabel("Amplitude (mV)", fontsize=15)

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    plt.xlim([min(t), max(t)])
    plt.ylim([-70, 15])

    plt.legend(["Idealised", "Realistic"])
    plt.title(f"{estrus.capitalize()}")
    plt.subplots_adjust(left=LEFT, right=RIGHT, bottom=BOTTOM)
    plt.show()


def plot_resolution_convergence(comp_dict, density_data, metric):
    """Plots the convergence for different resolution meshes

    Arguments:
    comp_dict -- dict[np.array], keys are estrus stages and values are
    comparison data.
    density_data -- np.array, number of elements in each mesh.
    metric -- str, metric used for the comparison.

    Return:

    Raises:

    """
    # Create figure and plot
    fig, ax = plt.subplots(dpi=300)

    for stage, comp_data in comp_dict.items():
        plt.plot(density_data, comp_data, COLOURS[stage] + ".-")

    plt.legend([estrus.capitalize() for estrus in comp_dict.keys()])

    plt.xlabel("Number of elements")
    plt.ylabel("{} (mV)".format(metric.upper()))

    ax.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))

    plt.subplots_adjust(left=LEFT, right=RIGHT, bottom=BOTTOM)
    plt.show()


def plot_parameter_comparison(comp_dict, parameter_values, metric, parameter):
    """Plots the convergence for different resolution meshes

    Arguments:
    comp_dict -- dict[np.array], keys are estrus stages and values are
    comparison data.
    parameter_values, np.array, values of the parameter.
    metric -- str, metric used for the comparison.
    parameter -- str, name of the parameter.

    Return:

    Raises:

    """
    # Create figure and plot
    fig, ax = plt.subplots(dpi=300)

    for stage, comp_data in comp_dict.items():
        plt.plot(parameter_values, comp_data, COLOURS[stage] + ".-")

    if len(comp_dict.keys()) != 1:
        plt.legend([estrus.capitalize() for estrus in comp_dict.keys()])

    plt.xlabel(PARAM[parameter] + " " + UNITS[parameter])
    plt.ylabel("{}".format(metric.upper()))

    plt.subplots_adjust(left=LEFT, right=RIGHT, bottom=BOTTOM)
    plt.show()


def plot_spike_propagation(spike_dict, parameter_values, parameter):
    """Plots the number of spikes propagated to the cervix

    Arguments:
    spike_dict -- dict[np.array], keys are estrus stages and values are
    spike propagation data.
    parameter_values, np.array, values of the parameter.
    parameter -- str, name of the parameter.

    Return:

    Raises:

    """
    # Create figure and plot
    fig, ax = plt.subplots(dpi=300)

    for stage, spike_data in spike_dict.items():
        plt.plot(parameter_values, spike_data, COLOURS[stage] + ".-")

    if len(spike_dict.keys()) != 1:
        plt.legend([estrus.capitalize() for estrus in spike_dict.keys()])

    plt.xlabel(PARAM[parameter] + " " + UNITS[parameter])
    plt.ylabel("Number of propagated spikes")

    plt.subplots_adjust(left=LEFT, right=RIGHT, bottom=BOTTOM)
    plt.show()
