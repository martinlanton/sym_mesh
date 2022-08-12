import logging
from pprint import pformat

from maya.api import OpenMaya as om2

from sym_mesh.dag_path import create_MDagPath
from sym_mesh.selection import get_selected_mesh_points, get_sel_vtces_idcs

log = logging.getLogger(__name__)


class ExtractAxesCommand(object):
    def __init__(self, base_table, target_table):
        self.result = self.extract_axes(base_table, target_table)

    def extract_axes(self, base_table, target_table):
        """Extract deltas between target table and base table on a new geometry.

        :param base_table:
        :type base_table: sym_mesh.table.GeometryTable

        :param target_table:
        :type target_table: sym_mesh.table.GeometryTable

        :return: names of the newly created geometries
        :rtype: str, str, str
        """
        base_dag_path = base_table.dag_path
        target_name = target_table.dag_path.fullPathName().split("|")[-1]
        base_point_array = base_table.point_array
        target_point_array = target_table.point_array

        pathes = list()

        for i, axis in enumerate(["x", "y", "z"]):
            dag_path = self.duplicate_mesh(base_dag_path, target_name, suffix=axis)
            path = dag_path.fullPathName()
            pathes.append(path)

            # Init MFnMesh
            destination_table = om2.MPointArray()
            tgt_mesh_functionset = om2.MFnMesh(dag_path)

            # Loop in MPointArray
            for j in range(len(base_point_array)):
                base_point = base_point_array[j]
                target_point = target_point_array[j]
                new_point = list(base_point)
                new_point[i] = target_point[i]
                destination_table.append(new_point)

            # Modify points position using the new coordinates
            tgt_mesh_functionset.setPoints(destination_table, om2.MSpace.kObject)

        dag_path = self.duplicate_mesh(base_dag_path, target_name, suffix="extracted")
        pathes.append(dag_path.fullPathName())

        return pathes

    def duplicate_mesh(self, dag_path, name, suffix=""):
        """Duplicate the mesh at the selected dag path and rename it with the specified name.

        :param dag_path: dag path of the mesh to duplicate.
        :type dag_path: maya.api.OpenMaya.MDagPath

        :param name: name to give to the new geometry
        :type name: str

        :param suffix: suffix to add to the end of the new name
        :type suffix: str

        :return: dag path of the new mesh
        :rtype: maya.api.OpenMaya.MDagPath
        """
        mesh_function_set = om2.MFnMesh(dag_path)
        mesh = mesh_function_set.duplicate()
        duplicate_function_set = om2.MFnDagNode(mesh)
        dag_path = duplicate_function_set.getPath()
        new_x_path = self.get_new_name(name, dag_path, suffix=suffix)
        dag_modifier = om2.MDagModifier()
        dag_modifier.renameNode(mesh, new_x_path)
        dag_modifier.doIt()
        return dag_path

    def get_new_name(self, target_name, dag_path, suffix=""):
        """Renamed the dag object at the specific dag path with the specified
        name and suffix.

        :param target_name: name to give to the object.
        :type target_name: str

        :param dag_path: dag path of the object to rename.
        :type dag_path: maya.api.OpenMaya.MDagPath

        :param suffix: suffix to add at the end of the new name.
        :type suffix: str

        :return: new long name to give to the object
        :rtype: str
        """
        path = dag_path.fullPathName()
        new_path = path.split("|")[:-1]
        new_path.append("{}_{}".format(target_name, suffix))
        new_path = "|".join(new_path)
        return new_path


