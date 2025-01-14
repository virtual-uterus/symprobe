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
RESISTIVITY = 1e-2  # Intracellular resistivity
CONFIG_ENV_VAR = "CHASTE_MODELLING_CONFIG_DIR"
PTS_DICT = {  # List of points to extract for the scaffolds
    "uterus_scaffold_1": [195, 265, 345],
    "uterus_scaffold_2": [1088, 1493, 1973],
    "uterus_scaffold_3": [1595, 2192, 2912],
    "uterus_scaffold_4": [2387, 3824, 4364],
    "uterus_scaffold_5": [3183, 4379, 5819],
}
RES_DICT = {  # List of points to extract for the scaffolds
    "uterus_scaffold_1": 1258,
    "uterus_scaffold_2": 9984,
    "uterus_scaffold_3": 14976,
    "uterus_scaffold_4": 22464,
    "uterus_scaffold_5": 33696,
}
DIST_DICT = {  # Average distance between elements for the scaffolds
    "uterus_scaffold_1": 1.27,
    "uterus_scaffold_2": 0.65,
    "uterus_scaffold_3": 0.48,
    "uterus_scaffold_4": 0.46,
    "uterus_scaffold_5": 0.44,
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
    "mr": "Mean Ratio",
}
ESTRUS = ["proestrus", "estrus", "metestrus", "diestrus"]
# Plot constants
LEFT = 0.22
BOTTOM = 0.17
RIGHT = 0.80
