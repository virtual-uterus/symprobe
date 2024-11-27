#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simulation-sweep.py

Performs multiple simulations with different parameters
Author: Mathias Roesler
Date: 11/24
"""

import sys
import argparse

import sweeps

if __name__ == "__main__":
    # Main argument parser setup
    parser = argparse.ArgumentParser(
        description="Runs multiple simulations with different parameters"
    )
    subparsers = parser.add_subparsers(
        title="subcommands", description="Available commands", dest="command"
    )

    # Subcommand: parameter
    param_parser = subparsers.add_parser(
        "parameter", help="Run a parameter sweep for the given parameter"
    )
    param_parser.add_argument("dim", type=int, help="dimension (2 or 3)")
    param_parser.add_argument("param", type=str, help="parameter to sweep")
    param_parser.add_argument(
        "start_val",
        type=float,
        help="start value of the parameter",
    )
    param_parser.add_argument(
        "end_val",
        type=float,
        help="end value of the parameter",
    )
    param_parser.add_argument(
        "step",
        type=float,
        help="step value for the parameter sweep",
    )
    param_parser.set_defaults(func=sweeps.parameter_sweep)

    # Subcommand: resolution
    res_parser = subparsers.add_parser(
        "resolution", help="Run a simulation on different resolution meshes"
    )
    res_parser.add_argument("dim", type=int, help="dimension (2 or 3)")
    res_parser.add_argument(
        "mesh_name",
        metavar="mesh-name",
        type=str,
        help="base name of the mesh",
    )
    res_parser.add_argument(
        "start_val",
        type=int,
        help="start value of the mesh index",
    )
    res_parser.add_argument(
        "end_val",
        type=int,
        help="end value of the mesh index",
    )
    res_parser.set_defaults(func=sweeps.resolution_sweep)

    # Subcommand: estrus
    estrus_parser = subparsers.add_parser(
        "estrus",
        help="Run an estrus sweep with the same mesh and base parameters",
    )
    estrus_parser.add_argument("dim", type=int, help="dimension (2 or 3)")
    estrus_parser.set_defaults(func=sweeps.estrus_sweep)

    # Parse the arguments and call the appropriate function
    args = parser.parse_args()

    try:
        if args.command == "resolution":
            args.func(args.dim, args.mesh_name, args.start_val, args.end_val)
        elif args.command == "parameter":
            args.func(
                args.dim,
                args.param,
                args.start_val,
                args.end_val,
                args.step,
            )
        elif args.command == "estrus":
            args.func(args.dim)
        else:
            parser.print_help()
    except Exception as e:
        sys.stderr.write("Error: {}\n".format(e))
