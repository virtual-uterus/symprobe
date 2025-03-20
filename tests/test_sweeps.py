#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_sweeps.py

Unit tests for the sweep functions in sweeps.py.
Author: Mathias Roesler
Date: 03/25

This file contains test cases for the functions:
- modify_config
- get_config_dir,
- get_dim_config
- get_cell_config
- resolution_sweep
- parameter_sweep
- estrus_sweep

The tests cover various scenarios including valid inputs, invalid inputs,
and edge cases.
"""

import pytest
import os

from symprobe.sweeps import (
    modify_config,
    get_config_dir,
    get_dim_config,
    get_cell_config,
    resolution_sweep,
    parameter_sweep,
    estrus_sweep,
)

from symprobe.constants import CONFIG_ENV_VAR


@pytest.fixture
def config_files():
    return {
        "2d": "tests/2d_params.toml",
        "3d": "tests/3d_params.toml",
        "Roesler_estrus": "tests/Roesler_estrus.toml",
        "Means": "tests/Means.toml",
    }


@pytest.mark.parametrize(
    "mesh, param,value",
    [
        ("Means", "conductivities_2d", "0.1"),
        ("Means", "magnitude", "-3.0"),
        ("Roesler_estrus", "conductivities_3d", "0.2"),
        ("3d", "mesh_name", "test_mesh"),
        ("2d", "estrus", "proestrus"),
    ],
)
def test_modify_config(config_files, mesh, param, value):
    config_file = config_files[mesh]
    modify_config(config_file, param, value)

    with open(config_file, "r") as f:
        content = f.read()
    assert f"{param} =" in content


def test_get_config_dir():
    config_dir = get_config_dir()
    assert config_dir == os.getenv(CONFIG_ENV_VAR)


@pytest.mark.parametrize("dim", [2, 3])
def test_get_dim_config(config_files, dim):
    config_file = get_dim_config(dim)
    assert os.path.exists(config_file)


@pytest.mark.parametrize("dim", [2, 3])
def test_get_cell_config(config_files, dim):
    dim_config_file = get_dim_config(dim)
    cell_config_file = get_cell_config(dim_config_file)
    assert os.path.exists(cell_config_file)


@pytest.mark.parametrize(
    "dim,mesh_name,start_val,end_val", [(2, "mesh", 1, 2), (3, "mesh3d", 2, 3)]
)
def test_resolution_sweep(config_files, dim, mesh_name, start_val, end_val):
    resolution_sweep(dim, mesh_name, start_val, end_val)


@pytest.mark.parametrize(
    "dim,param,start_val,end_val,step",
    [
        (2, "conductivities_2d", 0.1, 0.2, 0.05),
        (3, "conductivities_3d", 0.2, 0.4, 0.1),
    ],
)
def test_parameter_sweep(config_files, dim, param, start_val, end_val, step):
    parameter_sweep(dim, param, start_val, end_val, step)


@pytest.mark.parametrize("dim", [2, 3])
def test_estrus_sweep(config_files, dim):
    estrus_sweep(dim)
