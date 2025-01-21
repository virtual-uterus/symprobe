#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convergene-plot.py

Script that compares the outputs at different mesh resolutions
Author: Mathias Roesler
Date: 11/24
"""

import os
import sys
import argparse

import numpy as np

from symprobe import utils, plots, constants, metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plots the comparison for different resolution meshes"
    )
    parser.add_argument(
        "dir_path",
        type=str,
        metavar="dir-path",
        help="path from BASE to the Chaste save directory",
    )
    parser.add_argument(
        "estrus_dir",
        type=str,
        metavar="estrus-dir",
        help="name of the estrus specific directory",
    )
    parser.add_argument(
        "metric",
        type=str,
        choices={"rmse", "mae", "mse", "vrd"},
        help="metric used for comparison",
    )
    parser.add_argument(
        "sim_numbers",
        nargs="+",
        metavar="sim-numbers",
        help="numbers of the simulations to extract data from",
    )
    parser.add_argument(
        "--sim-name",
        type=str,
        default="simulation",
        help="name of the simulation prefix",
    )
    parser.add_argument(
        "--estrus",
        type=str,
        default="all",
        choices={"proestrus", "estrus", "metestrus", "diestrus", "all"},
        help="estrus stage",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        help="delimiter for the reading the data",
        default=",",
    )

    # Parse input arguments
    args = parser.parse_args()

    sim_numbers = utils.get_range(args.sim_numbers)

    # Create path to main directory
    dir_path = os.path.join(
        constants.HOME,
        constants.BASE,
        args.dir_path,
    )

    if args.estrus == "all":
        estrus = constants.ESTRUS

    else:
        estrus = [args.estrus]

    comp_dict = {}  # Create a dictionnary for the data of each stage

    for stage in estrus:
        estrus_path = os.path.join(dir_path, stage + "_" + args.estrus_dir)

        for i, sim_nb in enumerate(sim_numbers):
            # Iterate over each simulation
            current_sim_name = f"{args.sim_name}_{sim_nb:03}"

            data_path = os.path.join(
                estrus_path,
                "extract",
                "{}.csv".format(current_sim_name),
            )
            log_path = os.path.join(
                estrus_path,
                "log",
                "{}.log".format(current_sim_name),
            )

            try:
                V, t = utils.load_data(data_path, log_path, args.delimiter)
            except Exception as e:
                sys.stderr.write("Error: {}\n".format(e))
                exit()

            if i == 0:
                # Allocate space for data on the first loop
                data = np.zeros((len(V), len(sim_numbers)))
                nb_mesh_eles = np.zeros(len(sim_numbers))

            data[:, i] = V[:, 0]
            nb_mesh_eles[i] = constants.RES_DICT[utils.get_mesh_name(log_path)]

        comp_data = np.zeros(len(sim_numbers))

        for i in range(len(sim_numbers) - 1):
            comp_data[i] = metrics.compute_comparison(
                data[:, i],
                data[:, i + 1],
                args.metric,
                time=t,
            )

        comp_data[len(sim_numbers) - 1] = metrics.compute_comparison(
            data[:, len(sim_numbers) - 1],
            data[:, len(sim_numbers) - 1],
            args.metric,
            time=t,
        )
        comp_dict[stage] = comp_data  # Add data to the estrus dict

    plots.plot_resolution_convergence(comp_dict, nb_mesh_eles, args.metric)
