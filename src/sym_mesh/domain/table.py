import logging
import math
from maya.api import OpenMaya as om2

from sym_mesh.domain import dag_path
from sym_mesh.domain import selection

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class GeometryTable:
    def __init__(
        self,
        mesh_dag_path,
        axis="x",
        threshold=0.001,
        direction="positive",
        space=om2.MSpace.kObject,
    ):
        """Initialize the symmetry table using the specified mesh.

        :param mesh_dag_path: name of the maya mesh to use to build the symmetry table.
        :type mesh_dag_path: str

        :param axis: axis to use to build the symmetry table
        :type axis: str

        :param threshold: threshold to use to identify symmetrical vertices
        :type threshold: flat

        :param direction: direction to use to build the symmetry table. Accepted
        directions are "positive" and "negative".
        :type direction: str

        :param space: space in which the point position should be queried.
        :type space: int

        """
        self._axis = axis
        self._axis_idcs = {"x": 0, "y": 1, "z": 2}
        self._direction = direction
        self.threshold = threshold
        self._space = space

        self._dag_path = mesh_dag_path
        self._points_table = selection.get_points_positions(self.dag_path, space=space)

        self._symmetry_table = None
        self._non_mirrored_vertices = selection.VertexSelection(from_list=())

        self.build_symmetry_table()

    def __str__(self):
        return self._dag_path

    @property
    def space(self):
        return self._space

    @property
    def symmetry_table(self):
        return self._symmetry_table

    @property
    def non_mirrored_vertices(self):
        """Return a vertex selection object containing all the non-mirrored vertices.

        :return: Vertex selection object containing all the non-mirrored vertices.
        :rtype: domain.selection.VertexSelection
        """
        return self._non_mirrored_vertices

    @property
    def axis(self):
        """Return the symmetrization axis as an int.

        x: 0
        y: 1
        z: 2

        :return: The symmetrization axis as an int.
        :rtype: int
        """
        return self._axis_idcs[self._axis]

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

    def build_symmetry_table(self, base_mesh=""):
        """Create symmetry table base on symmetry self._axis and self._threshold

        :param base_mesh: optional. Name of the mesh to use to build the symmetry table.
        :type base_mesh: str

        :return: symmetry table
        :rtype: dict

        """
        points_table = (
            selection.get_points_positions(
                dag_path.create_MDagPath(base_mesh), self.space
            )
            if base_mesh
            else self._points_table
        )
        symmetry_map = self._build_symmetry_map(points_table)
        non_mirrored_table = self._get_non_mirrored_vertices(points_table, symmetry_map)

        path = base_mesh if base_mesh else self.dag_path
        if non_mirrored_table:
            log.warning(
                "Model %s is NOT symmetrical," " mirroring might not work as expected.",
                path,
            )
        else:
            log.info("Model %s is symmetrical.", path)

        self._symmetry_table = symmetry_map
        self._non_mirrored_vertices = selection.VertexSelection(
            (self.dag_path, non_mirrored_table)
        )

    def _build_symmetry_map(self, points_table):
        """Build the symmetry map as a dict {target: source}.

        :param points_table: MPointArray of the positions of all the points
        :type points_table: maya.api.OpenMaya.MPointArray

        :return: map of the symmetry as a dict {target: source}.
        :rtype: dict[int: int]
        """
        symmetry_map = dict()
        check_table = dict()
        for idx, item in enumerate(points_table):
            position = (item[0], item[1], item[2])
            check_table[position] = idx
            position_to_check = self._get_opposite_position(position)

            for pos in check_table:
                if self._distance(position_to_check, pos) < self.threshold:
                    if self._vertex_should_be_symmetry_source(position, pos):
                        symmetry_map[check_table[pos]] = idx
                    else:  # Vertex should be symmetry target
                        symmetry_map[idx] = check_table[pos]
        return symmetry_map

    def _get_opposite_position(self, position):
        """Get the opposite position along the selected symmetry axis.

        :param position: position for which we want the opposite.
        :type position: tuple(float, float, float)

        :return: Opposite position along the symmetry axis
        :rtype: tuple(float, float, float)
        """
        position_to_check = list(position)
        position_to_check[self.axis] = -position_to_check[self.axis]
        position_to_check = tuple(position_to_check)
        return position_to_check

    def _vertex_should_be_symmetry_source(self, position, position_to_check):
        return (
            self.positive and (position[self.axis] < position_to_check[self.axis])
        ) or (
            not self.positive and (position[self.axis] > position_to_check[self.axis])
        )

    @staticmethod
    def _get_non_mirrored_vertices(points_table, symmetry_map):
        """Get the list of the vertex indices that do not have a mirrored counterpart.

        :param points_table:
        :type points_table: maya.api.OpenMaya.MPointArray

        :param symmetry_map: map of the symmetry as a dict {target: source}.
        :type symmetry_map: dict[int: int]

        :return: list of the vertex indices that do not have a mirrored counterpart.
        :rtype: list[int]
        """
        non_mirrored_table = list()
        for idx in range(len(points_table)):
            if idx not in list(symmetry_map.keys()) + list(symmetry_map.values()):
                non_mirrored_table.append(idx)
        return non_mirrored_table

    @staticmethod
    def _distance(point_a, point_b):
        """Calculate the distance between 2 points.

        :param point_a: starting point
        :type point_a: tuple(float, float, float)

        :param point_b: point to subtract
        :type point_b: tuple(float, float, float)

        :return: distance between the 2 vectors
        :rtype: float
        """
        vector = (
            point_a[0] - point_b[0],
            point_a[1] - point_b[1],
            point_a[2] - point_b[2],
        )
        distance = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
        return distance
