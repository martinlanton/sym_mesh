from maya.api import OpenMaya as om2


def get_selected_mesh_points(obj_dag_path=None):
    """
    Get the position of every point of the selected mesh.

    :return: dag dir_path of the object, position of the points
    :rtype: MDagPath, MPointArray
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

    return {"objs_path": obj_dag_path, "points_pos": points}