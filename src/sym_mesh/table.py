import logging

import maya.api.OpenMaya as om2

from sym_mesh import dag_path
from sym_mesh.selection import get_selected_mesh_points

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class GeometryTable:
    def __init__(self, mesh, axis="x", threshold=0.001):
        """Initialize the symmetry table using the specified mesh.

        :param mesh: name of the maya mesh to use to build the symmetry table.
        :type mesh: str

        """
        self._axis = axis
        self._threshold = threshold

        self._dag_path = dag_path.create_MDagPath(mesh)
        self._points_table = get_selected_mesh_points(self._dag_path)
        self._symmetry_table = None
        self.build_symmetry_table()

    @property
    def symmetry_table(self):
        return self._symmetry_table

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

    @property
    def dag_path(self):
        return self._dag_path

    @property
    def point_array(self):
        return self._points_table
    
    def build_symmetry_table(self, base_mesh=None):
        """
        Create symmetry table base on symmetry self._axis and self._threshold

        :param base_mesh: optional. Name of the mesh to use to build the symmetry table.

        :return: symmetry table
        :rtype: dict
        """
        # TODO : symmetry table should only contain half of the points at the
        #  end, based on the direction of the symmetry
        if base_mesh:
            path = dag_path.create_MDagPath(base_mesh)
            points_table = get_selected_mesh_points(path)
        else:
            path = self._dag_path
            points_table = self._points_table
        base_points = points_table
        axis_idcs = {"x": 0, "y": 1, "z": 2}
        axis_idx = axis_idcs[self._axis]

        if self._threshold > 1:
            threshold_nb = -len(str(self._threshold).split(".")[0])
        else:
            threshold_nb = len(str(self._threshold).split(".")[1])

        non_mirrored_table = list()
        symmetry_table = dict()

        check_table = dict()

        MItVtx = om2.MItMeshVertex(path)
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

        MItVtx = om2.MItMeshVertex(self._dag_path)
        while not MItVtx.isDone():
            if MItVtx.index() not in symmetry_table:
                non_mirrored_table.append(MItVtx.index())

            MItVtx.next()

        log.debug(len(symmetry_table))
        log.debug(symmetry_table)

        self._symmetry_table = symmetry_table, non_mirrored_table
