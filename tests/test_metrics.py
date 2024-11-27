#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_metrics.py

Unit tests for the metrics functions in metrics.py.
Author: Mathias Roesler
Date: 11/24

This file contains test cases for the functions:
- check_broadcasting
- compute_rmse
- compute_mae
- compute_mse
- compute_comparison

The tests cover various scenarios including valid inputs, invalid inputs,
and edge cases.
"""

import pytest
import numpy as np

from symprobe.metrics import (
    compute_rmse,
    compute_mae,
    compute_mse,
    compute_comparison,
    check_broadcasting,
)


# Test check_broadcasting function
def test_check_broadcasting_valid():
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])
    # Should not raise an error
    check_broadcasting(y_true, y_pred)


def test_check_broadcasting_invalid():
    y_true = np.array([1, 2])
    y_pred = np.array([1, 2, 3])
    # Should raise ValueError
    with pytest.raises(ValueError):
        check_broadcasting(y_true, y_pred)


# Test compute_rmse function
def test_compute_rmse_valid():
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])
    result = compute_rmse(y_true, y_pred)
    assert np.isclose(result, 0.0), f"Expected 0.0, but got {result}"


def test_compute_rmse_non_broadcastable():
    y_true = np.array([1, 2])
    y_pred = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        compute_rmse(y_true, y_pred)


def test_compute_rmse_edge_case():
    y_true = np.array([0])
    y_pred = np.array([0])
    result = compute_rmse(y_true, y_pred)
    assert np.isclose(result, 0.0), f"Expected 0.0, but got {result}"


# Test compute_mae function
def test_compute_mae_valid():
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])
    result = compute_mae(y_true, y_pred)
    assert np.isclose(result, 0.0), f"Expected 0.0, but got {result}"


def test_compute_mae_non_broadcastable():
    y_true = np.array([1, 2])
    y_pred = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        compute_mae(y_true, y_pred)


def test_compute_mae_edge_case():
    y_true = np.array([0])
    y_pred = np.array([0])
    result = compute_mae(y_true, y_pred)
    assert np.isclose(result, 0.0), f"Expected 0.0, but got {result}"


# Test compute_mse function
def test_compute_mse_valid():
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])
    result = compute_mse(y_true, y_pred)
    assert np.isclose(result, 0.0), f"Expected 0.0, but got {result}"


def test_compute_mse_non_broadcastable():
    y_true = np.array([1, 2])
    y_pred = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        compute_mse(y_true, y_pred)


def test_compute_mse_edge_case():
    y_true = np.array([0])
    y_pred = np.array([0])
    result = compute_mse(y_true, y_pred)
    assert np.isclose(result, 0.0), f"Expected 0.0, but got {result}"

    # Test compute_comparison function


def test_compute_comparison_rmse_valid():
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])
    result = compute_comparison(y_true, y_pred, "rmse")
    expected = compute_rmse(y_true, y_pred)
    assert np.isclose(
        result, expected), f"Expected {expected}, but got {result}"


def test_compute_comparison_mae_valid():
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])
    result = compute_comparison(y_true, y_pred, "mae")
    expected = compute_mae(y_true, y_pred)
    assert np.isclose(
        result, expected), f"Expected {expected}, but got {result}"


def test_compute_comparison_mse_valid():
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])
    result = compute_comparison(y_true, y_pred, "mse")
    expected = compute_mse(y_true, y_pred)
    assert np.isclose(
        result, expected), f"Expected {expected}, but got {result}"


def test_compute_comparison_invalid_metric():
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])
    # Should raise ValueError due to invalid metric
    with pytest.raises(ValueError):
        compute_comparison(y_true, y_pred, "invalid_metric")


def test_compute_comparison_non_broadcastable():
    y_true = np.array([1, 2])
    y_pred = np.array([1, 2, 3])
    # Should raise ValueError due to non-broadcastable arrays
    with pytest.raises(ValueError):
        compute_comparison(y_true, y_pred, "rmse")


def test_compute_comparison_edge_case():
    y_true = np.array([0])
    y_pred = np.array([0])
    result_rmse = compute_comparison(y_true, y_pred, "rmse")
    result_mae = compute_comparison(y_true, y_pred, "mae")
    result_mse = compute_comparison(y_true, y_pred, "mse")

    # All should be 0 for identical arrays
    assert np.isclose(result_rmse, 0.0), f"Expected 0.0, but got {result_rmse}"
    assert np.isclose(result_mae, 0.0), f"Expected 0.0, but got {result_mae}"
    assert np.isclose(result_mse, 0.0), f"Expected 0.0, but got {result_mse}"
