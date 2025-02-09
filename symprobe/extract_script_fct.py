import os
import numpy as np

from symprobe import utils, plots, constants, metrics


def _fct_setup(rng, estrus):
    """Setups simulation numbers and estrus cycle for all functions

    Arguments:
    rng -- int or list[int], range of simulation numbers.
    estrus -- str, estrus cycle.

    Return:
    nb_sims -- list[int], list of simulation numbers.
    estrus -- list[str], list of estrus phases.

    Raises:
    ValueError -- if the number of simulations does not match with estrus.

    """
    sim_numbers = utils.get_range(rng)

    if type(sim_numbers) is type(int()):
        if estrus == "all":
            raise ValueError("estrus cannot be all with a single simulation")

        sim_numbers = [sim_numbers]

    if estrus == "all":
        estrus = constants.ESTRUS
        nb_sims = sim_numbers

    else:
        estrus = [estrus]
        nb_sims = sim_numbers

    return nb_sims, estrus


def _data_extract(sim_name, sim_nb, path, delimiter):
    """Recuperates the extracted data for a simulation

    Arguments:
    sim_name -- str, simulation name.
    sim_nb -- int, simulation number.
    path -- str, path to the data directory.
    delimiter -- str, csv file delimiter.

    Return:
    V -- np.array[float], amplitude values of the extracted cells.
    t -- np.array[float], timesteps of the extracted cells.
    cell_ids -- np.array[int], cell ids (assume only 3 cells extracted).
    log_path -- str, path to the log file.

    Raises:
    Exception -- if an error occurs during the recuperation process.

    """
    current_sim_name = f"{sim_name}_{sim_nb:03}"

    data_path = os.path.join(
        path,
        "extract",
        "{}.csv".format(current_sim_name),
    )
    log_path = os.path.join(
        path,
        "log",
        "{}.log".format(current_sim_name),
    )

    try:
        V, t, cell_ids = utils.load_data(data_path, log_path, delimiter)
    except Exception as e:
        raise e

    return V, t, cell_ids, log_path


def _reorder_V(V, cell_ids, ordered_ids):
    """Reorders V to follow ovaries, centre, cervical end extract

    Arguments:
    V -- np.array[float], amplitude values of the extracted cells.
    cell_ids -- np.array[int], cell ids (assume only 3 cells extracted).
    ordered_ids -- np.array[int], correctly ordered ids.

    Return:
    ordered_V -- np.array[float], reordered array.

    Raises:
    ValueError -- if the ordered and unordered ids are not the same length.

    """
    if len(cell_ids) != len(ordered_ids):
        raise ValueError("cell ids and ordered ids should have same length.")

    if (cell_ids == ordered_ids).all():
        # Already in order
        return V

    ordered_V = np.zeros(V.shape)

    for i, ordered_id in enumerate(ordered_ids):
        for j, id in enumerate(cell_ids):
            if id == ordered_id:
                ordered_V[:, i] = V[:, j]

    return ordered_V


def resolution_fct(
    dir_path,
    estrus_dir,
    metric,
    rng,
    sim_name,
    estrus,
    delimiter,
):
    nb_sims, estrus = _fct_setup(rng, estrus)

    comp_dict = {}  # Create a dictionnary for the data of each stage

    for stage in estrus:
        estrus_path = os.path.join(dir_path, stage + "_" + estrus_dir)

        for i, sim_nb in enumerate(nb_sims):
            # Iterate over each simulation
            try:
                V, t, _, log_path = _data_extract(
                    sim_name,
                    sim_nb,
                    estrus_path,
                    delimiter,
                )
            except Exception as e:
                raise e

            if i == 0:
                # Allocate space for data on the first loop
                data = np.zeros((len(V), len(nb_sims)))
                nb_mesh_eles = np.zeros(len(nb_sims))

            data[:, i] = V[:, 0]
            nb_mesh_eles[i] = constants.RES_DICT[utils.get_mesh_name(log_path)]

        comp_data = np.zeros(len(nb_sims))

        for i in range(len(nb_sims) - 1):
            comp_data[i] = metrics.compute_comparison(
                data[:, i],
                data[:, i + 1],
                metric,
                time=t,
            )

        comp_data[len(nb_sims) - 1] = metrics.compute_comparison(
            data[:, len(nb_sims) - 1],
            data[:, len(nb_sims) - 1],
            metric,
            time=t,
        )
        comp_dict[stage] = comp_data  # Add data to the estrus dict

    plots.plot_resolution_convergence(comp_dict, nb_mesh_eles, metric)


