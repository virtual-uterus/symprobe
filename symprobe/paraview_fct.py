#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paraview_fct.py

Functions based off Paraview's API
Author: Mathias Roesler
Date: 11/24
"""

import paraview.simple as ps


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
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise e

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
