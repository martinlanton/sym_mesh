import maya.api.OpenMaya as om2
import logging

from sym_mesh import commands
from sym_mesh.dag_path import create_MDagPath
from sym_mesh.selection import get_sel_vtces_idcs


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class MeshModifier(object):
    def __init__(self):
        # Attributes
        self.base = ""
        self.target = ""
        self.get_vtcs_selection(reset=True)

        self.base_table = {"objs_path": om2.MDagPath(), "points_pos": om2.MPointArray()}
        self.temp_base_table = {
            "objs_path": om2.MDagPath(),
            "points_pos": om2.MPointArray(),
        }
        self.target_table = {
            "objs_path": om2.MDagPath(),
            "points_pos": om2.MPointArray(),
        }
        self.current_table = {
            "objs_path": om2.MDagPath(),
            "points_pos": om2.MPointArray(),
        }
        self.sel_vtces_idcs = {"objs_path": om2.MDagPath(), "indices": om2.MIntArray()}
        self.vtcs_selection = {"objs_path": om2.MDagPath(), "indices": om2.MIntArray()}

        self.symmetry_table = dict()
        self.non_mirrored_vtcs = list()

        self.are_vertices_stored = False
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
            self.vtcs_selection = get_sel_vtces_idcs()
            if len(self.vtcs_selection["indices"]) > 0:
                self.are_vertices_stored = True
            else:
                self.are_vertices_stored = False

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

    # def revert_selected_to_base(self, revert_value=None):
    #     """
    #     Revert selected mesh or vertices to base from the registered target
    #     value, using vertices selection (if one has been stored or is active) or
    #     on the whole mesh.
    #
    #     """
    #     # Get selected vertices indices
    #     self.sel_vtces_idcs = self.get_sel_vtces_idcs()
    #     # If no vertices are currently selected
    #     if self.sel_vtces_idcs["indices"].__len__() == 0:
    #         # If a selection is stored
    #         if self.vtcs_selection["indices"].__len__() > 0:
    #             # Replace indices using stored selection
    #             self.sel_vtces_idcs["indices"] = self.vtcs_selection["indices"]
    #
    #     # Update revert value
    #     if revert_value is not None:
    #         self._revert_value = revert_value
    #
    #     for dag_path in self.sel_vtces_idcs["objs_path"]:
    #         # Update current mesh table
    #         self.current_table = self.get_selected_mesh_points(dag_path)
    #
    #         log.debug(self.current_table["objs_path"].fullPathName())
    #
    #         self.undo_table = {
    #             "objs_path": self.current_table["objs_path"].fullPathName(),
    #             "points_pos": self.current_table["points_pos"],
    #         }
    #
    #         self.undo.append(self.undo_table)
    #
    #         # Check if base is registered
    #         if not self.base_table["points_pos"]:
    #             log.error("No base selected")
    #             return
    #         # Check if target is registered
    #         elif not self.target_table["points_pos"]:
    #             log.info("No target registered")
    #             return
    #         # Check if something is selected
    #         elif not self.sel_vtces_idcs["objs_path"]:
    #             log.info("Nothing is selected")
    #             return
    #         # Revert to base
    #         else:
    #             self.revert_to_base(
    #                 self.base_table["points_pos"],
    #                 self.target_table["points_pos"],
    #                 self.sel_vtces_idcs["indices"],
    #                 self._revert_value,
    #                 dag_path,
    #                 self.space,
    #             )

    # def revert_selected_to_base_live(self, revert_value=None):
    #     """
    #     Revert selected mesh or vertices to base from the current value, using
    #     vertices selection (if one has been stored or is active) or on the whole
    #     mesh.
    #
    #     """
    #     # Get selected vertices indices
    #     self.sel_vtces_idcs = self.get_sel_vtces_idcs()
    #     # If no vertices are currently selected
    #     if self.sel_vtces_idcs["indices"].__len__() == 0:
    #         # If a selection is stored
    #         if self.vtcs_selection["indices"].__len__() > 0:
    #             # Replace indices using stored selection
    #             self.sel_vtces_idcs["indices"] = self.vtcs_selection["indices"]
    #
    #     # Update revert value
    #     if revert_value is not None:
    #         self._revert_value = revert_value
    #
    #     for dag_path in self.sel_vtces_idcs["objs_path"]:
    #         # Update current mesh table
    #         self.current_table = self.get_selected_mesh_points(dag_path)
    #         self.temp_base_table = self.get_selected_mesh_points(
    #             self.base_table["objs_path"]
    #         )
    #
    #         self.undo_table = {
    #             "objs_path": self.current_table["objs_path"].fullPathName(),
    #             "points_pos": self.current_table["points_pos"],
    #         }
    #
    #         self.undo.append(self.undo_table)
    #
    #         # Check if base is registered
    #         if not self.temp_base_table["points_pos"]:
    #             log.info("No base selected")
    #             return
    #         # Check if something is selected
    #         elif not self.sel_vtces_idcs["objs_path"]:
    #             log.info("Nothing is selected")
    #             return
    #         # Revert to base
    #         else:
    #             self.revert_to_base(
    #                 self.temp_base_table["points_pos"],
    #                 self.current_table["points_pos"],
    #                 self.sel_vtces_idcs["indices"],
    #                 self._revert_value,
    #                 dag_path,
    #                 self.space,
    #             )

    # def bake_difference_on_selected(self):
    #     """
    #     Bake the difference between base and target on the selected meshes using
    #     vertices selection (if one has been stored or is active) or on the whole
    #     mesh.
    #
    #     """
    #     # Get selected vertices indices
    #     self.sel_vtces_idcs = self.get_sel_vtces_idcs()
    #     # If no vertices are currently selected
    #     if self.sel_vtces_idcs["indices"].__len__() == 0:
    #         # If a selection is stored
    #         if self.vtcs_selection["indices"].__len__() > 0:
    #             # Replace indices using stored selection
    #             self.sel_vtces_idcs["indices"] = self.vtcs_selection["indices"]
    #
    #     for dag_path in self.sel_vtces_idcs["objs_path"]:
    #         # Update current mesh table
    #         self.current_table = self.get_selected_mesh_points(dag_path)
    #
    #         log.debug(self.current_table["objs_path"].fullPathName())
    #
    #         self.undo_table = {
    #             "objs_path": self.current_table["objs_path"].fullPathName(),
    #             "points_pos": self.current_table["points_pos"],
    #         }
    #
    #         self.undo.append(self.undo_table)
    #
    #         # Check if base is registered
    #         if not self.base_table["points_pos"]:
    #             log.info("No base selected")
    #             return
    #         # Check if target is registered
    #         elif not self.target_table["points_pos"]:
    #             log.info("No target registered")
    #             return
    #         # Check if something is selected
    #         elif not self.sel_vtces_idcs["objs_path"]:
    #             log.info("Nothing is selected")
    #             return
    #         # Revert to base
    #         else:
    #             self.bake_difference(
    #                 self.base_table["points_pos"],
    #                 self.target_table["points_pos"],
    #                 self.current_table["points_pos"],
    #                 self.sel_vtces_idcs["indices"],
    #                 dag_path,
    #                 self.space,
    #             )
    #
    # def select_stored_vertices(self):
    #     if len(self.vtcs_selection["indices"]) == 0:
    #         log.warning("No vertex selection stored")
    #     else:
    #         vtcs_to_select = om2.MSelectionList()
    #         MItVtx = om2.MItMeshVertex(self.vtcs_selection["objs_path"][0])
    #         while not MItVtx.isDone():
    #             if MItVtx.index() in self.vtcs_selection["indices"]:
    #                 vtcs_to_select.add(
    #                     (self.vtcs_selection["objs_path"][0], MItVtx.currentItem())
    #                 )
    #             MItVtx.next()
    #         om2.MGlobal.setActiveSelectionList(vtcs_to_select)
    #
    # def select_non_mirrored_vertices(self):
    #     if len(self.non_mirrored_vtcs) == 0:
    #         log.info("Model is symmetrical, no vertices to select")
    #     else:
    #         vtcs_to_select = om2.MSelectionList()
    #         MItVtx = om2.MItMeshVertex(self.base_table["objs_path"])
    #         while not MItVtx.isDone():
    #             if MItVtx.index() in self.non_mirrored_vtcs:
    #                 vtcs_to_select.add(
    #                     (self.base_table["objs_path"], MItVtx.currentItem())
    #                 )
    #             MItVtx.next()
    #         om2.MGlobal.setActiveSelectionList(vtcs_to_select)

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
