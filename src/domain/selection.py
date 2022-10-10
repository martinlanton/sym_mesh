import logging

from maya.api import OpenMaya as om2

log = logging.getLogger(__name__)


def get_points_positions(obj_dag_path=None):
    """
    Get the position of every point of the selected mesh.

    :param obj_dag_path: dag path object of the geometry for which we want the points position
    :type obj_dag_path: maya.api.OpenMaya.MDagPath

    :return: position of the points
    :rtype: maya.api.OpenMaya.MPointArray
    """
    mfn_object = om2.MFnMesh(obj_dag_path)

    points = mfn_object.getPoints(space=om2.MSpace.kObject)

    return points


class VertexSelection(object):
    def __init__(self, from_list=None):
        """

        :param from_list:
        """
        self.dag_path = om2.MDagPath()
        self.indices = om2.MIntArray()

        if from_list is not None:
            self.get_selection_from_list()
        else:
            self.get_live_selection()

    def __str__(self):
        return "Vertex selection : path : {}, indices : {}".format(
            self.dag_path, self.indices
        )

    def get_live_selection(self):
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
            self.dag_path = om2.MDagPath()
            self.indices = om2.MIntArray()
            return

        # Initialize MDagPathArray
        dag_path_list = om2.MDagPathArray()

        # If no vertices selected
        if components.isNull():
            # Empty list of vertices
            self.dag_path = om2.MDagPath()
            self.indices = om2.MIntArray()
            return
        # If vertices are selected
        else:

            dag_path_list.append(selection_list.getDagPath(0))
            # Query vertex indices
            fn_components = om2.MFnSingleIndexedComponent(components)
            # Create an MIntArray with the vertex indices
            selected_vertices_indices = fn_components.getElements()

        if dag_path_list.__len__() > 1:
            log.error(
                "More than one object selected, unable to initialize a vertex selection."
            )
            del self
            return

        self.dag_path = dag_path_list[0]
        self.indices = selected_vertices_indices

    def get_selection_from_list(self, from_list=()):
        if not from_list:
            self.dag_path = om2.MDagPath()
            self.indices = om2.MIntArray()

    def select(self):
        if len(self.indices) == 0:
            log.warning("No vertex selection stored")
        else:
            vtcs_to_select = om2.MSelectionList()
            MItVtx = om2.MItMeshVertex(self.dag_path)
            while not MItVtx.isDone():
                if MItVtx.index() in self.indices:
                    vtcs_to_select.add((self.dag_path, MItVtx.currentItem()))
                MItVtx.next()
            om2.MGlobal.setActiveSelectionList(vtcs_to_select)
