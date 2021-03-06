import maya.api.OpenMaya as om2
import logging
from pprint import pformat

from sym_mesh.dag_path import create_MDagPath

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

    def get_base_mesh(self, mesh):
        """Set the specified mesh as base mesh.

        :param mesh: mesh to set as base mesh
        :type mesh: str or maya.api.OpenMaya.MDagPath

        """
        if not isinstance(mesh, om2.MDagPath):
            mesh = create_MDagPath(mesh)
        self.base = mesh
        self.base_table = self.get_selected_mesh_points(mesh)

    def get_base(self):
        """
        Get base data and set its name in the corresponding lineEdit.

        """
        # Get data
        self.base_table = self.get_selected_mesh_points()
        self.symmetry_table, self.non_mirrored_vtcs = self.get_symmetry_table(
            self.base_table
        )

        # Get name
        self.base = self.base_table["objs_path"].partialPathName()

        self.select_non_mirrored_vertices()

    def get_target(self):
        """
        Get target data and set its name in the corresponding lineEdit.

        """
        # Get data
        self.target_table = self.get_selected_mesh_points()

        # Get name
        self.target = self.target_table["objs_path"].partialPathName()

    def get_symmetry_table(self, axis="x", threshold=0.001):
        """
        Create symmetry table base on symmetry axis and threshold

        :param axis: axis to use for mirroring
        :type axis: basestring

        :param threshold: number to use to round point values
        :type threshold: float

        :return: symmetry table
        :rtype: dict
        """
        base_tbl = self.base_table

        base_points = base_tbl["points_pos"]
        axis_idcs = {"x": 0, "y": 1, "z": 2}
        axis_idx = axis_idcs[axis]

        # Todo: replace with threshold method
        if threshold > 1:
            threshold_nb = -len(str(threshold).split(".")[0])
        else:
            threshold_nb = len(str(threshold).split(".")[1])

        non_mirrored_table = list()
        symmetry_table = dict()

        log.info(base_points.__len__())

        check_table = dict()

        MItVtx = om2.MItMeshVertex(base_tbl["objs_path"])
        while not MItVtx.isDone():
            position = (
                round(MItVtx.position()[0], threshold_nb),
                round(MItVtx.position()[1], threshold_nb),
                round(MItVtx.position()[2], threshold_nb),
            )
            check_table[position] = MItVtx.index()
            position_to_check = list(position)
            position_to_check[axis_idx] = -position_to_check[axis_idx]
            position_to_check = tuple(position_to_check)

            if position_to_check in check_table:
                symmetry_table[MItVtx.index()] = check_table[position_to_check]
                symmetry_table[check_table[position_to_check]] = MItVtx.index()

            MItVtx.next()

        if len(symmetry_table) < base_points.__len__():
            log.info(
                "Not all vertices are symmetrical,"
                " mirroring might not work as expected"
            )
        else:
            log.info("Model is symmetrical")

        MItVtx = om2.MItMeshVertex(base_tbl["objs_path"])
        while not MItVtx.isDone():
            if MItVtx.index() not in symmetry_table:
                non_mirrored_table.append(MItVtx.index())

            MItVtx.next()

        log.debug(len(symmetry_table))
        log.debug(symmetry_table)

        return symmetry_table, non_mirrored_table

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
            self.vtcs_selection = self.get_sel_vtces_idcs()
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

    def revert_selected_to_base(self, revert_value=None):
        """
        Revert selected mesh or vertices to base from the registered target
        value, using vertices selection (if one has been stored or is active) or
        on the whole mesh.

        """
        # Get selected vertices indices
        self.sel_vtces_idcs = self.get_sel_vtces_idcs()
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
            self.current_table = self.get_selected_mesh_points(dag_path)

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
        self.sel_vtces_idcs = self.get_sel_vtces_idcs()
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
            self.current_table = self.get_selected_mesh_points(dag_path)
            self.temp_base_table = self.get_selected_mesh_points(
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
        self.sel_vtces_idcs = self.get_sel_vtces_idcs()
        # If no vertices are currently selected
        if self.sel_vtces_idcs["indices"].__len__() == 0:
            # If a selection is stored
            if self.vtcs_selection["indices"].__len__() > 0:
                # Replace indices using stored selection
                self.sel_vtces_idcs["indices"] = self.vtcs_selection["indices"]

        for dag_path in self.sel_vtces_idcs["objs_path"]:
            # Update current mesh table
            self.current_table = self.get_selected_mesh_points(dag_path)

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
    def get_sel_vtces_idcs():
        """
        Get the indices of the selected vertices.

        :return: DagPath of the current mesh, indices of the selected vertices
        :rtype: MDagPathArray, MIntArray
        """
        # Get current selection
        selection_list = om2.MGlobal.getActiveSelectionList()
        log.info("Selection list is : %s" % selection_list)

        # Get the dag dir_path and components of the first item in the list
        if selection_list.length() > 0:
            obj_dag_path, components = selection_list.getComponent(0)
        else:
            log.warning("No selection found.")
            return {"objs_path": om2.MDagPath(), "indices": om2.MIntArray()}

        # Initialize MDagPathArray
        dag_path_list = om2.MDagPathArray()

        # If no vertices selected
        if components.isNull():
            # Empty list of vertices
            selected_vertices_indices = om2.MIntArray()

            # Create iterator
            sel_iter = om2.MItSelectionList(selection_list)
            # Create list of dagPath of selected objects
            while not sel_iter.isDone():
                dag_path_list.append(sel_iter.getDagPath())
                sel_iter.next()
        # If vertices are selected
        else:

            dag_path_list.append(selection_list.getDagPath(0))
            # Query vertex indices
            fn_components = om2.MFnSingleIndexedComponent(components)
            # Create an MIntArray with the vertex indices
            selected_vertices_indices = fn_components.getElements()

        return {"objs_path": dag_path_list, "indices": selected_vertices_indices}

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

        :return:
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
        for i in range(base_point_array.__len__()):
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
    def bake_difference(base_tbl, tgt_tbl, current_tbl, sel_vtcs_idcs, dag_path, space):
        """
        Bake the difference between 2 mesh on a list of vertices on a selection
        of meshes.

        :param base_tbl: positions of the points of the base mesh
        :type base_tbl: MPointArray

        :param tgt_tbl: positions of the points of the target mesh
        :type tgt_tbl: MPointArray

        :param current_tbl: positions of the points of the current mesh
        :type current_tbl: MPointArray

        :param sel_vtcs_idcs: indices of the selected points on the target mesh
        :type sel_vtcs_idcs: MIntArray

        :param dag_path: MDagPathArray of targets
        :type dag_path: MDagPathArray

        :param space: space in which operate the deformation (object or world)
        :type space: constant

        :return:
        """
        # Create new table for destination position
        destination_table = om2.MPointArray()

        # Init MFnMesh
        tgt_mesh = om2.MFnMesh(dag_path)

        # Loop in MPointArray
        for i in range(base_tbl.__len__()):
            # If the current point is also in selection
            if i in sel_vtcs_idcs or sel_vtcs_idcs.__len__() == 0:
                # Modify new position
                destination_table.append(current_tbl[i] + (tgt_tbl[i] - base_tbl[i]))
            # If the current point is not selected
            else:
                # Do nothing
                destination_table.append(current_tbl[i])

        # Modify points position using the new coordinates
        tgt_mesh.setPoints(destination_table, space)
