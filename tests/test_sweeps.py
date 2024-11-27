#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_sweeps.py

Unit tests for the sweep functions in sweeps.py.
Author: Mathias Roesler
Date: 11/24

This file contains test cases for the functions:
- resolution_sweep
- parameter_sweep
- modify_config
- estrus_sweep

The tests cover various scenarios including valid inputs, invalid inputs.
"""

import os
import pytest

from unittest.mock import patch, mock_open, call
from symprobe.sweeps import (
    resolution_sweep,
    parameter_sweep,
    modify_config,
    estrus_sweep,
)
from symprobe.constants import HOME, BASE, CONFIG_ENV_VAR

CONFIG_DIR = os.path.join(HOME, BASE, "uterine-modelling", "config")
PARAMS_FILE = os.path.join(CONFIG_DIR, "2d_params.toml")
ROESLER_FILE = os.path.join(CONFIG_DIR, "Roesler.toml")
PROESTRUS_FILE = os.path.join(CONFIG_DIR, "Roesler_proestrus.toml")
MEANS_FILE = os.path.join(CONFIG_DIR, "Means.toml")


@pytest.fixture
def mock_env():
    """Set up the environment variable for the configuration directory."""
    with patch.dict(os.environ, {CONFIG_ENV_VAR: CONFIG_DIR}):
        yield


def test_modify_config_success(mock_env):
    # Initial mock file content
    mock_file_content = ["mesh_name = 'old_mesh'\n", "another_param = value\n"]

    # Mock the `open` call
    mock_open_obj = mock_open(read_data="".join(mock_file_content))
    with patch("builtins.open", mock_open_obj):
        # Run the function under test
        modify_config(PARAMS_FILE, "mesh_name", "new_mesh")

    # Ensure the file was opened twice: once for reading and once for writing
    assert (
        mock_open_obj.call_count == 2
    ), f"Expected 2 file openings, got {mock_open_obj.call_count}"

    # Capture the lines passed to the `writelines` method during the write operation
    handle = mock_open_obj()
    handle.writelines.assert_called_once()  # Ensure `writelines` was called
    written_lines = handle.writelines.call_args[0][
        0
    ]  # Extract the first argument to `writelines`

    # Expected output after modification
    expected_lines = ['mesh_name = "new_mesh"\n', "another_param = value\n"]

    # Compare written lines with the expected content
    assert (
        written_lines == expected_lines
    ), f"Output mismatch: expected {expected_lines}, got {written_lines}"


def test_modify_config_param_not_found(mock_env):
    mock_file_content = ["another_param = value\n"]

    with patch(
        "builtins.open",
        mock_open(
            read_data="".join(
                mock_file_content,
            )
        ),
    ):
        with pytest.raises(
            ValueError,
            match="the parameter 'mesh_name' was not found",
        ):
            modify_config(PARAMS_FILE, "mesh_name", "new_mesh")


def test_modify_config_file_not_found(mock_env):
    with pytest.raises(FileNotFoundError):
        modify_config("nonexistent_file.toml", "mesh_name", "new_mesh")


def test_resolution_sweep_success(mock_env):
    mock_file_content = [
        "mesh_name = 'uterus_scaffold_0'\n",
        "conductivities_2d = [0, 0]",
    ]
    mock_open_obj = mock_open(read_data="".join(mock_file_content))

    with (
        patch(
            "builtins.open",
            mock_open_obj,
        ),
        patch("subprocess.run") as mock_run,
    ):
        resolution_sweep(2, "uterus_scaffold", 1, 3)

    # Assert subprocess was called three times (once per mesh value)
    assert mock_run.call_count == 3
    mock_run.assert_called_with(["uterine-simulation", "2"])

    # Ensure the file was written to three times with updated mesh_name
    expected_calls = [
        call(PARAMS_FILE, "w"),
        call(PARAMS_FILE, "w"),
        call(PARAMS_FILE, "w"),
    ]
    mock_open_obj.assert_has_calls(expected_calls, any_order=True)


def test_resolution_sweep_missing_env():
    with patch.dict(os.environ, {}, clear=True), pytest.raises(OSError):
        resolution_sweep(2, "test_mesh", 1, 3)


def test_resolution_sweep_invalid_range(mock_env):
    with pytest.raises(
        ValueError, match="the start value is greater than the end value"
    ):
        resolution_sweep(2, "test_mesh", 3, 1)


def test_parameter_sweep_no_estrus_success(mock_env):
    mock_file_content = [
        "param = old_value\n",
        'cell_type = "Means"\n',
    ]
    mock_open_obj = mock_open(read_data="".join(mock_file_content))

    with (
        patch(
            "builtins.open",
            mock_open_obj,
        ),
        patch("subprocess.run") as mock_run,
    ):
        parameter_sweep(2, "param", 1.0, 3.0, 1.0)

    # Assert subprocess was called three times (once per parameter value)
    assert mock_run.call_count == 3
    mock_run.assert_called_with(["uterine-simulation", "2"])

    # Ensure the file was written to three times with updated param values
    expected_calls = [
        call(MEANS_FILE, "w"),
        call(MEANS_FILE, "w"),
        call(MEANS_FILE, "w"),
    ]
    mock_open_obj.assert_has_calls(expected_calls, any_order=True)


def test_parameter_sweep_estrus_success(mock_env):
    mock_file_content = [
        "param = old_value\n",
        'cell_type = "Roesler"\n',
        'estrus = "proestrus"\n',
    ]
    mock_open_obj = mock_open(read_data="".join(mock_file_content))

    with (
        patch(
            "builtins.open",
            mock_open_obj,
        ),
        patch("subprocess.run") as mock_run,
    ):
        parameter_sweep(2, "param", 1.0, 3.0, 1.0)

    # Assert subprocess was called three times (once per parameter value)
    assert mock_run.call_count == 3
    mock_run.assert_called_with(["uterine-simulation", "2"])

    # Ensure the file was written to three times with updated param values
    expected_calls = [
        call(PROESTRUS_FILE, "w"),
        call(PROESTRUS_FILE, "w"),
        call(PROESTRUS_FILE, "w"),
    ]
    mock_open_obj.assert_has_calls(expected_calls, any_order=True)


def test_parameter_sweep_estrus_presence(mock_env):
    mock_file_content = ["param = old_value\n", 'cell_type = "Roesler"\n']
    mock_open_obj = mock_open(read_data="".join(mock_file_content))

    with (
        patch(
            "builtins.open",
            mock_open_obj,
        ),
        patch("subprocess.run"),
        pytest.raises(
            ValueError,
            match="estrus not found in config file",
        ),
    ):
        parameter_sweep(2, "param", 1.0, 3.0, 1.0)


def test_parameter_sweep_missing_env():
    with patch.dict(os.environ, {}, clear=True), pytest.raises(OSError):
        parameter_sweep(2, "param", 1.0, 3.0, 1.0)


def test_parameter_sweep_invalid_range(mock_env):
    with pytest.raises(
        ValueError, match="the start value is greater than the end value"
    ):
        parameter_sweep(2, "param", 3.0, 1.0, 1.0)


def test_estrus_sweep_success(mock_env):
    mock_file_content = [
        "mesh_name = 'uterus_scaffold_0'\n",
        "conductivities_2d = [0, 0]\n",
        "estrus = proestrus\n",
    ]
    mock_open_obj = mock_open(read_data="".join(mock_file_content))

    with (
        patch(
            "builtins.open",
            mock_open_obj,
        ),
        patch("subprocess.run") as mock_run,
    ):
        estrus_sweep(2)

    # Assert subprocess was called three times (once per mesh value)
    assert mock_run.call_count == 4
    mock_run.assert_called_with(["uterine-simulation", "2"])

    # Ensure the file was written to three times with updated mesh_name
    expected_calls = [
        call(PARAMS_FILE, "w"),
        call(PARAMS_FILE, "w"),
        call(PARAMS_FILE, "w"),
        call(PARAMS_FILE, "w"),
    ]
    mock_open_obj.assert_has_calls(expected_calls, any_order=True)


def test_estrus_sweep_invalid_parameter(mock_env):
    mock_file_content = [
        "mesh_name = 'uterus_scaffold_0'\n",
        "conductivities_2d = [0, 0]",
    ]
    mock_open_obj = mock_open(read_data="".join(mock_file_content))

    with (
        patch(
            "builtins.open",
            mock_open_obj,
        ),
        patch("subprocess.run"),
        pytest.raises(
            ValueError,
        ),
    ):
        estrus_sweep(2)
