#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_metrics.py

Unit tests for the metrics functions in metrics.py.
Author: Mathias Roesler
Date: 03/25

This file contains test cases for the functions:
- _fct_setup
- _data_extract
- _reorder_V
- resolution_fct
- cell_fct
- parameter_fct
- comparison_fct

The tests cover various scenarios including valid inputs, invalid inputs,
and edge cases.
"""

import numpy as np
import pytest
from unittest.mock import patch
from symprobe import constants
from symprobe.extract_script_fct import (
    _fct_setup,
    _data_extract,
    _reorder_V,
    resolution_fct,
    cell_fct,
    parameter_fct,
    comparison_fct,
)


@pytest.mark.parametrize(
    "rng, estrus, expected_nb_sims, expected_estrus",
    [
        ("5", "proestrus", [5], ["proestrus"]),
        (["1-3"], "estrus", [1, 2, 3], ["estrus"]),
        (["1-3"], "all", [1, 2, 3], constants.ESTRUS),
    ],
)
def test_fct_setup(rng, estrus, expected_nb_sims, expected_estrus):
    nb_sims, estrus_result = _fct_setup(rng, estrus)
    assert nb_sims == expected_nb_sims
    assert estrus_result == expected_estrus


def test_fct_setup_invalid():
    with pytest.raises(
        ValueError, match="estrus cannot be all with a single simulation"
    ):
        _fct_setup("2", "all")


@patch("symprobe.utils.load_data")
def test_data_extract(mock_load_data):
    mock_load_data.return_value = (
        np.array([[1.0, 2.0], [3.0, 4.0]]),
        np.array([0, 1]),
        np.array([10, 20, 30]),
    )

    V, t, cell_ids, log_path = _data_extract("sim", 1, "/fake/path", ",")

    assert log_path == "/fake/path/log/sim_001.log"
    assert V.shape == (2, 2)
    assert np.array_equal(t, np.array([0, 1]))
    assert np.array_equal(cell_ids, np.array([10, 20, 30]))


@patch("symprobe.utils.load_data", side_effect=Exception("File not found"))
def test_data_extract_failure(mock_load_data):
    with pytest.raises(Exception, match="File not found"):
        _data_extract("sim", 1, "/fake/path", ",")


def test_reorder_V():
    V = np.array([[1, 2, 3], [4, 5, 6]])
    cell_ids = np.array([10, 20, 30])
    ordered_ids = np.array([30, 10, 20])

    reordered_V = _reorder_V(V, cell_ids, ordered_ids)

    expected_V = np.array([[3, 1, 2], [6, 4, 5]])
    assert np.array_equal(reordered_V, expected_V)


def test_reorder_V_invalid():
    with pytest.raises(
        ValueError, match="cell ids and ordered ids should have same length"
    ):
        _reorder_V(np.array([[1, 2], [3, 4]]),
                   np.array([10, 20]), np.array([30]))


@patch("symprobe.utils.load_data")
@patch("symprobe.constants.RES_DICT", {"mesh_1": 100})
@patch("symprobe.plots.plot_resolution_convergence")
def test_resolution_fct(mock_plot, mock_load_data):
    mock_load_data.return_value = (
        np.array([[1.0, 2.0]]), np.array([0]), np.array([1]))

    with patch("symprobe.utils.get_mesh_name", return_value="mesh_1"):
        resolution_fct("/path", "estrus_data", "rmse",
                       "1", "sim", "proestrus", ",")

    mock_plot.assert_called_once()


@patch("symprobe.utils.load_data")
@patch("symprobe.plots.plot_cell_data")
def test_cell_fct(mock_plot, mock_load_data):
    mock_load_data.return_value = (
        np.array([[-70, -70, -70], [-50, -70, -60],
                 [-70, -50, -50], [-70, -70, -70]]),
        np.array([0, 1, 2, 3]),
        np.array([10, 20, 30]),
    )

    with (
        patch("symprobe.utils.get_mesh_name",
              return_value="uterus_scaffold_scaled_3"),
    ):
        cell_fct("/path", "1", "sim", "proestrus", ",")

    mock_plot.assert_called()


@patch("symprobe.utils.load_data")
@patch("symprobe.utils.get_param_value", return_value=0.5)
@patch("symprobe.plots.plot_parameter_comparison")
@patch("symprobe.plots.plot_spike_propagation")
def test_parameter_fct(
    mock_spike_plot,
    mock_param_plot,
    mock_get_param,
    mock_load_data,
):
    mock_load_data.return_value = (
        np.array([[-70, -70, -70], [-50, -70, -60],
                 [-70, -50, -50], [-70, -70, -70]]),
        np.array([0, 1, 2, 3]),
        np.array([10, 20, 30]),
    )

    with (
        patch("symprobe.utils.get_mesh_name",
              return_value="uterus_scaffold_scaled_3"),
    ):
        parameter_fct(
            "/path",
            "param",
            "estrus_data",
            "rmse",
            "1",
            "sim",
            "proestrus",
            ",",
        )

    mock_param_plot.assert_called()
    mock_spike_plot.assert_called()


@patch("symprobe.utils.load_data")
@patch("symprobe.metrics.compute_comparison", return_value=0.9)
@patch("symprobe.plots.plot_cell_comparison")
def test_comparison_fct(mock_plot, mock_metric, mock_load_data):
    mock_load_data.return_value = (
        np.array([[1.0, 2.0]]),
        np.array([0]),
        np.array([10, 20, 30]),
    )

    with (
        patch("symprobe.utils.get_mesh_name", return_value="mesh_1"),
        patch.dict("symprobe.constants.PTS_DICT", {
                   "mesh_1": np.array([10, 20, 30])}),
    ):
        comparison_fct(
            "/path",
            "metric",
            "realistic",
            "ideal",
            "sub",
            "1",
            "sim",
            "proestrus",
            ",",
        )

    mock_plot.assert_called()
    mock_metric.assert_called()
