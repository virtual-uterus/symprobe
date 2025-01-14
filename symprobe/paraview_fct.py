#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paraview_fct.py

Functions based off Paraview's API
Author: Mathias Roesler
Date: 11/24
"""

import os

import numpy as np
import paraview.simple as ps
import paraview.servermanager as psm


def paraview_extract(mesh_path, save_path, pts_list):
    """Extracts the data from the desired points in the mesh and
    saves in a csv file

    Arguments:
    mesh_path -- str, path to the mesh vtu file.
    save_path -- str, path to the export save file.
    pts_list -- list(int), list of points to extract data from in the mesh.

    Return:
    FileNotFoundError -- if the file is not found.
    RuntimeError -- if the an error occurs while opening the file.

    """
    # Create a new 'XML Unstructured Grid Reader'
    try:
        mesh = ps.XMLUnstructuredGridReader(
            registrationName="mesh.vtu",
            FileName=[mesh_path],
        )
    except FileNotFoundError:
        raise
    except Exception:
        raise

    mesh.PointArrayStatus = ["V"]

    # Properties modified on mesh
    mesh.TimeArray = "None"

    # Get active view
    view = ps.GetActiveViewOrCreate("RenderView")

    # Update the view to ensure updated data information
    view.Update()

    # create a query selection
    ps.QuerySelect(
        QueryString="(in1d(id, {}))".format(pts_list),
        FieldType="POINT",
        InsideOut=0,
    )

    # Update the view to ensure updated data information
    view.Update()

    # Create a new 'Extract Selection'
    selected_pts = ps.ExtractSelection(
        registrationName="Selected_pts",
        Input=mesh,
    )

    # Save data
    ps.SaveData(
        save_path,
        proxy=selected_pts,
        WriteTimeSteps=1,
        PointDataArrays=["V"],
        AddMetaData=0,
        AddTime=1,
    )


def fetch_quality_data(quality, mesh_quality, view):
    """Fetches the quality data based on the selected quality

    Arguments:
    quality -- str, quality metric to fecth.
    mesh_quality -- psm.MeshQuality, Paraview extracted mesh quality object.
    view -- psm.RenderView, Paraview rendered view of the mesh.

    Return:
    quality_data -- np.array, quality value for the cells in the mesh.

    Raises:
    ValueError -- if the quality array is not found.

    """
    # Properties modified on mesh_quality
    mesh_quality.TetQualityMeasure = quality

    # Update the view to ensure updated data information
    view.Update()

    fetched_data = psm.Fetch(mesh_quality)
    cell_data = fetched_data.GetCellData()
    quality_array = cell_data.GetArray("Quality")

    if quality_array:
        quality_data = [
            quality_array.GetValue(i)
            for i in range(
                quality_array.GetNumberOfTuples(),
            )
        ]

    else:
        raise ValueError("quality array not found")

    return np.array(quality_data)


def paraview_quality(mesh_path, metric):
    """Inspects the quality of the mesh for a given metric

    Arguments:
    mesh_path -- str, path to the mesh vtu file.
    metric -- str, quality metric used {Aspect Ratio, Mean Ratio, Jacobian}.

    Return:
    quality_data -- np.array, quality data for the given metric.

    Raises:
    ValueError -- if the extension is not vtk or vtu.
    FileNotFoundError -- if the file is not found.
    RuntimeError -- if the an error occurs while opening the file.
    ValueError -- if the quality array is not found.

    """
    extension = os.path.splitext(mesh_path)[1]

    try:
        if extension == ".vtk":
            mesh = ps.LegacyVTKReader(
                registrationName="mesh.vtk",
                FileNames=[mesh_path],
            )

        elif extension == ".vtu":
            # Create a new 'XML Unstructured Grid Reader'
            mesh = ps.XMLUnstructuredGridReader(
                registrationName="mesh.vtu",
                FileName=[mesh_path],
            )

        else:
            raise ValueError(
                "unrecognised extension {}\n".format(extension),
            )
    except FileNotFoundError:
        raise
    except ValueError:
        raise
    except Exception:
        raise

    # Get active view
    view = ps.GetActiveViewOrCreate("RenderView")

    # Update the view to ensure updated data information
    view.Update()

    # Create a new 'Mesh Quality'
    mesh_quality = ps.MeshQuality(
        registrationName="quality",
        Input=mesh,
    )
    # Update the view to ensure updated data information
    view.Update()

    try:
        return fetch_quality_data(metric, mesh_quality, view)
    except ValueError:
        raise