class BakeDifferenceCommand(object):
    def __init__(
        self,
        base_table,
        target_table,
        selected_vertices_indices=(),
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

        :param target_dag_path: MDagPath of the target
        :type target_dag_path: maya.api.OpenMaya.MDagPath or str

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        self.space = space
        self.path = target_dag_path
        self.current_point_array = get_selected_mesh_points(create_MDagPath(target_dag_path))
        self.undo_action = self.current_point_array
        self.result = self.bake_difference(
            base_table, target_table, selected_vertices_indices, target_dag_path
        )
        self.redo_action = self.result

    def bake_difference(
        self,
        base_table,
        target_table,
        selected_vertices_indices=(),
        target_dag_path=None,
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

        :param target_dag_path: MDagPath of the target
        :type target_dag_path: maya.api.OpenMaya.MDagPath or str
        """
        if not isinstance(target_dag_path, om2.MDagPath):
            target_dag_path = create_MDagPath(target_dag_path)

        # Create new table for destination position
        destination_table = om2.MPointArray()
        target_point_array = target_table.point_array
        base_point_array = base_table.point_array

        # Init MFnMesh
        tgt_mesh_functionset = om2.MFnMesh(target_dag_path)

        # Loop in MPointArray
        for i in range(len(base_point_array)):
            # If the current point is also in selection
            if (
                i in selected_vertices_indices
                or selected_vertices_indices.__len__() == 0
            ):
                # Modify new position
                destination_table.append(
                    self.current_point_array[i]
                    + (target_point_array[i] - base_point_array[i])
                )
            # If the current point is not selected
            else:
                # Do nothing
                destination_table.append(self.current_point_array[i])

        # Modify points position using the new coordinates
        tgt_mesh_functionset.setPoints(destination_table, self.space)

        return destination_table

    def undo(self):
        path = create_MDagPath(self.path)
        tgt_mesh_functionset = om2.MFnMesh(path)
        tgt_mesh_functionset.setPoints(self.undo_action, self.space)

    def redo(self):
        path = create_MDagPath(self.path)
        tgt_mesh_functionset = om2.MFnMesh(path)
        tgt_mesh_functionset.setPoints(self.redo_action, self.space)


class SymmetrizeCommand(object):
    def __init__(
        self,
        base_table,
        current_table,
        selected_vertices_indices=(),
        percentage=100,
        space=om2.MSpace.kObject,
    ):
        """
        Symmetrize selected vertices on the target mesh.

        :param base_table: positions of the points of the base mesh
        :type base_table: sym_mesh.table.GeometryTable

        :param current_table: positions of the points of the current mesh
        :type current_table: sym_mesh.table.GeometryTable

        :param selected_vertices_indices: indices of the selected points on the target mesh
        :type selected_vertices_indices: maya.api.OpenMaya.MIntArray

        :param percentage: percentage used for the revert to base function
        :type percentage: int

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        self.space = space
        self.path = current_table.dag_path.getPath()
        self.undo_action = current_table.point_array
        self.result = self.symmetrize(
            base_table, current_table, selected_vertices_indices, percentage
        )
        self.redo_action = self.result

    def symmetrize(
        self,
        base_table,
        current_table,
        selected_vertices_indices=(),
        percentage=100,
    ):
        """
        Symmetrize selected vertices on the target mesh.

        :param base_table: positions of the points of the base mesh
        :type base_table: sym_mesh.table.GeometryTable

        :param current_table: positions of the points of the current mesh
        :type current_table: sym_mesh.table.GeometryTable

        :param selected_vertices_indices: indices of the selected points on the target mesh
        :type selected_vertices_indices: maya.api.OpenMaya.MIntArray

        :param percentage: percentage used for the revert to base function
        :type percentage: int
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
        log.debug("Symmetry table is : %s", symmetry_table)

        # Init MFnMesh
        tgt_mesh = om2.MFnMesh(dag_path)

        # Loop in MPointArray
        for i in range(len(base_point_array)):
            # If the current point is also in selection
            current_position = symmetry_position = current_point_array[i]
            if (
                i in selected_vertices_indices
                or selected_vertices_indices.__len__() == 0
            ) and i in symmetry_table:
                # Modify new position
                source_index = symmetry_table[i]
                target_vertex_position = current_point_array[source_index]
                symmetry_position = list(target_vertex_position)
                symmetry_position[axis_index] = -target_vertex_position[axis_index]
                symmetry_position = om2.MPoint(symmetry_position)
                log.debug(
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
                log.debug("Not mirroring the position of vtx %s", i)

            log.debug(
                "Modifying position from %s to %s", current_position, symmetry_position
            )
            destination_point_array.append(symmetry_position)

        # Modify points position using the new coordinates
        tgt_mesh.setPoints(destination_point_array, self.space)

        return destination_point_array

    def undo(self):
        path = create_MDagPath(self.path)
        tgt_mesh_functionset = om2.MFnMesh(path)
        tgt_mesh_functionset.setPoints(self.undo_action, self.space)

    def redo(self):
        path = create_MDagPath(self.path)
        tgt_mesh_functionset = om2.MFnMesh(path)
        tgt_mesh_functionset.setPoints(self.redo_action, self.space)


class RevertToBaseCommand(object):
    def __init__(
        self,
        base_table,
        current_table,
        selected_vertices_indices=(),
        percentage=100,
        space=om2.MSpace.kObject,
    ):
        """
        Revert selected vertices on the target mesh to the base position.

        :param base_table: positions of the points of the base mesh
        :type base_table: sym_mesh.table.GeometryTable

        :param current_table: positions of the points of the current mesh
        :type current_table: sym_mesh.table.GeometryTable

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
        self.space = space
        self.path = current_table.dag_path.getPath()
        self.undo_action = current_table.point_array
        self.result = self.revert_to_base(
            base_table, current_table, selected_vertices_indices, percentage
        )
        self.redo_action = self.result

    def revert_to_base(
        self,
        base_table,
        current_table,
        selected_vertices_indices=(),
        percentage=100,
    ):
        """
        Revert selected vertices on the target mesh to the base position.

        :param base_table: positions of the points of the base mesh
        :type base_table: sym_mesh.table.GeometryTable

        :param current_table: positions of the points of the current mesh
        :type current_table: sym_mesh.table.GeometryTable

        :param selected_vertices_indices: indices of the selected points on the target mesh
        :type selected_vertices_indices: maya.api.OpenMaya.MIntArray

        :param percentage: percentage used for the revert to base function. This
        is a value from 0 to 100, a value of 100 means we're reverting the
        position of the base, a value of 0 means we're staying at the current
        position.
        :type percentage: int
        """
        base_point_array = base_table.point_array
        log.debug("base_point_array :\n%s", pformat(base_point_array))
        current_point_array = current_table.point_array
        log.debug("current_point_array :\n%s", pformat(current_point_array))
        dag_path = current_table.dag_path

        # Create new table for destination position
        destination_table = om2.MPointArray()

        # Init MFnMesh
        tgt_mesh_functionset = om2.MFnMesh(dag_path)

        # Loop in MPointArray
        for i in range(base_point_array.__len__()):
            # If the current point is also in selection
            if (
                i in selected_vertices_indices
                or selected_vertices_indices.__len__() == 0
            ):
                # Modify new position
                base_position = base_point_array[i]
                new_position = base_position + (
                    (current_point_array[i] - base_position)
                    * ((100 - percentage) / 100.00)
                )
                log.debug("New position : %s", new_position)
                destination_table.append(new_position)
            # If the current point is not selected
            else:
                # Do nothing
                destination_table.append(current_point_array[i])

        # Modify points position using the new coordinates
        tgt_mesh_functionset.setPoints(destination_table, self.space)

        return destination_table

    def undo(self):
        path = create_MDagPath(self.path)
        tgt_mesh_functionset = om2.MFnMesh(path)
        tgt_mesh_functionset.setPoints(self.undo_action, self.space)

    def redo(self):
        path = create_MDagPath(self.path)
        tgt_mesh_functionset = om2.MFnMesh(path)
        tgt_mesh_functionset.setPoints(self.redo_action, self.space)
