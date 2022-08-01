import maya.api.OpenMaya as om2
import logging
from pprint import pformat

from sym_mesh.dag_path import create_MDagPath
from sym_mesh.selection import get_selected_mesh_points, get_sel_vtces_idcs

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
        self.undo = list()
        self.undo_table = dict()

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

    def undo_last_action(self):
        """
        Undo the last move stored.

        """
        if len(self.undo) > 0:
            undo = self.undo.pop(-1)
        else:
            log.error("No undo action to undo.")
            return

        dag_path = create_MDagPath(undo["objs_path"])

        tgt_mesh = om2.MFnMesh(dag_path)

        tgt_mesh.setPoints(undo["points_pos"], om2.MSpace.kObject)

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

    @staticmethod
    def get_selected_mesh_points(obj_dag_path=None):
        """
        Get the position of every point of the selected mesh.

        :return: dag dir_path of the object, position of the points
        :rtype: MDagPath, MPointArray
        """
        if not obj_dag_path:
            # Get current selection
            selection_list = om2.MGlobal.getActiveSelectionList()

            # Get the dag dir_path of the first item in the selection list
            obj_dag_path = selection_list.getDagPath(0)

        # Query vertex position
        # create a Mesh functionSet from our dag object
        mfn_object = om2.MFnMesh(obj_dag_path)

        points = mfn_object.getPoints(space=om2.MSpace.kObject)

        return {"objs_path": obj_dag_path, "points_pos": points}

    @staticmethod
    def revert_to_base(
        base_table,
        current_table,
        sel_vtcs_idcs=(),
        percentage=100,
        space=om2.MSpace.kObject,
    ):
        """
        Revert selected vertices on the target mesh to the base position.

        :param base_table: positions of the points of the base mesh
        :type base_table: sym_mesh.table.GeometryTable

        :param current_table: positions of the points of the current mesh
        :type current_table: MPointArray

        :param sel_vtcs_idcs: indices of the selected points on the target mesh
        :type sel_vtcs_idcs: MIntArray

        :param percentage: percentage used for the revert to base function. This
        is a value from 0 to 100, a value of 100 means we're reverting the
        position of the base, a value of 0 means we're staying at the current
        position.
        :type percentage: int

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        base_point_array = base_table.point_array
        log.info("base_point_array :\n%s", pformat(base_point_array))
        current_point_array = current_table.point_array
        log.info("current_point_array :\n%s", pformat(current_point_array))
        dag_path = current_table.dag_path

        # Create new table for destination position
        destination_table = om2.MPointArray()

        # Init MFnMesh
        tgt_mesh_functionset = om2.MFnMesh(dag_path)

        # Loop in MPointArray
        for i in range(base_point_array.__len__()):
            log.info(i)
            # If the current point is also in selection
            if i in sel_vtcs_idcs or sel_vtcs_idcs.__len__() == 0:
                # Modify new position
                base_position = base_point_array[i]
                new_position = base_position + (
                    (current_point_array[i] - base_position)
                    * ((100 - percentage) / 100.00)
                )
                log.info("New position : %s", new_position)
                destination_table.append(new_position)
            # If the current point is not selected
            else:
                # Do nothing
                destination_table.append(current_point_array[i])

        # Modify points position using the new coordinates
        tgt_mesh_functionset.setPoints(destination_table, space)

    # TODO : this needs to be tested
    @staticmethod
    def symmetrize(
        base_table,
        current_table,
        sel_vtcs_idcs=(),
        percentage=100,
        space=om2.MSpace.kObject,
    ):
        """
        Symmetrize selected vertices on the target mesh.

        :param base_table: positions of the points of the base mesh
        :type base_table: sym_mesh.table.GeometryTable

        :param current_table: positions of the points of the current mesh
        :type current_table: sym_mesh.table.GeometryTable

        :param sel_vtcs_idcs: indices of the selected points on the target mesh
        :type sel_vtcs_idcs: MIntArray

        :param percentage: percentage used for the revert to base function
        :type percentage: int

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        axis = base_table.axis
        axis_indices = {"x": 0, "y": 1, "z": 2}
        axis_index = axis_indices[axis]
        # Create new table for destination position
        destination_point_array = om2.MPointArray()

        dag_path = current_table.dag_path
        current_point_array = current_table.point_array
        base_point_array = base_table.point_array
        symmetry_table = base_table.symmetry_table[0]
        log.info("Symmetry table is : %s", symmetry_table)

        # Init MFnMesh
        tgt_mesh = om2.MFnMesh(dag_path)

        # Loop in MPointArray
        for i in range(len(base_point_array)):
            # If the current point is also in selection
            current_position = symmetry_position = current_point_array[i]
            if (
                i in sel_vtcs_idcs or sel_vtcs_idcs.__len__() == 0
            ) and i in symmetry_table:
                # Modify new position
                source_index = symmetry_table[i]
                target_vertex_position = current_point_array[source_index]
                print(type(target_vertex_position))
                symmetry_position = list(target_vertex_position)
                symmetry_position[axis_index] = -target_vertex_position[axis_index]
                symmetry_position = om2.MPoint(symmetry_position)
                log.info(
                    "Mirroring position of vtx %s from vtx %s. Current position : %s, target position : %s",
                    i,
                    source_index,
                    current_position,
                    symmetry_position,
                )
                symmetry_position = current_position + (
                    (symmetry_position - current_position) * (percentage / 100.00)
                )
            else:
                log.info("Not mirroring the position of vtx %s", i)

            log.info(
                "Modifying position from %s to %s", current_position, symmetry_position
            )
            destination_point_array.append(symmetry_position)

        # Modify points position using the new coordinates
        tgt_mesh.setPoints(destination_point_array, space)

    @staticmethod
    def bake_difference(base_tbl, tgt_tbl, sel_vtcs_idcs=(), target_dag_path=None, space=om2.MSpace.kObject):
        """
        Bake the difference between 2 mesh on a list of vertices on a selection
        of meshes.

        :param base_tbl: GeometryTable of the base geometry
        :type base_tbl: sym_mesh.table.GeometryTable

        :param tgt_tbl: GeometryTable of the target geometry
        :type tgt_tbl: sym_mesh.table.GeometryTable

        :param sel_vtcs_idcs: indices of the selected points on the target mesh
        :type sel_vtcs_idcs: MIntArray

        :param target_dag_path: MDagPath of the target
        :type target_dag_path: MDagPath or str

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        if isinstance(target_dag_path, str):
            target_dag_path = create_MDagPath(target_dag_path)

        # Create new table for destination position
        destination_table = om2.MPointArray()
        current_tbl = get_selected_mesh_points(target_dag_path)
        target_point_array = tgt_tbl.point_array
        base_point_array = base_tbl.point_array

        # Init MFnMesh
        tgt_mesh = om2.MFnMesh(target_dag_path)

        # Loop in MPointArray
        for i in range(len(base_point_array)):
            # If the current point is also in selection
            if i in sel_vtcs_idcs or sel_vtcs_idcs.__len__() == 0:
                # Modify new position
                destination_table.append(current_tbl[i] + (target_point_array[i] - base_point_array[i]))
            # If the current point is not selected
            else:
                # Do nothing
                destination_table.append(current_tbl[i])

        # Modify points position using the new coordinates
        tgt_mesh.setPoints(destination_table, space)

