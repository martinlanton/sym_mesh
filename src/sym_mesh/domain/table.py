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
        log.info(
            "Building symmetry table for mesh '%s' (axis=%s, direction=%s, threshold=%s).",
            base_mesh or self._dag_path,
            self._axis,
            self._direction,
            self.threshold,
        )

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
                "Model %s is NOT symmetrical, mirroring might not work as expected.",
                path,
            )
        else:
            log.info("Model %s is symmetrical.", path)

        self._symmetry_table = symmetry_map
        self._non_mirrored_vertices = selection.VertexSelection(
            (self.dag_path, non_mirrored_table)
        )

    def _build_symmetry_map(self, points_table):
        """Build the symmetry map as a dict ``{target_index: source_index}``.

        For each vertex, this method computes its mirror reflection across the
        symmetry plane and searches for a matching vertex within the Euclidean
        distance threshold.  Matched vertices are assigned a role:

        - **source** -- the vertex whose position is preserved and mirrored
          onto its counterpart during symmetry operations.
        - **target** -- the vertex that receives the mirrored position.

        The *direction* setting controls which half-space contains the sources.
        With ``positive`` direction the vertices on the negative side of the
        axis are the sources; with ``negative`` direction it is the opposite.

        Mathematical formulation:
            Given symmetry axis index ``a`` (0 = X, 1 = Y, 2 = Z), the mirror
            of a point ``p`` is defined as::

                mirror(p)_i = -p_i   if i = a
                mirror(p)_i =  p_i   otherwise

            Two vertices ``v_i`` and ``v_j`` form a symmetrical pair when::

                || mirror(v_i) - v_j ||_2  <  threshold

            where ``||.||_2`` is the Euclidean (L2) norm.

            Vertices that lie on the symmetry plane (``|p_a| < threshold / 2``)
            satisfy ``mirror(p) ~= p`` and therefore match themselves.  These
            self-paired vertices are included in the map as
            ``{idx: idx}`` so that they are not reported as non-mirrored.

            The distance comparison is performed in squared form
            (``d^2 < threshold^2``) to avoid the cost of a square root.

        Performance:
            Instead of comparing every vertex against every other vertex
            (O(n^2)), positions are discretized into a uniform spatial hash
            grid with cell size equal to the threshold.  For each vertex only
            the 3^3 = 27 cells surrounding its mirror position are inspected,
            yielding **O(n) average-case** complexity.

            For an in-depth discussion of spatial hashing see:
            Teschner, M. et al. (2003). *Optimized Spatial Hashing for
            Collision Detection of Deformable Objects.* Proceedings of VMV.
            https://matthias-research.github.io/pages/publications/tetraederCollision.pdf

        :param points_table: positions of all mesh vertices.
        :type points_table: maya.api.OpenMaya.MPointArray

        :return: symmetry map ``{target_index: source_index}``.
        :rtype: dict[int, int]
        """
        n = len(points_table)
        log.debug("Building symmetry map for %d points.", n)

        threshold = self.threshold
        axis = self.axis
        is_positive = self.positive
        threshold_sq = threshold * threshold

        cell_size = threshold if threshold > 0 else 1.0
        inv_cell = 1.0 / cell_size

        positions = [(pt[0], pt[1], pt[2]) for pt in points_table]
        grid = self._build_spatial_hash(positions, inv_cell)

        symmetry_map = {}
        for idx, position in enumerate(positions):
            mirror = list(position)
            mirror[axis] = -mirror[axis]
            mirror_cell = self._compute_cell_key(mirror, inv_cell)

            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    for dk in (-1, 0, 1):
                        cell_contents = grid.get(
                            (
                                mirror_cell[0] + di,
                                mirror_cell[1] + dj,
                                mirror_cell[2] + dk,
                            )
                        )
                        if cell_contents is None:
                            continue
                        for other_idx, other_pos in cell_contents:
                            dx = mirror[0] - other_pos[0]
                            dy = mirror[1] - other_pos[1]
                            dz = mirror[2] - other_pos[2]
                            if dx * dx + dy * dy + dz * dz < threshold_sq:
                                if (
                                    is_positive and position[axis] < other_pos[axis]
                                ) or (
                                    not is_positive and position[axis] > other_pos[axis]
                                ):
                                    symmetry_map[other_idx] = idx
                                else:
                                    symmetry_map[idx] = other_idx
        return symmetry_map

    @staticmethod
    def _compute_cell_key(position, inv_cell):
        """Quantize a 3D position into a spatial hash grid cell key.

        Each coordinate is mapped to the nearest integer grid index using
        round-half-away-from-zero rounding, which guarantees that any two
        points within one cell width of each other end up in the same cell
        or in directly adjacent cells.

        :param position: 3D coordinates to quantize.
        :type position: tuple[float, float, float] | list[float]

        :param inv_cell: inverse of the grid cell size (``1.0 / cell_size``).
        :type inv_cell: float

        :return: integer grid cell indices.
        :rtype: tuple[int, int, int]
        """
        return (
            int(position[0] * inv_cell + (0.5 if position[0] >= 0 else -0.5)),
            int(position[1] * inv_cell + (0.5 if position[1] >= 0 else -0.5)),
            int(position[2] * inv_cell + (0.5 if position[2] >= 0 else -0.5)),
        )

    @classmethod
    def _build_spatial_hash(cls, positions, inv_cell):
        """Populate a spatial hash grid from a list of vertex positions.

        Each vertex is placed in the grid cell corresponding to its quantized
        position (see :meth:`_compute_cell_key`).  The resulting dictionary
        maps cell keys to lists of ``(vertex_index, position)`` tuples.

        :param positions: vertex positions as a list of 3-tuples.
        :type positions: list[tuple[float, float, float]]

        :param inv_cell: inverse of the grid cell size (``1.0 / cell_size``).
        :type inv_cell: float

        :return: spatial hash grid.
        :rtype: dict[tuple[int, int, int], list[tuple[int, tuple[float, float, float]]]]
        """
        grid = {}
        for idx, pos in enumerate(positions):
            cell = cls._compute_cell_key(pos, inv_cell)
            grid.setdefault(cell, []).append((idx, pos))
        return grid

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
        mapped_indices = set(symmetry_map.keys()) | set(symmetry_map.values())
        non_mirrored_table = [
            idx for idx in range(len(points_table)) if idx not in mapped_indices
        ]

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
