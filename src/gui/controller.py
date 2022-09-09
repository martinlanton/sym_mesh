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

        self.sel_vtces_idcs = {"objs_path": om2.MDagPath(), "indices": om2.MIntArray()}
        self.vtcs_selection = {"objs_path": om2.MDagPath(), "indices": om2.MIntArray()}

        self.symmetry_table = dict()
        self.non_mirrored_vtcs = list()

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

    def symmetrize(self):
        target = mc.ls(sl=True)[0]
        if not target:
            log.error("Unable to symmetrize, no target selected.")
            return
        base_table = self.base_table
        if not base_table:
            log.error("Unable to symmetrize, no base defined.")
            return
        target_table = table.GeometryTable(target)
        self.mesh_modifier.symmetrize(base_table, target_table, percentage=self._percentage)

    def get_base(self):
        """
        Get base data and set its name in the corresponding lineEdit.
        :return:
        """
        mesh = mc.ls(sl=True)[0]
        self.base_table = table.GeometryTable(mesh)

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
            self.are_vertices_stored = False
        else:
            self.vtcs_selection = selection.get_sel_vtces_idcs()
            if len(self.vtcs_selection["indices"]) > 0:
                self.are_vertices_stored = True
            else:
                self.are_vertices_stored = False

    def revert_selected_to_base(self, revert_value=None):
        """
        Revert selected mesh or vertices to base from the registered target
        value, using vertices selection (if one has been stored or is active) or
        on the whole mesh.

        """
        # Get selected vertices indices
        self.sel_vtces_idcs = selection.get_sel_vtces_idcs()
        # If no vertices are currently selected
        if self.sel_vtces_idcs["indices"].__len__() == 0:
            # If a selection is stored
            if self.vtcs_selection["indices"].__len__() > 0:
                # Replace indices using stored selection
                self.sel_vtces_idcs["indices"] = self.vtcs_selection["indices"]

        # Update revert value
        if revert_value is not None:
            self._revert_value = revert_value

        for dag_path in self.sel_vtces_idcs["objs_path"]:
            # Update current mesh table
            self.current_table = selection.get_points_positions(dag_path)

            log.debug(self.current_table["objs_path"].fullPathName())

            self.undo_table = {
                "objs_path": self.current_table["objs_path"].fullPathName(),
                "points_pos": self.current_table["points_pos"],
            }

            self.undo.append(self.undo_table)

            # Check if base is registered
            if not self.base_table["points_pos"]:
                log.error("No base selected")
                return
            # Check if target is registered
            elif not self.target_table["points_pos"]:
                log.info("No target registered")
                return
            # Check if something is selected
            elif not self.sel_vtces_idcs["objs_path"]:
                log.info("Nothing is selected")
                return
            # Revert to base
            else:
                self.revert_to_base(
                    self.base_table["points_pos"],
                    self.target_table["points_pos"],
                    self.sel_vtces_idcs["indices"],
                    self._revert_value,
                    dag_path,
                    self.space,
                )

    def revert_selected_to_base_live(self, revert_value=None):
        """
        Revert selected mesh or vertices to base from the current value, using
        vertices selection (if one has been stored or is active) or on the whole
        mesh.

        """
        # Get selected vertices indices
        self.sel_vtces_idcs = selection.get_sel_vtces_idcs()
        # If no vertices are currently selected
        if self.sel_vtces_idcs["indices"].__len__() == 0:
            # If a selection is stored
            if self.vtcs_selection["indices"].__len__() > 0:
                # Replace indices using stored selection
                self.sel_vtces_idcs["indices"] = self.vtcs_selection["indices"]

        # Update revert value
        if revert_value is not None:
            self._revert_value = revert_value

        for dag_path in self.sel_vtces_idcs["objs_path"]:
            # Update current mesh table
            self.current_table = selection.get_points_positions(dag_path)
            self.temp_base_table = selection.get_points_positions(
                self.base_table["objs_path"]
            )

            self.undo_table = {
                "objs_path": self.current_table["objs_path"].fullPathName(),
                "points_pos": self.current_table["points_pos"],
            }

            self.undo.append(self.undo_table)

            # Check if base is registered
            if not self.temp_base_table["points_pos"]:
                log.info("No base selected")
                return
            # Check if something is selected
            elif not self.sel_vtces_idcs["objs_path"]:
                log.info("Nothing is selected")
                return
            # Revert to base
            else:
                self.revert_to_base(
                    self.temp_base_table["points_pos"],
                    self.current_table["points_pos"],
                    self.sel_vtces_idcs["indices"],
                    self._revert_value,
                    dag_path,
                    self.space,
                )

    def bake_difference_on_selected(self):
        """
        Bake the difference between base and target on the selected meshes using
        vertices selection (if one has been stored or is active) or on the whole
        mesh.

        """
        # Get selected vertices indices
        self.sel_vtces_idcs = selection.get_sel_vtces_idcs()
        # If no vertices are currently selected
        if self.sel_vtces_idcs["indices"].__len__() == 0:
            # If a selection is stored
            if self.vtcs_selection["indices"].__len__() > 0:
                # Replace indices using stored selection
                self.sel_vtces_idcs["indices"] = self.vtcs_selection["indices"]

        for dag_path in self.sel_vtces_idcs["objs_path"]:
            # Update current mesh table
            self.current_table = selection.get_points_positions(dag_path)

            log.debug(self.current_table["objs_path"].fullPathName())

            self.undo_table = {
                "objs_path": self.current_table["objs_path"].fullPathName(),
                "points_pos": self.current_table["points_pos"],
            }

            self.undo.append(self.undo_table)

            # Check if base is registered
            if not self.base_table["points_pos"]:
                log.info("No base selected")
                return
            # Check if target is registered
            elif not self.target_table["points_pos"]:
                log.info("No target registered")
                return
            # Check if something is selected
            elif not self.sel_vtces_idcs["objs_path"]:
                log.info("Nothing is selected")
                return
            # Revert to base
            else:
                self.bake_difference(
                    self.base_table["points_pos"],
                    self.target_table["points_pos"],
                    self.current_table["points_pos"],
                    self.sel_vtces_idcs["indices"],
                    dag_path,
                    self.space,
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
        if len(self.non_mirrored_vtcs) == 0:
            log.info("Model is symmetrical, no vertices to select")
        else:
            vtcs_to_select = om2.MSelectionList()
            MItVtx = om2.MItMeshVertex(self.base_table["objs_path"])
            while not MItVtx.isDone():
                if MItVtx.index() in self.non_mirrored_vtcs:
                    vtcs_to_select.add(
                        (self.base_table["objs_path"], MItVtx.currentItem())
                    )
                MItVtx.next()
            om2.MGlobal.setActiveSelectionList(vtcs_to_select)
