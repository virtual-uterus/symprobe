#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_utils.py

Unit tests for the utility functions in utils.py.
Author: Mathias Roesler
Date: 03/25

This file contains test cases for the functions:
- get_print_timestep
- get_mesh_name
- get_param_value
- load_data
- get_range
- extract_spike_times
- create_spike_train
- estimate_velocity

The tests cover various scenarios including valid inputs, invalid inputs,
and edge cases.
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import mock_open, patch
from symprobe.utils import (
    get_print_timestep,
    get_mesh_name,
    get_param_value,
    load_data,
    get_range,
    extract_spike_times,
    create_spike_train,
    estimate_velocity,
)
from neo.core import SpikeTrain
import quantities as quant


@pytest.fixture
def mock_log_file():
    return """
    Simulation log
    print timestep: 0.1 ms
    mesh: test_mesh
    some_param: 3.5
    """.strip()


@patch("builtins.open", new_callable=mock_open, read_data="print timestep: 0.1 ms\n")
def test_get_print_timestep(mock_file):
    assert get_print_timestep("log.txt") == 0.1


@patch("builtins.open", side_effect=FileNotFoundError)
def test_get_print_timestep_file_not_found(mock_file):
    with pytest.raises(FileNotFoundError):
        get_print_timestep("missing.txt")


@patch("builtins.open", new_callable=mock_open, read_data="mesh: test_mesh\n")
def test_get_mesh_name(mock_file):
    assert get_mesh_name("log.txt") == "test_mesh"


@patch("builtins.open", side_effect=FileNotFoundError)
def test_get_mesh_name_file_not_found(mock_file):
    with pytest.raises(FileNotFoundError):
        get_mesh_name("missing.txt")


@patch("builtins.open", new_callable=mock_open, read_data="param1: 2.5\n")
def test_get_param_value(mock_file):
    assert get_param_value("log.txt", "param1") == 2.5


@patch("builtins.open", side_effect=FileNotFoundError)
def test_get_param_value_file_not_found(mock_file):
    with pytest.raises(FileNotFoundError):
        get_param_value("missing.txt", "param1")


@patch("pandas.read_csv")
def test_load_data(mock_read_csv, mock_log_file):
    mock_df = pd.DataFrame(
        {
            "Time": [0, 0, 0, 1, 1, 1],
            "V": [10, -40, 30, 11, -41, 29],
            "vtkOriginalPointIds": [0, 1, 2, 0, 1, 2],
        }
    )
    mock_read_csv.return_value = mock_df

    with patch("builtins.open", new_callable=mock_open, read_data=mock_log_file):
        V, t, cell_ids = load_data("data.csv", "log.txt")

    assert V.shape == (2, 3)
    assert len(t) == 2
    assert len(cell_ids) == 3


@pytest.mark.parametrize(
    "num_range, expected",
    [(["5"], 5), (["1-3"], [1, 2, 3]), (["2", "4", "6"], [2, 4, 6])],
)
def test_get_range(num_range, expected):
    assert get_range(num_range) == expected


@pytest.mark.parametrize(
    "signal, time, height, expected",
    [
        ([0, -40, -30, -60, -50, -45], [0, 1, 2, 3, 4, 5], -50, [2]),
        ([0, -20, -10, -5, -10, -20], [0, 1, 2, 3, 4, 5], -10, [3]),
    ],
)
def test_extract_spike_times(signal, time, height, expected):
    spike_times = extract_spike_times(np.array(signal), np.array(time), height)
    np.testing.assert_array_equal(spike_times, np.array(expected))


def test_create_spike_train():
    spike_times = np.array([0.1, 0.5, 1.0])
    spike_train = create_spike_train(spike_times, 2.0)
    assert isinstance(spike_train, SpikeTrain)
    assert spike_train.t_stop == 2.0 * quant.s


def test_estimate_velocity():
    V = np.array([[-70, -50, -30], [-70, -50, 30], [-70, 50, 30]])
    t = np.array([0, 1, 2])

    with pytest.raises(ValueError):
        estimate_velocity(V, t, "uterus_scaffold_scaled_3")