def cell_fct(dir_path, rng, sim_name, estrus, delimiter):
    """ """
    nb_sims, estrus = _fct_setup(rng, estrus)

    for i in nb_sims:
        try:
            V, t, cell_ids, log_path = _data_extract(
                sim_name,
                i,
                dir_path,
                delimiter,
            )

            ordered_ids = constants.PTS_DICT[utils.get_mesh_name(log_path)]

            V = _reorder_V(V, cell_ids, ordered_ids)

            if type(estrus) is type(list()):
                plots.plot_cell_data(V, t, estrus=estrus[i - 1])
            else:
                plots.plot_cell_data(V, t, estrus=estrus)

        except Exception as e:
            raise e


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
    nb_sims, estrus = _fct_setup(rng, estrus)

    comp_dict = {}  # Create a dictionnary for the data of each stage
    spike_dict = {}  # Create a dictionnary for spike propagation of each stage

    for stage in estrus:
        estrus_path = os.path.join(dir_path, stage + "_" + estrus_dir)

        for i, sim_nb in enumerate(nb_sims):
            # Iterate over each simulation
            try:
                V, t, cell_ids, log_path = _data_extract(
                    sim_name,
                    sim_nb,
                    estrus_path,
                    delimiter,
                )
                ordered_ids = constants.PTS_DICT[utils.get_mesh_name(log_path)]

                V = _reorder_V(V, cell_ids, ordered_ids)
            except Exception as e:
                raise e

            if i == 0:
                # Allocate space for data on the first loop
                data = np.zeros((len(V), len(nb_sims)))
                param_values = np.zeros(len(nb_sims))
                nb_spikes = np.zeros(len(nb_sims))

            data[:, i] = V[:, 0]
            param_values[i] = utils.get_param_value(log_path, parameter)
            nb_spikes[i] = len(utils.extract_spike_times(V[:, 2], t))

        comp_data = np.zeros(len(nb_sims))

        for i in range(1, len(nb_sims)):
            comp_data[i] = metrics.compute_comparison(
                data[:, i],
                data[:, 0],
                metric,
                time=t,
            )

        comp_data[0] = 0.0  # Comparing inital state with initial state
        comp_dict[stage] = comp_data  # Add data to the estrus dict
        spike_dict[stage] = nb_spikes  # Add number of spike to estrus dict

    plots.plot_parameter_comparison(comp_dict, param_values, metric, parameter)
    plots.plot_spike_propagation(spike_dict, param_values, parameter)


def comparison_fct(
    dir_path,
    metric,
    realistic_dir,
    idealised_dir,
    sub_dir,
    rng,
    sim_name,
    estrus,
    delimiter,
):
    """ """
    nb_sims, estrus = _fct_setup(rng, estrus)

    for i, stage in enumerate(estrus):
        idealised_path = os.path.join(dir_path, idealised_dir, sub_dir)
        realistic_path = os.path.join(dir_path, realistic_dir, sub_dir)
        comp_data = []

        try:
            # Get idealised mesh data
            idealised_V, t, ideal_ids, idealised_log_path = _data_extract(
                sim_name,
                i + 1,
                idealised_path,
                delimiter,
            )
            ideal_ordered_ids = constants.PTS_DICT[
                utils.get_mesh_name(idealised_log_path)
            ]

            idealised_V = _reorder_V(  # Reorder to be ova, cen, cvx
                idealised_V,
                ideal_ids,
                ideal_ordered_ids,
            )

            # Get realistic mesh data
            realistic_V, t, real_ids, realistic_log_path = _data_extract(
                sim_name,
                i + 1,
                realistic_path,
                delimiter,
            )
            real_ordered_ids = constants.PTS_DICT[
                utils.get_mesh_name(realistic_log_path)
            ]

            realistic_V = _reorder_V(  # Reorder to be ova, cen, cvx
                realistic_V,
                real_ids,
                real_ordered_ids,
            )

        except Exception as e:
            raise e

        for j in range(idealised_V.shape[1]):
            comp_data.append(
                metrics.compute_comparison(
                    idealised_V[:, j],
                    realistic_V[:, j],
                    metric,
                    time=t,
                )
            )

        mean_data = np.mean(comp_data)
        std_data = np.std(comp_data)
        print(f"{stage.capitalize()}: {mean_data:.3f} ± {std_data:.3f}")
