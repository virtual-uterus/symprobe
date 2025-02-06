import os
import sys
import numpy as np

from symprobe import utils, plots, constants, metrics


def resolution_fct(
    dir_path,
    estrus_dir,
    metric,
    rng,
    sim_name,
    estrus,
    delimiter,
):
    sim_numbers = utils.get_range(rng)

    if estrus == "all":
        estrus = constants.ESTRUS

    else:
        estrus = [estrus]

    comp_dict = {}  # Create a dictionnary for the data of each stage

    for stage in estrus:
        estrus_path = os.path.join(dir_path, stage + "_" + estrus_dir)

        for i, sim_nb in enumerate(sim_numbers):
            # Iterate over each simulation
            current_sim_name = f"{sim_name}_{sim_nb:03}"

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
                V, t = utils.load_data(data_path, log_path, delimiter)
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
                metric,
                time=t,
            )

        comp_data[len(sim_numbers) - 1] = metrics.compute_comparison(
            data[:, len(sim_numbers) - 1],
            data[:, len(sim_numbers) - 1],
            metric,
            time=t,
        )
        comp_dict[stage] = comp_data  # Add data to the estrus dict

    plots.plot_resolution_convergence(comp_dict, nb_mesh_eles, metric)


def cell_fct(dir_path, rng, sim_name, estrus, delimiter):
    """ """
    sim_numbers = utils.get_range(rng)

    if estrus == "all" and len(sim_numbers) != 4:
        raise ValueError("range must be 4 if estrus is set to all")

    if estrus == "all":
        estrus = constants.ESTRUS
        nb_sims = np.arange(1, 5)

    else:
        estrus = estrus
        nb_sims = sim_numbers

    for i in nb_sims:
        current_sim_name = f"{sim_name}_{(i):03}"

        data_path = os.path.join(
            dir_path,
            "extract",
            "{}.csv".format(current_sim_name),
        )
        log_path = os.path.join(
            dir_path,
            "log",
            "{}.log".format(current_sim_name),
        )

        try:
            V, t = utils.load_data(data_path, log_path, delimiter)

            if type(estrus) is type(list()):
                plots.plot_cell_data(V, t, estrus=estrus[i])
            else:
                plots.plot_cell_data(V, t, estrus=estrus)

        except Exception as e:
            raise Exception from e


def parameter_fct(
    dir_path,
    parameter,
    estrus_dir,
    metric,
    rng,
    sim_name,
    estrus,
    delimiter,
):
    sim_numbers = utils.get_range(rng)

    if estrus == "all":
        estrus = constants.ESTRUS

    else:
        estrus = [estrus]

    comp_dict = {}  # Create a dictionnary for the data of each stage

    for stage in estrus:
        estrus_path = os.path.join(dir_path, stage + "_" + estrus_dir)

        for i, sim_nb in enumerate(sim_numbers):
            # Iterate over each simulation
            current_sim_name = f"{sim_name}_{sim_nb:03}"

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
                V, t = utils.load_data(data_path, log_path, delimiter)
            except Exception as e:
                raise Exception from e

            if i == 0:
                # Allocate space for data on the first loop
                data = np.zeros((len(V), len(sim_numbers)))
                param_values = np.zeros(len(sim_numbers))

            data[:, i] = V[:, 0]
            param_values[i] = utils.get_param_value(log_path, parameter)

        comp_data = np.zeros(len(sim_numbers))

        for i in range(1, len(sim_numbers)):
            comp_data[i] = metrics.compute_comparison(
                data[:, i],
                data[:, 0],
                metric,
                time=t,
            )

        comp_data[0] = metrics.compute_comparison(
            data[:, 0],
            data[:, 0],
            metric,
            time=t,
        )
        comp_dict[stage] = comp_data  # Add data to the estrus dict

    plots.plot_parameter_comparison(comp_dict, param_values, metric, parameter)
