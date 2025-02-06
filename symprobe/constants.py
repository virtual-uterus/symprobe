#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants.py

Constants for the symprobe package
Author: Mathias Roesler
Date: 11/24
"""

import os

# Define global constants
HOME = os.path.expanduser("~")
BASE = "Documents/phd"
RESISTANCE = 2000  # Specific resistance
CONFIG_ENV_VAR = "CHASTE_MODELLING_CONFIG_DIR"
PTS_DICT = {  # List of points to extract for the scaffolds [Ova, Cen, Cvx]
    "uterus_scaffold_1": [195, 265, 329],
    "uterus_scaffold_2": [1088, 1493, 1971],
    "uterus_scaffold_3": [1595, 2192, 2908],
    "uterus_scaffold_4": [2387, 3824, 4358],
    "uterus_scaffold_5": [3183, 4379, 5813],
    "uterus_scaffold_norm_1": [195, 265, 329],
    "uterus_scaffold_norm_2": [1088, 1493, 1971],
    "uterus_scaffold_norm_3": [1595, 2192, 2908],
    "uterus_scaffold_norm_4": [2387, 3824, 4358],
    "uterus_scaffold_norm_5": [3183, 4379, 5813],
    "AWA026_proestrus_mesh": [38608, 41874, 42446],
    "AWA033_estrus_mesh": [31768, 9323, 31933],
    "AWB008_metestrus_mesh": [27499, 27256, 27826],
    "AWB003_diestrus_mesh": [44899, 44192, 43638],
}
RES_DICT = {  # Number of elements in the scaffolds
    "uterus_scaffold_1": 1258,
    "uterus_scaffold_2": 9984,
    "uterus_scaffold_3": 14976,
    "uterus_scaffold_4": 22464,
    "uterus_scaffold_5": 33696,
    "uterus_scaffold_norm_1": 1258,
    "uterus_scaffold_norm_2": 9984,
    "uterus_scaffold_norm_3": 14976,
    "uterus_scaffold_norm_4": 22464,
    "uterus_scaffold_norm_5": 33696,
}
DIST_DICT = {  # Average distance between elements for the scaffolds
    "uterus_scaffold_1": 1.27,
    "uterus_scaffold_2": 0.65,
    "uterus_scaffold_3": 0.48,
    "uterus_scaffold_4": 0.46,
    "uterus_scaffold_5": 0.44,
    "uterus_scaffold_norm_1": 0.03,
    "uterus_scaffold_norm_2": 0.01,
    "uterus_scaffold_norm_3": 0.01,
    "uterus_scaffold_norm_4": 0.01,
    "uterus_scaffold_norm_5": 0.01,
}
CONVERSION_IDX = [  # List of node indices for each tetrahedra
    [0, 1, 2, 4],  # Tetrahedron 1
    [0, 2, 3, 4],  # Tetrahedron 2
    [1, 2, 4, 5],  # Tetrahedron 3
    [2, 3, 4, 7],  # Tetrahedron 4
    [2, 4, 5, 6],  # Tetrahedron 5
    [2, 4, 6, 7],  # Tetrahedron 6
]
QUALITY_METRIC_MAP = {  # Mapping for quality metrics
    "ar": "Aspect Ratio",
    "ja": "Jacobian",
    "sj": "Scaled Jacobian",
    "mr": "Mean Ratio",
}
ESTRUS = ["proestrus", "estrus", "metestrus", "diestrus"]

# Plot constants
LEFT = 0.22
BOTTOM = 0.17
RIGHT = 0.80
COLOURS = {
    "proestrus": "r",
    "estrus": "b",
    "metestrus": "g",
    "diestrus": "k",
}
PARAM = {
    "gkv43": r"g$_{Kv4.3}$",
    "gcal": r"g$_{CaL}$",
    "gna": r"g$_{Na}$",
    "stim_current": r"I$_{stim}$",
}
UNITS = {
    "gkv43": r"nS pF$^{-1}$",
    "gcal": r"nS pF$^{-1}$",
    "gkca": r"nS pF$^{-1}$",
    "gna": r"nS pF$^{-1}$",
    "stim_current": r"pA pF$^{-1}$",
}
