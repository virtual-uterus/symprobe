#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_mesh.py

Unit tests for the mesh functions in mesh.py.
Author: Mathias Roesler
Date: 11/24

This file contains test cases for the functions:
- quality_information
- distance_information
- neighbour_distance

The tests cover various scenarios including valid inputs, invalid inputs,
and edge cases.
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from symprobe.mesh import (
    neighbour_distance,
    distance_information,
    quality_information,
)


def test_neighbour_distance_valid():
    # Mock pyvista read and the mesh structure
    mesh = MagicMock()
    mesh.n_cells = 3
    mesh.cell_centers.return_value.points = np.array(
        [[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    mesh.cell_neighbors.side_effect = [[1, 2], [0, 2], [0, 1]]

    with patch("pyvista.read", return_value=mesh):
        distances = neighbour_distance("fake_mesh.vtk")
        assert len(distances) == mesh.n_cells
        assert distances[0] > 0  # Example basic check


def test_neighbour_distance_file_not_found():
    with pytest.raises(FileNotFoundError):
        neighbour_distance("nonexistent_file.vtk")


@patch(
    "symprobe.mesh.neighbour_distance",
    return_value=np.array([1.0, 2.0, 3.0]),
)
def test_distance_information_single_mesh(mock_neighbour_distance):
    with patch("symprobe.mesh.neighbour_distance", mock_neighbour_distance):
        distance_information("file", "mesh", None, "vtu")
        # Just ensure no exception, check stdout with capsys if needed.


@patch("symprobe.utils.get_range", return_value=[1, 2])
@patch(
    "symprobe.mesh.neighbour_distance",
    return_value=np.array([1.0, 2.0, 3.0]),
)
def test_distance_information_range(mock_get_range, mock_neighbour_distance):
    distance_information("file", "mesh", [1, 2], "vtu")
    # Further assertions or validate calls


@patch("symprobe.paraview_fct.paraview_quality")
@patch("symprobe.plots.plot_single_mesh_quality")
def test_quality_information_single(mock_plot, mock_quality):
    mock_quality.return_value = np.array([1, 2, 3])
    quality_information("file", "mesh", "ar", None, "vtu")
    mock_quality.assert_called_once()
