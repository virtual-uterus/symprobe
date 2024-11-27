#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
metrics.py

Metrics used to compare simulation outputs
Author: Mathias Roesler
Date: 11/24
"""

import numpy as np


def check_broadcasting(y_true, y_pred):
    """Checks if the arrays are broadcastable

    Arguments:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, predicted values.

    Return:

    Raises:
    ValueError -- if the arrays are not broadcastable

    """
    try:
        # Check broadcasting compatibility
        np.broadcast_arrays(y_true, y_pred)
    except ValueError:
        raise


def compute_rmse(y_true, y_pred):
    """Computes the root mean square error between two arrays

    Arguments:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, predicted values.

    Return:

    Raises:
    ValueError -- if the arrays are not broadcastable

    """
    # Check broadcasting before calculation
    try:
        check_broadcasting(y_true, y_pred)
    except ValueError:
        raise
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def compute_mae(y_true, y_pred):
    """Computes the mean average error between arrays.

    Arguments:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, predicted values.

    Return:

    Raises:
    ValueError -- if the arrays are not broadcastable

    """
    # Check broadcasting before calculation
    try:
        check_broadcasting(y_true, y_pred)
    except ValueError:
        raise
    return np.mean(np.abs(y_true - y_pred))


def compute_mse(y_true, y_pred):
    """Computes the mean squared error between arrays.

    Arguments:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, predicted values.

    Return:

    Raises:
    ValueError -- if the arrays are not broadcastable

    """
    # Check broadcasting before calculation
    try:
        check_broadcasting(y_true, y_pred)
    except ValueError:
        raise
    return np.mean((y_true - y_pred) ** 2)


def compute_comparison(y_true, y_pred, metric):
    """Computes the comparison between y_true and y_pred based on the metric

    Arguments:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.
    metric -- str, comparison metric {rmse, mae, mse}.

    Return:
    comp_point -- float, comparison point.

    Raises:
    ValueError -- if the provided metric is not one of
    {'rmse', 'mae', 'mse'}.
    ValueError -- if the arrays are not broadcastable

    """
    try:
        match metric:
            case "rmse":
                return compute_rmse(y_true, y_pred)

            case "mae":
                return compute_mae(y_true, y_pred)

            case "mse":
                return compute_mse(y_true, y_pred)
            case _:
                raise ValueError("invalid metric {}\n".format(metric))
    except ValueError:
        raise
