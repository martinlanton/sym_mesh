import maya.api.OpenMaya as om2
import logging

from domain import commands
from domain.dag_path import create_MDagPath
from domain import selection

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# TODO : In its current form, the MeshModifier class is nothing more than an
#  executor, although without a registry of available commands. This means that
#  it does not actually serve any purpose. As soon as all commands are modified
#  to exclusively use the maya API, instead of the cmds (currently only in the
#  extract axes command), I should convert those commands to MPxCommand to get a
#  proper maya undo/redo behavior and use Maya as the executor and registry.
#  This will allow calling the commands directly from the controller instead of
#  through the MeshModifier class. It will require however a refactor of the
#  commands tests as well as of their undo/redo
#  *
#  This might not be possible depending on how I want to setup the undo
#  mechanism for some commands.


class MeshModifier(object):
    def __init__(self):
        self.undo_queue = list()
        self.redo_queue = list()

    def undo(self):
        """Undo the last move stored in the undo queue."""
        if len(self.undo_queue) > 0:
            last_action = self.undo_queue.pop(-1)
        else:
            log.error("No action to undo.")
            return

        last_action.undo()
        self.redo_queue.append(last_action)

    def redo(self):
        """Redo the last move stored in the redo queue."""
        if len(self.redo_queue) > 0:
            last_action = self.redo_queue.pop(-1)
        else:
            log.error("No action to redo.")
            return

        last_action.redo()
        self.undo_queue.append(last_action)

    def bake_difference(
        self,
        base_table,
        target_table,
        vertex_selection=selection.VertexSelection(from_list=()),
        percentage=100,
        target_dag_path=None,
    ):
        """
        Bake the difference between 2 mesh on a list of vertices on a selection
        of meshes.

        :param base_table: GeometryTable of the base geometry
        :type base_table: domain.table.GeometryTable

        :param target_table: GeometryTable of the target geometry
        :type target_table: domain.table.GeometryTable

        :param vertex_selection: indices of the selected points on the target mesh
        :type vertex_selection: domain.selection.VertexSelection

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
            base_table, target_table, vertex_selection, percentage, target_dag_path,
        )
        self.undo_queue.append(cmd)

    def revert_to_base(
        self,
        base_table,
        target_table,
        vertex_selection=selection.VertexSelection(from_list=()),
        percentage=100,
    ):
        """
        Revert selected vertices on the target mesh to the base position.

        :param base_table: positions of the points of the base mesh
        :type base_table: domain.table.GeometryTable

        :param target_table: positions of the points of the current mesh
        :type target_table: domain.table.GeometryTable

        :param vertex_selection: indices of the selected points on the target mesh
        :type vertex_selection: domain.selection.VertexSelection

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
            vertex_selection,
            percentage,
            target_table.dag_path.getPath(),
        )
        self.undo_queue.append(cmd)

    def symmetrize(
        self,
        base_table,
        target_table,
        vertex_selection=selection.VertexSelection(from_list=()),
        percentage=100,
    ):
        """
        Symmetrize selected vertices on the target mesh.

        :param base_table: positions of the points of the base mesh
        :type base_table: domain.table.GeometryTable

        :param target_table: positions of the points of the current mesh
        :type target_table: domain.table.GeometryTable

        :param vertex_selection: indices of the selected points on the target mesh
        :type vertex_selection: domain.selection.VertexSelection

        :param percentage: percentage used for the revert to base function
        :type percentage: int

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        cmd = commands.SymmetrizeCommand(
            base_table,
            target_table,
            vertex_selection,
            percentage,
            target_table.dag_path.getPath(),
        )
        self.undo_queue.append(cmd)

    def extract_axes(self, base_table, target_table):
        """Extract deltas between target table and base table on a new geometry.

        :param base_table:
        :type base_table: domain.table.GeometryTable

        :param target_table:
        :type target_table: domain.table.GeometryTable

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
        vertex_selection=selection.VertexSelection(from_list=()),
        percentage=100,
    ):
        """Flip selected vertices on the target mesh.

        :param base_table: positions of the points of the base mesh
        :type base_table: domain.table.GeometryTable

        :param target_table: positions of the points of the current mesh
        :type target_table: domain.table.GeometryTable

        :param vertex_selection: indices of the selected points on the target mesh
        :type vertex_selection: domain.selection.VertexSelection

        :param percentage: percentage used for the revert to base function
        :type percentage: int

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        cmd = commands.FlipCommand(
            base_table,
            target_table,
            vertex_selection,
            percentage,
            target_table.dag_path.getPath(),
        )
        self.undo_queue.append(cmd)
