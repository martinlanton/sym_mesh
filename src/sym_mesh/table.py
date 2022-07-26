import logging

import maya.api.OpenMaya as om2

from sym_mesh import dag_path
from sym_mesh.selection import get_selected_mesh_points

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class GeometryTable:
    def __init__(self, mesh_dag_path, axis="x", threshold=0.001, direction="positive"):
        """Initialize the symmetry table using the specified mesh.

        :param mesh_dag_path: name of the maya mesh to use to build the symmetry table.
        :type mesh_dag_path: str

        """
        self._axis = axis
        self._direction = direction  # todo : convert this to an enum
        self._threshold = threshold

        self._dag_path = mesh_dag_path
        self._points_table = get_selected_mesh_points(self.dag_path)
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
        return dag_path.create_MDagPath(self._dag_path)

    @property
    def point_array(self):
        return self._points_table

    @property
    def positive(self):
        if self._direction == "positive":
            return True
        return False

    @positive.setter
    def positive(self, value):
        if value:
            self._direction = "positive"
        else:
            self._direction = "negative"
    
    def build_symmetry_table(self, base_mesh=None):
        """
        Create symmetry table base on symmetry self._axis and self._threshold

        :param base_mesh: optional. Name of the mesh to use to build the symmetry table.

        :return: symmetry table
        :rtype: dict
        """
        # TODO : simplify this method
        if base_mesh:
            path = dag_path.create_MDagPath(base_mesh)
            points_table = get_selected_mesh_points(path)
        else:
            path = self.dag_path
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
            idx = MItVtx.index()
            check_table[position] = idx
            position_to_check = list(position)
            position_to_check[axis_idx] = -position_to_check[axis_idx]
            position_to_check = tuple(position_to_check)

            if self.positive:
                if position_to_check in check_table:
                    if position[axis_idx] < position_to_check[axis_idx]:
                        symmetry_table[idx] = check_table[position_to_check]
                    else:
                        symmetry_table[check_table[position_to_check]] = idx
            else:
                if position_to_check in check_table:
                    if position[axis_idx] < position_to_check[axis_idx]:
                        symmetry_table[check_table[position_to_check]] = idx
                    else:
                        symmetry_table[idx] = check_table[position_to_check]

            MItVtx.next()

        if len(symmetry_table) < base_points.__len__():
            log.info(
                "Not all vertices are symmetrical,"
                " mirroring might not work as expected"
            )
        else:
            log.info("Model is symmetrical")

        MItVtx = om2.MItMeshVertex(self.dag_path)
        while not MItVtx.isDone():
            idx = MItVtx.index()
            if idx not in symmetry_table and idx not in symmetry_table.values():
                non_mirrored_table.append(idx)

            MItVtx.next()

        log.debug(len(symmetry_table))
        log.debug(symmetry_table)

        self._symmetry_table = symmetry_table, non_mirrored_table
