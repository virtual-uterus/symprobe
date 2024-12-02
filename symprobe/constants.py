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
RESISTIVITY = 1e-1  # Intracellular resistivity
CONFIG_ENV_VAR = "CHASTE_MODELLING_CONFIG_DIR"
PTS_DICT = {  # List of points to extract for the scaffolds
    "uterus_scaffold_1": [725, 995, 1251],
    "uterus_scaffold_2": [1401, 1927, 2439],
    "uterus_scaffold_3": [1591, 2189, 2765],
    "uterus_scaffold_4": [1595, 2192, 2768],
    "uterus_scaffold_5": [2387, 3824, 4148],
}
RES_DICT = {  # List of points to extract for the scaffolds
    "uterus_scaffold_1": 4492,
    "uterus_scaffold_2": 9984,
    "uterus_scaffold_3": 11232,
    "uterus_scaffold_4": 14976,
    "uterus_scaffold_5": 22464,
}
DIST_DICT = {  # Average distance between elements for the scaffolds
    "uterus_scaffold_1": 0.70,
    "uterus_scaffold_2": 0.46,
    "uterus_scaffold_3": 0.52,
    "uterus_scaffold_4": 0.48,
    "uterus_scaffold_5": 0.46,
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
}
ESTRUS = ["proestrus", "estrus", "metestrus", "diestrus"]
