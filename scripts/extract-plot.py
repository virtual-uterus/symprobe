#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract-plot.py

Script that plots extracted data
Author: Mathias Roesler
Date: 11/24
"""

import os
import sys
import argparse

from symprobe import extract_script_fct, constants


def add_shared_arguments(parser):
    parser.add_argument(
        "dir_path",
        type=str,
        metavar="dir-path",
        help="path from BASE to the data",
    )
    parser.add_argument(
        "--estrus",
        type=str,
        default="all",
        choices={"proestrus", "estrus", "metestrus", "diestrus", "all"},
        help="estrus stage",
    )
    parser.add_argument(
        "--sim-name",
        type=str,
        default="simulation",
        help="name of the simulation prefix",
    )
    parser.add_argument(
        "--range",
        "-r",
        nargs="+",
        help="range of mesh numbers for comparison",
    )
    parser.add_argument(
        "--delimiter",
        type=str,
        default=",",
        help="delimiter in csv file",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot tools for extracted data")
    subparsers = parser.add_subparsers(
        title="subcommands", description="Available commands", dest="command"
    )

    # Subcommand: resolution
    resolution_parser = subparsers.add_parser(
        "resolution",
        help="Plots the comparison metric for different resolution meshes",
    )

    add_shared_arguments(resolution_parser)

    resolution_parser.add_argument(
        "estrus_dir",
        type=str,
        metavar="estrus-dir",
        help="name of the estrus specific directory",
    )
    resolution_parser.add_argument(
        "metric",
        type=str,
        choices={"rmse", "mae", "mse", "vrd"},
        help="metric used for comparison",
    )
    resolution_parser.set_defaults(func=extract_script_fct.resolution_fct)

    # Subcommand: cell
    cell_parser = subparsers.add_parser(
        "cell", help="Plots the extracted data of cells"
    )

    add_shared_arguments(cell_parser)

    cell_parser.set_defaults(func=extract_script_fct.cell_fct)

    # Subcommand: parameter
    parameter_parser = subparsers.add_parser(
        "parameter",
        help="Plots the comparison metric for different parameter values",
    )

    add_shared_arguments(parameter_parser)

    parameter_parser.add_argument(
        "parameter",
        type=str,
        help="parameter to plot against",
    )
    parameter_parser.add_argument(
        "metric",
        type=str,
        choices={"rmse", "mae", "mse", "vrd"},
        help="metric used for comparison",
    )

    parameter_parser.add_argument(
        "estrus_dir",
        type=str,
        metavar="estrus-dir",
        help="name of the estrus specific directory",
    )

    parameter_parser.set_defaults(func=extract_script_fct.parameter_fct)

    # Parse input arguments
    args = parser.parse_args()

    # Create path to main directory
    dir_path = os.path.join(
        constants.HOME,
        constants.BASE,
        args.dir_path,
    )

    try:
        if args.command == "resolution":
            args.func(
                dir_path,
                args.estrus_dir,
                args.metric,
                args.range,
                args.sim_name,
                args.estrus,
                args.delimiter,
            )
        elif args.command == "cell":
            args.func(
                dir_path,
                args.range,
                args.sim_name,
                args.estrus,
                args.delimiter,
            )
        elif args.command == "parameter":
            args.func(
                dir_path,
                args.parameter,
                args.estrus_dir,
                args.metric,
                args.range,
                args.sim_name,
                args.estrus,
                args.delimiter,
            )
        else:
            parser.print_help()
    except Exception as e:
        sys.stderr.write("Error: {}\n".format(e))
        exit()
