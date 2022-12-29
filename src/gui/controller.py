from maya import cmds as mc
import logging

import domain.table
from domain import mesh_modification
from domain.selection import VertexSelection
from gui import signal
from domain import table


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Controller(object):
    def __init__(self):
        log.info("Initializing controller")
        # Attributes
        self.get_vertex_selection(reset=True)

        self.vertex_selection = VertexSelection(from_list=())

        self.mesh_modifier = mesh_modification.MeshModifier()

        self.vertices_are_stored = False
        self._threshold = 0.001
        self._percentage = 100
        self._direction = "positive"
        self._axis = "x"
        self.base_table: domain.table.GeometryTable = None
        self.target_table: domain.table.GeometryTable = None

        # Signals
        self.set_base = signal.Signal()
        self.set_target = signal.Signal()

    @property
    def threshold(self):
        return self._threshold  # pragma: no cover

    @threshold.setter
    def threshold(self, value):
        log.info("Setting threshold to : %s", value)
        self._threshold = value

        self._regenerate_base()

    @property
    def axis(self):
        return self._axis  # pragma: no cover

    @axis.setter
    def axis(self, value):
        log.info("Setting axis to : %s", value)
        self._axis = value

        self._regenerate_base()

    @property
    def direction(self):
        return self._direction  # pragma: no cover

    @direction.setter
    def direction(self, value):
        log.info("Setting direction to : %s", value)
        self._direction = value

        self._regenerate_base()

    def _regenerate_base(self):
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
        """
        Get target data and set its name in the corresponding lineEdit.
        :return:
        """
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

    def symmetrize(self):
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
        self.mesh_modifier.symmetrize(
            base_table,
            target_table,
            vertex_selection=vertex_selection,
            percentage=self._percentage,
        )

    def flip(self):
        target = mc.ls(sl=True)[0]
        if not target:
            log.error("Unable to flip, no target selected.")
            return
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
        self.mesh_modifier.flip(
            base_table,
            target_table,
            vertex_selection=vertex_selection,
            percentage=self._percentage,
        )

    def extract_axes(self):
        target = mc.ls(sl=True)[0]
        if not target:
            log.error("Unable to extract axes, no target selected.")
            return
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
        self.mesh_modifier.extract_axes(
            base_table, target_table,
        )

    def revert_to_base(self):
        """
        Revert selected mesh or vertices to base from the current value, using
        vertices selection (if one has been stored or is active) or on the whole
        mesh.

        """
        target = mc.ls(sl=True)[0]
        if not target:
            log.error("Unable to revert to base, no target selected.")
            return
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
        self.mesh_modifier.revert_to_base(
            base_table,
            target_table,
            vertex_selection=vertex_selection,
            percentage=self._percentage,
        )

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
            self.mesh_modifier.bake_difference(
                base_table,
                target_table,
                vertex_selection=self.vertex_selection,
                percentage=self._percentage,
                target_dag_path=target_path,
            )

    def undo(self):
        self.mesh_modifier.undo()

    def redo(self):
        self.mesh_modifier.redo()
