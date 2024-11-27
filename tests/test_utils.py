#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_utils.py

Unit tests for the utility functions in utils.py.
Author: Mathias Roesler
Date: 11/24

This file contains test cases for the functions:
- get_print_timestep
- load_data
- get_range
- print_quality

The tests cover various scenarios including valid inputs, invalid inputs.
"""

import pytest
import numpy as np
import pandas as pd

from symprobe import utils
from unittest.mock import patch, mock_open


def test_get_print_timestep():
    log_content = "Some log content\nprint timestep: 0.5 ms\nOther content"
    with patch("builtins.open", mock_open(read_data=log_content)):
        assert utils.get_print_timestep("dummy_path.log") == 0.5


def test_get_print_timestep_missing():
    log_content = "No timestep information here"
    with patch("builtins.open", mock_open(read_data=log_content)):
        with pytest.raises(ValueError):
            utils.get_print_timestep("dummy_path.log")


def test_get_print_timestep_file_not_found():
    with pytest.raises(FileNotFoundError):
        utils.get_print_timestep("non_existent.log")


def test_load_data(mocker):
    # Mock data for CSV
    data = {
        "Time": [0, 0, 1, 1],
        "V": [0.1, 0.5, 0.2, 0.6],
        "vtkOriginalPointIds": [0, 1, 0, 1],
    }
    mock_df = pd.DataFrame(data)
    mocker.patch("pandas.read_csv", return_value=mock_df)

    # Mock get_print_timestep
    mocker.patch("symprobe.utils.get_print_timestep", return_value=1.0)

    V, t = utils.load_data("dummy_data.csv", "dummy_log.log")

    assert V.shape == (2, 2)
    assert t.size == 2
    np.testing.assert_array_almost_equal(V, [[0.1, 0.5], [0.2, 0.6]])
    np.testing.assert_array_almost_equal(t, [0.0, 0.001])  # in seconds


def test_load_data_file_not_found(mocker):
    mocker.patch(
        "pandas.read_csv", side_effect=FileNotFoundError("CSV file not found.")
    )
    mocker.patch("symprobe.utils.get_print_timestep", return_value=1.0)

    with pytest.raises(FileNotFoundError):
        utils.load_data("non_existent.csv", "dummy_log.log")


def test_load_data_missing_point_ids(mocker):
    # Mock data for CSV without the required column
    data = {
        "Time": [0, 1],
        "V": [0.1, 0.2],
        # No vtkOriginalPointIds column
    }
    mock_df = pd.DataFrame(data)
    mocker.patch("pandas.read_csv", return_value=mock_df)
    mocker.patch("symprobe.utils.get_print_timestep", return_value=1.0)

    with pytest.raises(IndexError):
        utils.load_data("dummy_data.csv", "dummy_log.log")


def test_load_data_incorrect_column(mocker):
    # Mock data for CSV without the required column
    data = {
        "Time": [0, 1],
        "V": [0.1, 0.2],
        "Incorrect column": [0, 1],
    }
    mock_df = pd.DataFrame(data)
    mocker.patch("pandas.read_csv", return_value=mock_df)
    mocker.patch("symprobe.utils.get_print_timestep", return_value=1.0)

    with pytest.raises(ValueError):
        utils.load_data("dummy_data.csv", "dummy_log.log")


def test_get_range_single_number():
    assert utils.get_range(["5"]) == 5


def test_get_range_range():
    assert utils.get_range(["1-3"]) == [1, 2, 3]


def test_get_range_list():
    assert utils.get_range(["1", "3", "5"]) == [1, 3, 5]


def test_print_quality(capsys):
    quality_data = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
    utils.print_quality(quality_data, "Test Metric")

    captured = capsys.readouterr()
    assert "Mean: 0.70 ± 0.14" in captured.out
    assert "Min-Max: [0.50 - 0.90]" in captured.out
    assert "25th percentile: 0.60" in captured.out
    assert "Median: 0.70" in captured.out
    assert "75th percentile: 0.80" in captured.out
