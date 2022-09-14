import maya.api.OpenMaya as om2
from maya import cmds as mc
import logging

import domain.table
from domain import selection, mesh_modification
from domain import table


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Controller(object):
    def __init__(self):
        log.info("Initializing controller")
        # Attributes
        self.get_vtcs_selection(reset=True)

        # TODO : vertex selection should probably be extracted in its own object
        #  to make it easier to work with
        self.sel_vtces_idcs = {"objs_path": om2.MDagPath(), "indices": om2.MIntArray()}
        self.vtcs_selection = {"objs_path": om2.MDagPath(), "indices": om2.MIntArray()}

        self.mesh_modifier = mesh_modification.MeshModifier()

        self.are_vertices_stored = False
        self._percentage = 100
        self.space = om2.MSpace.kObject
        self.base_table: domain.table.GeometryTable = None
        self.target_table: domain.table.GeometryTable = None

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

    def undo(self):
        self.mesh_modifier.undo()

    def redo(self):
        self.mesh_modifier.redo()

    def get_target(self):
        """
        Get target data and set its name in the corresponding lineEdit.
        :return:
        """
        mesh = mc.ls(sl=True)[0]
        self.target_table = table.GeometryTable(mesh)

    def get_vtcs_selection(self, reset=False):
        """Get the current selection of vertices and set it.

        :param reset: Set whether the currently stored selection should be set
        to an empty selection.
        :type reset: bool
        """
        if reset:
            self.vtcs_selection = {
                "objs_path": om2.MDagPath(),
                "indices": om2.MIntArray(),
            }
        else:
            self.vtcs_selection = selection.get_sel_vtces_idcs()

        if len(self.vtcs_selection["indices"]) > 0:
            self.are_vertices_stored = True
        else:
            self.are_vertices_stored = False

    def symmetrize(self):
        target = mc.ls(sl=True)[0]
        if not target:
            log.error("Unable to symmetrize, no target selected.")
            return
        base_table = self.base_table
        if not base_table:
            log.error("Unable to symmetrize, no base defined.")
            return
        sel_vtces_idcs = selection.get_sel_vtces_idcs()
        target_table = table.GeometryTable(target)
        self.mesh_modifier.symmetrize(
            base_table,
            target_table,
            selected_vertices_indices=sel_vtces_idcs[1],
            percentage=self._percentage,
        )

    def flip(self):
        target = mc.ls(sl=True)[0]
        if not target:
            log.error("Unable to symmetrize, no target selected.")
            return
        base_table = self.base_table
        if not base_table:
            log.error("Unable to symmetrize, no base defined.")
            return
        sel_vtces_idcs = selection.get_sel_vtces_idcs()
        target_table = table.GeometryTable(target)
        self.mesh_modifier.flip(
            base_table,
            target_table,
            selected_vertices_indices=sel_vtces_idcs[1],
            percentage=self._percentage,
        )

    def revert_to_base(self):
        """
        Revert selected mesh or vertices to base from the current value, using
        vertices selection (if one has been stored or is active) or on the whole
        mesh.

        """
        target = mc.ls(sl=True)[0]
        if not target:
            log.error("Unable to symmetrize, no target selected.")
            return
        base_table = self.base_table
        if not base_table:
            log.error("Unable to symmetrize, no base defined.")
            return
        sel_vtces_idcs = selection.get_sel_vtces_idcs()
        target_table = table.GeometryTable(target)
        self.mesh_modifier.revert_to_base(
            base_table,
            target_table,
            selected_vertices_indices=sel_vtces_idcs[1],
            percentage=self._percentage,
        )

    def select_stored_vertices(self):
        if len(self.vtcs_selection["indices"]) == 0:
            log.warning("No vertex selection stored")
        else:
            vtcs_to_select = om2.MSelectionList()
            MItVtx = om2.MItMeshVertex(self.vtcs_selection["objs_path"][0])
            while not MItVtx.isDone():
                if MItVtx.index() in self.vtcs_selection["indices"]:
                    vtcs_to_select.add(
                        (self.vtcs_selection["objs_path"][0], MItVtx.currentItem())
                    )
                MItVtx.next()
            om2.MGlobal.setActiveSelectionList(vtcs_to_select)

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
