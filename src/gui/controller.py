import maya.api.OpenMaya as om2
from maya import cmds as mc
import logging

import domain.table
from domain import mesh_modification
from domain import selection
from gui import signal
from domain import table


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Controller(object):
    def __init__(self):
        log.info("Initializing controller")
        # Attributes
        self.get_vertex_selection(reset=True)

        # TODO : vertex selection should probably be extracted in its own object
        #  to make it easier to work with
        self.vtcs_selection = selection.VertexSelection(from_list=())

        self.mesh_modifier = mesh_modification.MeshModifier()

        self.are_vertices_stored = False
        self._percentage = 100
        self.space = om2.MSpace.kObject
        self.base_table: domain.table.GeometryTable = None
        self.target_table: domain.table.GeometryTable = None

        # Signals
        self.set_base = signal.Signal()
        self.set_target = signal.Signal()

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, value):
        """
        :param value: percentage to use for deforming actions.
        """
        self._percentage = value

    def get_base(self):
        """
        Get base data and set its name in the corresponding lineEdit.
        :return:
        """
        mesh = mc.ls(sl=True)[0]
        self.base_table = table.GeometryTable(mesh)
        self.set_base.emit(mesh)

    def get_target(self):
        """
        Get target data and set its name in the corresponding lineEdit.
        :return:
        """
        mesh = mc.ls(sl=True)[0]
        self.target_table = table.GeometryTable(mesh)
        self.set_target.emit(mesh)

    def get_vertex_selection(self, reset=False):
        """Get the current selection of vertices and set it.

        :param reset: Set whether the currently stored selection should be set
        to an empty selection.
        :type reset: bool
        """
        if reset:
            self.vtcs_selection = selection.VertexSelection(from_list=())
        else:
            self.vtcs_selection = selection.VertexSelection()
            log.info("Selection is %s", self.vtcs_selection)

        if len(self.vtcs_selection.indices) > 0:
            self.are_vertices_stored = True
        else:
            self.are_vertices_stored = False

    def select_stored_vertices(self):
        self.vtcs_selection.select()

    def symmetrize(self):
        target = mc.ls(sl=True)[0]
        if not target:
            log.error("Unable to symmetrize, no target selected.")
            return
        base_table = self.base_table
        if not base_table:
            log.error("Unable to symmetrize, no base defined.")
            return
        vertex_selection = selection.VertexSelection()
        target_table = table.GeometryTable(target)
        self.mesh_modifier.symmetrize(
            base_table,
            target_table,
            selected_vertices_indices=vertex_selection,
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
        vertex_selection = selection.VertexSelection()
        target_table = table.GeometryTable(target)
        self.mesh_modifier.flip(
            base_table,
            target_table,
            selected_vertices_indices=vertex_selection,
            percentage=self._percentage,
        )

    def extract_axes(self):
        target = mc.ls(sl=True)[0]
        if not target:
            log.error("Unable to flip, no target selected.")
            return
        base_table = self.base_table
        if not base_table:
            log.error("Unable to flip, no base defined.")
            return
        target_table = table.GeometryTable(target)
        self.mesh_modifier.extract_axes(
            base_table,
            target_table,
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
        vertex_selection = selection.VertexSelection()
        target_table = table.GeometryTable(target)
        self.mesh_modifier.revert_to_base(
            base_table,
            target_table,
            selected_vertices_indices=vertex_selection,
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
        vertex_selection = selection.VertexSelection()
        for target_path in target_paths:
            self.mesh_modifier.bake_difference(
                base_table,
                target_table,
                selected_vertices_indices=vertex_selection,
                percentage=self._percentage,
                target_dag_path=target_path
            )

    def select_non_mirrored_vertices(self):
        dag_path = self.base_table.dag_path
        non_mirrored_vertices = self.base_table.symmetry_table[1]

        if len(non_mirrored_vertices) == 0:
            log.info("Model is symmetrical, no vertices to select")
        else:
            vtcs_to_select = om2.MSelectionList()
            MItVtx = om2.MItMeshVertex(dag_path)
            while not MItVtx.isDone():
                if MItVtx.index() in non_mirrored_vertices:
                    vtcs_to_select.add((dag_path, MItVtx.currentItem()))
                MItVtx.next()
            om2.MGlobal.setActiveSelectionList(vtcs_to_select)

    def undo(self):
        self.mesh_modifier.undo()

    def redo(self):
        self.mesh_modifier.redo()

