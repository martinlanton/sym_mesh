import maya.api.OpenMaya as om2
import logging

from sym_mesh.domain import commands
from sym_mesh.domain.dag_path import create_MDagPath

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class MeshModifier(object):
    def __init__(self):
        # Attributes
        self._revert_value = 100
        self.space = om2.MSpace.kObject
        # UNDO LIST
        self.undo_queue = list()
        self.redo_queue = list()

    @property
    def revert_value(self):
        return self._revert_value

    @revert_value.setter
    def revert_value(self, value):
        self._revert_value = value

    def undo(self):
        """Undo the last move stored in the undo queue."""
        if len(self.undo_queue) > 0:
            last_action = self.undo_queue.pop(-1)
        else:
            log.error("No action action to undo.")
            return

        last_action.undo()
        self.redo_queue.append(last_action)

    def redo(self):
        """Redo the last move stored in the redo queue."""
        if len(self.redo_queue) > 0:
            last_action = self.redo_queue.pop(-1)
        else:
            log.error("No action action to redo.")
            return

        last_action.redo()
        self.undo_queue.append(last_action)

    def bake_difference(
        self,
        base_table,
        target_table,
        selected_vertices_indices=(),
        percentage=100,
        target_dag_path=None,
        space=om2.MSpace.kObject,
    ):
        """
        Bake the difference between 2 mesh on a list of vertices on a selection
        of meshes.

        :param base_table: GeometryTable of the base geometry
        :type base_table: sym_mesh.table.GeometryTable

        :param target_table: GeometryTable of the target geometry
        :type target_table: sym_mesh.table.GeometryTable

        :param selected_vertices_indices: indices of the selected points on the target mesh
        :type selected_vertices_indices: maya.api.OpenMaya.MIntArray

        :param percentage: percentage used for the bake delta function. This
        is a value from 0 to 100, a value of 100 means we're adding the full
        delta between base and target to the destination meshes, a value of 0
        means we're staying at the current position.
        :type percentage: int

        :param target_dag_path: MDagPath of the target
        :type target_dag_path: maya.api.OpenMaya.MDagPath or str

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        if not isinstance(target_dag_path, om2.MDagPath):
            target_dag_path = create_MDagPath(target_dag_path)

        cmd = commands.BakeDifferenceCommand(
            base_table,
            target_table,
            selected_vertices_indices,
            percentage,
            target_dag_path,
            space,
        )
        self.undo_queue.append(cmd)

    def revert_to_base(
        self,
        base_table,
        target_table,
        selected_vertices_indices=(),
        percentage=100,
        space=om2.MSpace.kObject,
    ):
        """
        Revert selected vertices on the target mesh to the base position.

        :param base_table: positions of the points of the base mesh
        :type base_table: sym_mesh.table.GeometryTable

        :param target_table: positions of the points of the current mesh
        :type target_table: sym_mesh.table.GeometryTable

        :param selected_vertices_indices: indices of the selected points on the target mesh
        :type selected_vertices_indices: maya.api.OpenMaya.MIntArray

        :param percentage: percentage used for the revert to base function. This
        is a value from 0 to 100, a value of 100 means we're reverting the
        position of the base, a value of 0 means we're staying at the current
        position.
        :type percentage: int

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        cmd = commands.RevertToBaseCommand(
            base_table,
            target_table,
            selected_vertices_indices,
            percentage,
            target_table.dag_path.getPath(),
            space,
        )
        self.undo_queue.append(cmd)

    def symmetrize(
        self,
        base_table,
        target_table,
        selected_vertices_indices=(),
        percentage=100,
        space=om2.MSpace.kObject,
    ):
        """
        Symmetrize selected vertices on the target mesh.

        :param base_table: positions of the points of the base mesh
        :type base_table: sym_mesh.table.GeometryTable

        :param target_table: positions of the points of the current mesh
        :type target_table: sym_mesh.table.GeometryTable

        :param selected_vertices_indices: indices of the selected points on the target mesh
        :type selected_vertices_indices: maya.api.OpenMaya.MIntArray

        :param percentage: percentage used for the revert to base function
        :type percentage: int

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        cmd = commands.SymmetrizeCommand(
            base_table,
            target_table,
            selected_vertices_indices,
            percentage,
            target_table.dag_path.getPath(),
            space,
        )
        self.undo_queue.append(cmd)

    def extract_axes(self, base_table, target_table):
        """Extract deltas between target table and base table on a new geometry.

        :param base_table:
        :type base_table: sym_mesh.table.GeometryTable

        :param target_table:
        :type target_table: sym_mesh.table.GeometryTable

        :return: names of the newly created geometries
        :rtype: str, str, str
        """
        cmd = commands.ExtractAxesCommand(base_table, target_table)

        self.undo_queue.append(cmd)
        return cmd.result

    def flip(
        self,
        base_table,
        target_table,
        selected_vertices_indices=(),
        percentage=100,
        space=om2.MSpace.kObject,
    ):
        """Flip selected vertices on the target mesh.

        :param base_table: positions of the points of the base mesh
        :type base_table: sym_mesh.table.GeometryTable

        :param target_table: positions of the points of the current mesh
        :type target_table: sym_mesh.table.GeometryTable

        :param selected_vertices_indices: indices of the selected points on the target mesh
        :type selected_vertices_indices: maya.api.OpenMaya.MIntArray

        :param percentage: percentage used for the revert to base function
        :type percentage: int

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        cmd = commands.FlipCommand(
            base_table,
            target_table,
            selected_vertices_indices,
            percentage,
            target_table.dag_path.getPath(),
            space,
        )
        self.undo_queue.append(cmd)
