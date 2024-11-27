#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_plots.py

Unit tests for the plot functions in plots.py.
Author: Mathias Roesler
Date: 11/24

This file contains test cases for the functions:
- plot_cell_data
- plot_resolution_convergence
- plot_single_mesh_quality
- plot_multi_mesh_quality

The tests cover various scenarios including valid inputs, invalid inputs.
"""

import pytest
import numpy as np

from unittest.mock import patch
from symprobe.plots import (
    plot_cell_data,
    plot_resolution_convergence,
    plot_single_mesh_quality,
    plot_multi_mesh_quality,
)


def test_plot_cell_data_shape_mismatch():
    # Define mismatched shapes for V and t
    V = np.random.rand(100, 3)  # 100 time steps, 3 cells
    t = np.linspace(0, 10, 99)  # 99 time steps

    # Expect a ValueError
    with pytest.raises(ValueError, match="dimensions must agree."):
        plot_cell_data(V, t)


@patch("matplotlib.pyplot.show")  # Prevent plots from displaying
def test_plot_cell_data_success(mock_show):
    # Define matching shapes for V and t
    V = np.random.rand(100, 3)  # 100 time steps, 3 cells
    t = np.linspace(0, 10, 100)  # 100 time steps

    # Run the function
    plot_cell_data(V, t)

    # Verify that `show` is called to display the plot
    mock_show.assert_called_once()


# Test plot_resolution_convergence function
@patch("matplotlib.pyplot.show")  # Prevent plots from displaying
def test_plot_resolution_convergence_valid(mock_show):
    comp_data = np.array([1.0, 2.0, 1.5, 1.2])  # Sample comparison data
    metric = "rmse"  # Metric to be plotted

    # Run the function
    plot_resolution_convergence(comp_data, metric)

    # Verify that `show` was called to display the plot
    mock_show.assert_called_once()


@patch("matplotlib.pyplot.show")  # Prevent plots from displaying
def test_plot_resolution_convergence_empty_data(mock_show):
    comp_data = np.array([])  # Empty comparison data
    metric = "rmse"

    # Run the function
    plot_resolution_convergence(comp_data, metric)

    # Ensure plt.show was still called even with empty data
    mock_show.assert_called_once()


# Test plot_multi_mesh_quality function
@patch("matplotlib.pyplot.show")  # Prevent plots from displaying
def test_plot_multi_mesh_quality_valid(mock_show):
    quality_dict = {"test_1": 0.0, "test_2": 1.0}  # Sample dict
    metric = "rmse"  # Metric to be plotted

    # Run the function
    plot_multi_mesh_quality(quality_dict, metric)

    # Verify that `show` was called to display the plot
    mock_show.assert_called_once()


# Test plot_single_mesh_quality function
@patch("matplotlib.pyplot.show")  # Prevent plots from displaying
def test_plot_single_mesh_quality_valid(mock_show):
    quality_data = np.array([0.0, 1.0])  # Sample data
    mesh_name = "test_mesh"
    metric = "rmse"  # Metric to be plotted

    # Run the function
    plot_single_mesh_quality(quality_data, metric, mesh_name)

    # Verify that `show` was called to display the plot
    mock_show.assert_called_once()
