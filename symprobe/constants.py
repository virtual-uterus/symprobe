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
CONFIG_ENV_VAR = "CHASTE_MODELLING_CONFIG_DIR"
PTS_DICT = {  # List of points to extract for the scaffolds [Ova, Cen, Cvx]
    "uterus_scaffold_scaled_1": [195, 265, 329],
    "uterus_scaffold_scaled_2": [1088, 1493, 1971],
    "uterus_scaffold_scaled_3": [1595, 2192, 2908],
    "uterus_scaffold_scaled_4": [2387, 3824, 4358],
    "uterus_scaffold_scaled_5": [3183, 4379, 5813],
    "AWA026_proestrus_mesh": [38608, 41874, 42446],
    "AWA033_estrus_mesh": [31768, 9323, 31933],
    "AWB008_metestrus_mesh": [27499, 27256, 27826],
    "AWB003_diestrus_mesh": [44899, 44192, 43638],
}
RES_DICT = {  # Number of elements in the scaffolds
    "uterus_scaffold_scaled_1": 1258,
    "uterus_scaffold_scaled_2": 9984,
    "uterus_scaffold_scaled_3": 14976,
    "uterus_scaffold_scaled_4": 22464,
    "uterus_scaffold_scaled_5": 33696,
}
HORN_LENGTH_DICT = {  # Lenght of left horn in mm
    "uterus_scaffold_scaled_3": 20,
    "AWA026_proestrus_mesh": 21,
    "AWA033_estrus_mesh": 20,
    "AWB008_metestrus_mesh": 19,
    "AWB003_diestrus_mesh": 20,
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
