import logging

import maya.api.OpenMaya as om2

from sym_mesh import dag_path


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class SymmetryTable:
    def __init__(self, mesh, axis="x", threshold=0.001):
        """Initialize the symmetry table using the specified mesh.

        :param mesh: name of the maya mesh to use to build the symmetry table.
        :type mesh: str

        """
        self._axis = axis
        self._threshold = threshold

        self._reference_mesh = dag_path.create_MDagPath(mesh)
        self._base_table = get_selected_mesh_points(self._reference_mesh)
        self._table = self.build()

    @property
    def table(self):
        return self._table

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, value):
        self._axis = value

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value
    
    def build(self):
        """
        Create symmetry table base on symmetry self._axis and self._threshold

        :return: symmetry table
        :rtype: dict
        """
        base_points = self._base_table["points_pos"]
        axis_idcs = {"x": 0, "y": 1, "z": 2}
        axis_idx = axis_idcs[self._axis]

        if self._threshold > 1:
            threshold_nb = -len(str(self._threshold).split(".")[0])
        else:
            threshold_nb = len(str(self._threshold).split(".")[1])

        non_mirrored_table = list()
        symmetry_table = dict()

        log.info(base_points.__len__())

        check_table = dict()

        MItVtx = om2.MItMeshVertex(self._base_table["objs_path"])
        while not MItVtx.isDone():
            position = (
                round(MItVtx.position()[0], threshold_nb),
                round(MItVtx.position()[1], threshold_nb),
                round(MItVtx.position()[2], threshold_nb),
            )
            check_table[position] = MItVtx.index()
            position_to_check = list(position)
            position_to_check[axis_idx] = -position_to_check[axis_idx]
            position_to_check = tuple(position_to_check)

            if position_to_check in check_table:
                symmetry_table[MItVtx.index()] = check_table[position_to_check]
                symmetry_table[check_table[position_to_check]] = MItVtx.index()

            MItVtx.next()

        if len(symmetry_table) < base_points.__len__():
            log.info(
                "Not all vertices are symmetrical,"
                " mirroring might not work as expected"
            )
        else:
            log.info("Model is symmetrical")

        MItVtx = om2.MItMeshVertex(self._base_table["objs_path"])
        while not MItVtx.isDone():
            if MItVtx.index() not in symmetry_table:
                non_mirrored_table.append(MItVtx.index())

            MItVtx.next()

        log.debug(len(symmetry_table))
        log.debug(symmetry_table)

        return symmetry_table, non_mirrored_table


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