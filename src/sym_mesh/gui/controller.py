from maya import cmds as mc
import logging

from sym_mesh.domain import executor
from sym_mesh.domain import table
from sym_mesh.domain.commands.deformation_commands import (
    BakeDifferenceCommand,
    FlipCommand,
    RevertToBaseCommand,
    SymmetrizeCommand,
)
from sym_mesh.domain.commands.geometry_commands import ExtractAxesCommand
from sym_mesh.domain.selection import VertexSelection
from sym_mesh.gui import signal

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Controller(object):
    def __init__(self):
        log.info("Initializing controller")
        # Attributes
        self.get_vertex_selection(reset=True)

        self.vertex_selection = VertexSelection(from_list=())

        self.executor = executor.Executor()

        self.vertices_are_stored = False
        self._threshold = 0.001
        self._percentage = 100
        self._direction = "positive"
        self._axis = "x"
        self.translate_value = 20
        self.base_table: sym_mesh.domain.table.GeometryTable = None
        self.target_table: sym_mesh.domain.table.GeometryTable = None

        # Signals
        self.set_base = signal.Signal()
        self.set_target = signal.Signal()

    @property
    def threshold(self):
        return self._threshold  # pragma: no cover

    @threshold.setter
    def threshold(self, value):
        """Set the threshold and regenerate the base geometry table."""
        log.info("Setting threshold to : %s", value)
        self._threshold = value

        self._regenerate_base()

    @property
    def axis(self):
        return self._axis  # pragma: no cover

    @axis.setter
    def axis(self, value):
        """Set the axis and regenerate the base geometry table."""
        log.info("Setting axis to : %s", value)
        self._axis = value

        self._regenerate_base()

    @property
    def direction(self):
        return self._direction  # pragma: no cover

    @direction.setter
    def direction(self, value):
        """Set the direction and regenerate the base geometry table."""
        log.info("Setting direction to : %s", value)
        self._direction = value

        self._regenerate_base()

    def _regenerate_base(self):
        """Regenerate the geometry table for the base mesh. This is a convenience
        method used exclusively to regenerate the existing base geometry table
        when setting the properties to change the threshold, axis, or direction
        to use for the geometry tables."""
        if self.base_table:
            mesh = str(self.base_table)
            log.debug(
                "Existing base table found, regenerating base table with "
                'mesh "{}", axis "{}", direction "{}", threshold "{}"'.format(
                    mesh, self._axis, self._direction, self._threshold
                )
            )
            self.base_table = table.GeometryTable(
                mesh,
                axis=self._axis,
                direction=self._direction,
                threshold=self._threshold,
            )
            self.set_base.emit(mesh)

    def get_base(self):
        """
        Get base data and set its name in the corresponding lineEdit.
        :return:
        """
        mesh = mc.ls(sl=True)[0]
        self.base_table = table.GeometryTable(
            mesh, axis=self._axis, direction=self._direction, threshold=self._threshold
        )
        self.set_base.emit(mesh)

    def get_target(self):
        """Get target data and set its name in the corresponding lineEdit."""
        mesh = mc.ls(sl=True)[0]
        self.target_table = table.GeometryTable(
            mesh, axis=self._axis, direction=self._direction, threshold=self._threshold
        )
        self.set_target.emit(mesh)

    def get_vertex_selection(self, reset=False):
        """Get the current selection of vertices and set it.

        :param reset: Set whether the currently stored selection should be set
        to an empty selection.
        :type reset: bool
        """
        if reset:
            self.vertex_selection = VertexSelection(from_list=())
        else:
            self.vertex_selection = VertexSelection()
            log.info("Selection is %s", self.vertex_selection)

        if len(self.vertex_selection.indices) > 0:
            self.vertices_are_stored = True
        else:
            self.vertices_are_stored = False

    def select_stored_vertices(self):
        self.vertex_selection.select()

    def select_non_mirrored_vertices(self):
        self.base_table.non_mirrored_vertices.select()

    def revert_to_base(self):
        """Revert selected mesh or vertices to base from the current value, using
        vertices selection (if one has been stored or is active) or on the whole
        mesh."""
        selection = mc.ls(sl=True)
        if not selection:
            log.error("Unable to revert to base, no target selected.")
            return
        target = selection[0]
        base_table = self.base_table
        if not base_table:
            log.error("Unable to revert to base, no base defined.")
            return
        target_table = table.GeometryTable(
            target,
            axis=self._axis,
            direction=self._direction,
            threshold=self._threshold,
        )
        vertex_selection = (
            self.vertex_selection if self.vertices_are_stored else VertexSelection()
        )
        self.executor.execute(
            RevertToBaseCommand,
            base_table=base_table,
            target_table=target_table,
            vertex_selection=vertex_selection,
            percentage=100,
        )
        self.executor.stash_command()

    def revert_to_base_live(self, value):
        """Revert selected mesh or vertices to base from the current value, using
        vertices selection (if one has been stored or is active) or on the whole
        mesh.

        :param value: percentage value to use for the revert to base operation.
        :type value: int
        """
        if not self.executor.has_active_command():
            selection = mc.ls(sl=True)
            if not selection:
                log.error("Unable to revert to base, no target selected.")
                return
            target = selection[0]
            base_table = self.base_table
            if not base_table:
                log.error("Unable to revert to base, no base defined.")
                return
            target_table = table.GeometryTable(
                target,
                axis=self._axis,
                direction=self._direction,
                threshold=self._threshold,
            )
            vertex_selection = (
                self.vertex_selection if self.vertices_are_stored else VertexSelection()
            )
            self.executor.execute(
                RevertToBaseCommand,
                base_table=base_table,
                target_table=target_table,
                vertex_selection=vertex_selection,
                percentage=value,
            )
        else:
            self.executor.command.percentage = value

    def stash_command(self):
        self.executor.stash_command()

    def symmetrize(self):
        """Symmetrize selected mesh or vertices from the current value, using
        vertices selection (if one has been stored or is active) or on the whole
        mesh.
        """
        selection = mc.ls(sl=True)
        if not selection:
            log.error("Unable to symmetrize, no target selected.")
            return
        target = selection[0]
        base_table = self.base_table
        if not base_table:
            log.error("Unable to symmetrize, no base defined.")
            return
        vertex_selection = (
            self.vertex_selection if self.vertices_are_stored else VertexSelection()
        )
        target_table = table.GeometryTable(
            target,
            axis=self._axis,
            direction=self._direction,
            threshold=self._threshold,
        )
        self.executor.execute(
            SymmetrizeCommand,
            base_table=base_table,
            target_table=target_table,
            vertex_selection=vertex_selection,
            percentage=100,
        )
        self.executor.stash_command()

    def symmetrize_live(self, value):
        """Symmetrize selected mesh or vertices from the current value, using
        vertices selection (if one has been stored or is active) or on the whole
        mesh.

        :param value: percentage value to use for the symmetry operation.
        :type value: int
        """
        if not self.executor.has_active_command():
            selection = mc.ls(sl=True)
            if not selection:
                log.error("Unable to symmetrize, no target selected.")
                return
            target = selection[0]
            base_table = self.base_table
            if not base_table:
                log.error("Unable to symmetrize, no base defined.")
                return
            vertex_selection = (
                self.vertex_selection if self.vertices_are_stored else VertexSelection()
            )
            target_table = table.GeometryTable(
                target,
                axis=self._axis,
                direction=self._direction,
                threshold=self._threshold,
            )
            self.executor.execute(
                SymmetrizeCommand,
                base_table=base_table,
                target_table=target_table,
                vertex_selection=vertex_selection,
                percentage=value,
            )
        else:
            self.executor.command.percentage = value

    def flip(self):
        selection = mc.ls(sl=True)
        if not selection:
            log.error("Unable to flip, no target selected.")
            return
        target = selection[0]
        base_table = self.base_table
        if not base_table:
            log.error("Unable to flip, no base defined.")
            return
        vertex_selection = (
            self.vertex_selection if self.vertices_are_stored else VertexSelection()
        )
        target_table = table.GeometryTable(
            target,
            axis=self._axis,
            direction=self._direction,
            threshold=self._threshold,
        )
        self.executor.execute(
            FlipCommand,
            base_table=base_table,
            target_table=target_table,
            vertex_selection=vertex_selection,
            percentage=self._percentage,
        )
        self.executor.stash_command()

    def flip_live(self, value):
        """Flip selected mesh or vertices from the current value, using
        vertices selection (if one has been stored or is active) or on the whole
        mesh.

        :param value: percentage value to use for the flip operation.
        :type value: int
        """
        if not self.executor.has_active_command():
            selection = mc.ls(sl=True)
            if not selection:
                log.error("Unable to flip, no target selected.")
                return
            target = selection[0]
            base_table = self.base_table
            if not base_table:
                log.error("Unable to flip, no base defined.")
                return
            vertex_selection = (
                self.vertex_selection if self.vertices_are_stored else VertexSelection()
            )
            target_table = table.GeometryTable(
                target,
                axis=self._axis,
                direction=self._direction,
                threshold=self._threshold,
            )
            self.executor.execute(
                FlipCommand,
                base_table=base_table,
                target_table=target_table,
                vertex_selection=vertex_selection,
                percentage=value,
            )
        else:
            self.executor.command.percentage = value

    def extract_axes(self):
        selection = mc.ls(sl=True)
        if not selection:
            log.error("Unable to extract axes, no target selected.")
            return
        target = selection[0]
        base_table = self.base_table
        if not base_table:
            log.error("Unable to extract axes, no base defined.")
            return
        target_table = table.GeometryTable(
            target,
            axis=self._axis,
            direction=self._direction,
            threshold=self._threshold,
        )
        self.executor.execute(
            ExtractAxesCommand,
            base_table=base_table,
            target_table=target_table,
            translate=self.translate_value,
        )
        self.executor.stash_command()

    def bake_deltas(self):
        """
        Revert selected mesh or vertices to base from the current value, using
        vertices selection (if one has been stored or is active) or on the whole
        mesh.

        """
        target_paths = mc.ls(sl=True)
        if not target_paths:
            log.error("Unable to bake deltas, no selected geometries to bake onto.")
            return
        target_table = self.target_table
        if not target_table:
            log.error("Unable to bake deltas, no target position defined.")
            return
        base_table = self.base_table
        if not base_table:
            log.error("Unable to bake deltas, no base position defined.")
            return
        for target_path in target_paths:
            self.executor.execute(
                BakeDifferenceCommand,
                base_table=base_table,
                target_table=target_table,
                vertex_selection=self.vertex_selection,
                percentage=self._percentage,
                target_dag_path=target_path,
            )
            self.executor.stash_command()

    def undo(self):
        self.executor.undo()

    def redo(self):
        self.executor.redo()
