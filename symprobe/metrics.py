#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
metrics.py

Metrics used to compare simulation outputs
Author: Mathias Roesler
Date: 11/24
"""

import symprobe.utils

import numpy as np

from elephant.spike_train_dissimilarity import van_rossum_distance


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


def compute_van_rossum_distance(y_true, y_pred, time, tau=1.0):
    """Computes the Van Rossum distance between two spike trains.

    Args:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.
    time -- np.array, corresponding time points.
    tau -- float, time constant for the exponential kernel, default: 1.

    Returns:
    distance -- float, Van Rossum distance.
    """
    st_true = symprobe.utils.create_spike_train(
        symprobe.utils.extract_spike_times(y_true, time),
        time[-1],
    )
    st_pred = symprobe.utils.create_spike_train(
        symprobe.utils.extract_spike_times(y_pred, time),
        time[-1],
    )
    return van_rossum_distance(
        [st_true, st_pred],
        tau * symprobe.utils.quant.s,
    )[0, 1]


def compute_comparison(y_true, y_pred, metric, tau=1.0, time=np.array([])):
    """Computes the comparison between y_true and y_pred based on the metric

    Arguments:
    y_true -- np.array, ground truth values.
    y_pred -- np.array, estimated values.
    metric -- str, comparison metric {rmse, mae, mse}.
    tau -- float, time constant for the exponential kernel in the
    Van Rossum distance, default: 1.
    time -- np.array, corresponding time points, default: [].


    Return:
    comp_point -- float, comparison point.

    Raises:
    ValueError -- if the provided metric is not one of
    {'rmse', 'mae', 'mse', 'vrd'}.
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
            case "vrd":
                return compute_van_rossum_distance(y_true, y_pred, time=time)
            case _:
                raise ValueError("invalid metric {}\n".format(metric))
    except ValueError:
        raise
