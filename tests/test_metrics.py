#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_metrics.py

Unit tests for the metrics functions in metrics.py.
Author: Mathias Roesler
Date: 03/25

This file contains test cases for the functions:
- check_broadcasting
- compute_rmse
- compute_mae
- compute_mse
- compute_van_rossum_distance
- compute_comparison

The tests cover various scenarios including valid inputs, invalid inputs,
and edge cases.
"""

import pytest
import numpy as np
from symprobe.metrics import (
    check_broadcasting,
    compute_rmse,
    compute_mae,
    compute_mse,
    compute_van_rossum_distance,
    compute_comparison,
)
from unittest.mock import patch


@pytest.fixture
def sample_data():
    return {
        "simple": (np.array([1, 2, 3]), np.array([2, 3, 4])),
        "multidim": (np.array([[1, 2], [3, 4]]), np.array([[2, 3], [4, 5]])),
        "broadcast": (np.array([[1, 2], [3, 4]]), np.array([1, 2])),
        "spike_train": (np.array([0, 1, 0, 1, 0]), np.array([0, 0, 1, 0, 1])),
        "time": np.array([0, 1, 2, 3, 4]),
        "zeros": (np.array([0, 0, 0]), np.array([0, 0, 0])),
        "negative": (np.array([-1, -2, -3]), np.array([-2, -3, -4])),
        "large": (np.array([1e6, 2e6, 3e6]), np.array([2e6, 3e6, 4e6])),
    }


# check_broadcasting tests


def test_check_broadcasting_scalar():
    check_broadcasting(np.array([1, 2, 3]), 5)


def test_check_broadcasting_empty():
    check_broadcasting(np.array([]), np.array([]))


# Expanded tests for compute_rmse, compute_mae, compute_mse


@pytest.mark.parametrize("func", [compute_rmse, compute_mae, compute_mse])
@pytest.mark.parametrize(
    "case", ["simple", "multidim", "broadcast", "zeros", "negative", "large"]
)
def test_compute_metrics(func, case, sample_data):
    y_true, y_pred = sample_data[case]
    result = func(y_true, y_pred)
    assert isinstance(result, (float, np.float64))
    assert not np.isnan(result)
    assert not np.isinf(result)


def test_compute_metrics_perfect_prediction():
    y = np.array([1, 2, 3])
    for func in [compute_rmse, compute_mae, compute_mse]:
        assert func(y, y) == 0


# compute_van_rossum_distance tests


@patch("elephant.spike_train_dissimilarity.van_rossum_distance")
def test_compute_van_rossum_distance_empty(mock_vrd, sample_data):
    time = sample_data["time"]
    mock_vrd.return_value = np.array([[0, 0]])
    result = compute_van_rossum_distance(np.array([]), np.array([]), time)
    assert result == 0


@patch("elephant.spike_train_dissimilarity.van_rossum_distance")
def test_compute_van_rossum_distance_identical(mock_vrd, sample_data):
    y = np.array([0, 1, 0, 1, 0])
    time = sample_data["time"]
    mock_vrd.return_value = np.array([[0, 0]])
    result = compute_van_rossum_distance(y, y, time)
    assert result == 0


# compute_comparison tests


@pytest.mark.parametrize("metric", ["rmse", "mae", "mse", "vrd"])
@pytest.mark.parametrize(
    "case", ["simple", "multidim", "broadcast", "zeros", "negative", "large"]
)
def test_compute_comparison_all_metrics(metric, case, sample_data):
    y_true, y_pred = sample_data[case]
    time = sample_data["time"]

    if metric == "vrd" and case in ["multidim", "broadcast"]:
        with pytest.raises(ValueError, match="array should be 1D"):
            compute_comparison(y_true, y_pred, metric, time=time)
    else:
        result = compute_comparison(y_true, y_pred, metric, time=time)
        assert isinstance(result, (float, np.float64))
        assert not np.isnan(result)
        assert not np.isinf(result)


def test_compute_comparison_vrd_missing_time(sample_data):
    y_true, y_pred = sample_data["spike_train"]
    with pytest.raises(ValueError):
        compute_comparison(y_true, y_pred, "vrd")


# Error handling tests


@pytest.mark.parametrize(
    "func", [compute_rmse, compute_mae,
             compute_mse, compute_van_rossum_distance]
)
def test_error_handling(func):
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2])
    with pytest.raises(ValueError):
        if func == compute_van_rossum_distance:
            func(y_true, y_pred, np.array([0, 1, 2]))
        else:
            func(y_true, y_pred)
