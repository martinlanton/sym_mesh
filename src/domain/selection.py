import logging

from maya.api import OpenMaya as om2

log = logging.getLogger(__name__)


def get_points_positions(obj_dag_path=None):
    """
    Get the position of every point of the selected mesh.

    :param obj_dag_path: dag path object of the geometry for which we want the points position
    :type obj_dag_path: maya.api.OpenMaya.MDagPath

    :return: dag dir_path of the object, position of the points
    :rtype: maya.api.OpenMaya.MDagPath, maya.api.OpenMaya.MPointArray
    """
    if not obj_dag_path:
        # Get current selection
        selection_list = om2.MGlobal.getActiveSelectionList()

        # Get the dag dir_path of the first item in the selection list
        obj_dag_path = selection_list.getDagPath(0)

    # Query vertex position
    # create a Mesh functionSet from our dag object
    mfn_object = om2.MFnMesh(obj_dag_path)

    points = mfn_object.getPoints(space=om2.MSpace.kObject)

    return points


def get_sel_vtces_idcs():
    """
    Get the indices of the selected vertices.

    :return: DagPath of the current mesh, indices of the selected vertices
    :rtype: maya.api.OpenMaya.MDagPathArray, maya.api.OpenMaya.MIntArray
    """
    # Get current selection
    selection_list = om2.MGlobal.getActiveSelectionList()
    log.info("Selection list is : %s" % selection_list)

    # Get the dag dir_path and components of the first item in the list
    if selection_list.length() > 0:
        obj_dag_path, components = selection_list.getComponent(0)
    else:
        log.warning("No selection found.")
        return {"objs_path": om2.MDagPath(), "indices": om2.MIntArray()}

    # Initialize MDagPathArray
    dag_path_list = om2.MDagPathArray()

    # If no vertices selected
    if components.isNull():
        # Empty list of vertices
        selected_vertices_indices = om2.MIntArray()

        # Create iterator
        sel_iter = om2.MItSelectionList(selection_list)
        # Create list of dagPath of selected objects
        while not sel_iter.isDone():
            dag_path_list.append(sel_iter.getDagPath())
            sel_iter.next()
    # If vertices are selected
    else:

        dag_path_list.append(selection_list.getDagPath(0))
        # Query vertex indices
        fn_components = om2.MFnSingleIndexedComponent(components)
        # Create an MIntArray with the vertex indices
        selected_vertices_indices = fn_components.getElements()

    return {"objs_path": dag_path_list, "indices": selected_vertices_indices}
