import abc
import logging
from pprint import pformat
import six

from maya.api import OpenMaya as om2

from domain.selection import get_points_positions

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@six.add_metaclass(abc.ABCMeta)
class AbstractDeformationCommand(object):
    def __init__(
        self,
        base_table,
        target_table,
        selected_vertices_indices=(),
        percentage=100,
        target_dag_path=None,
        space=om2.MSpace.kObject,
    ):
        """Initialize the deformation command with the proper attributes.

        :param base_table: GeometryTable of the base geometry
        :type base_table: sym_mesh.table.GeometryTable

        :param target_table: GeometryTable of the target geometry
        :type target_table: sym_mesh.table.GeometryTable

        :param selected_vertices_indices: indices of the selected points on the target mesh
        :type selected_vertices_indices: maya.api.OpenMaya.MIntArray

        :param percentage: percentage used for the computing operation. This
        is a value from 0 to 100, a value of 100 means we're adding the full
        value of the computation between the base and target meshes to the
        destination mesh, a value of 0 means we're staying at the current position.
        :type percentage: int

        :param target_dag_path: MDagPath of the target
        :type target_dag_path: maya.api.OpenMaya.MDagPath

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        log.debug("base_table : %s", base_table)
        log.debug("target_table : %s", target_table)
        log.debug("selected_vertices_indices : %s", selected_vertices_indices)
        log.debug("percentage : %s", percentage)
        log.debug("target_dag_path : %s", target_dag_path)
        log.debug("space : %s", space)
        self.base_table = base_table
        self.target_table = target_table
        self.selected_vertices_indices = selected_vertices_indices
        self.percentage = percentage
        self.target_dag_path = target_dag_path
        self.space = space
        self.current_point_array = get_points_positions(target_dag_path)
        self.undo_action = self.current_point_array
        self.result = self.deform()
        self.redo_action = self.result

    def deform(self):
        """
        Bake the difference between 2 mesh on a list of vertices on a mesh.
        """
        base_point_array = self.base_table.point_array
        log.debug("base_point_array :\n%s", pformat(base_point_array))
        target_point_array = self.target_table.point_array
        log.debug("target_point_array :\n%s", pformat(target_point_array))
        destination_point_array = self.compute_point_position(
            base_point_array, target_point_array
        )

        # Modify points position using the new coordinates
        tgt_mesh_functionset = om2.MFnMesh(self.target_dag_path)
        tgt_mesh_functionset.setPoints(destination_point_array, self.space)

        return destination_point_array

    def undo(self):
        tgt_mesh_functionset = om2.MFnMesh(self.target_dag_path)
        tgt_mesh_functionset.setPoints(self.undo_action, self.space)

    def redo(self):
        tgt_mesh_functionset = om2.MFnMesh(self.target_dag_path)
        tgt_mesh_functionset.setPoints(self.redo_action, self.space)

    @abc.abstractmethod
    def compute_point_position(self, base_point_array, target_point_array):
        raise NotImplementedError
