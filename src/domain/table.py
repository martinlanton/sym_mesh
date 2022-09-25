import logging

from domain import dag_path
from domain.selection import get_points_positions

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class GeometryTable:
    def __init__(self, mesh_dag_path, axis="x", threshold=0.001, direction="positive"):
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

        """
        self._axis = axis
        self._direction = direction  # todo : convert this to an enum
        self._threshold = 0.001
        self._threshold_nb = 3

        self._dag_path = mesh_dag_path
        self._points_table = get_points_positions(self.dag_path)
        self._symmetry_table = None

        self.threshold = threshold
        self.build_symmetry_table()

    def __str__(self):
        return self._dag_path

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
        # TODO : test symmetry table building with higher threshold
        self._threshold = value
        if self._threshold > 1:
            self._threshold_nb = -len(str(self._threshold).split(".")[0])
        else:
            self._threshold_nb = len(str(self._threshold).split(".")[1])

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

    def build_symmetry_table(self, base_mesh=""):
        """Create symmetry table base on symmetry self._axis and self._threshold

        :param base_mesh: optional. Name of the mesh to use to build the symmetry table.
        :type base_mesh: str

        :return: symmetry table
        :rtype: dict

        """
        # TODO : simplify this method
        if base_mesh:
            path = base_mesh
            points_table = get_points_positions(dag_path.create_MDagPath(base_mesh))
        else:
            path = self.dag_path
            points_table = self._points_table
        axis_idcs = {"x": 0, "y": 1, "z": 2}
        axis_idx = axis_idcs[self._axis]

        non_mirrored_table = list()
        symmetry_table = dict()

        check_table = dict()

        for idx, item in enumerate(points_table):
            position = (
                round(item[0], self._threshold_nb),
                round(item[1], self._threshold_nb),
                round(item[2], self._threshold_nb),
            )
            check_table[position] = idx
            position_to_check = list(position)
            position_to_check[axis_idx] = -position_to_check[axis_idx]
            position_to_check = tuple(position_to_check)

            if position_to_check in check_table:
                if self.positive:
                    if position[axis_idx] < position_to_check[axis_idx]:
                        symmetry_table[check_table[position_to_check]] = idx
                    else:
                        symmetry_table[idx] = check_table[position_to_check]
                else:
                    if position[axis_idx] > position_to_check[axis_idx]:
                        symmetry_table[check_table[position_to_check]] = idx
                    else:
                        symmetry_table[idx] = check_table[position_to_check]

        for idx in range(len(points_table)):
            if idx not in symmetry_table and idx not in symmetry_table.values():
                non_mirrored_table.append(idx)

        log.debug(len(symmetry_table))
        log.debug(symmetry_table)

        # todo : test that this prints the right message.
        if non_mirrored_table:
            log.info(
                "Model %s is NOT symmetrical," " mirroring might not work as expected.",
                path,
            )
        else:
            log.info("Model %s is symmetrical.", path)

        self._symmetry_table = symmetry_table, non_mirrored_table
