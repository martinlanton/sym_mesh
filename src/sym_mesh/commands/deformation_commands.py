import logging
from pprint import pformat

from maya.api import OpenMaya as om2

from sym_mesh.dag_path import create_MDagPath
from sym_mesh.selection import get_selected_mesh_points
from abc import ABCMeta


log = logging.getLogger(__name__)


class AbstractDeformationCommand(metaclass=ABCMeta):
    def __init__(
        self,
        base_table,
        target_table,
        selected_vertices_indices=(),
        percentage=100,
        target_dag_path=None,
        space=om2.MSpace.kObject,
    ):
        """Initialize the deformation command with the proper attributes.

        :param base_table: GeometryTable of the base geometry
        :type base_table: sym_mesh.table.GeometryTable

        :param target_table: GeometryTable of the target geometry
        :type target_table: sym_mesh.table.GeometryTable

        :param selected_vertices_indices: indices of the selected points on the target mesh
        :type selected_vertices_indices: maya.api.OpenMaya.MIntArray

        :param percentage: percentage used for the computing operation. This
        is a value from 0 to 100, a value of 100 means we're adding the full
        value of the computation between the base and target meshes to the
        destination mesh, a value of 0 means we're staying at the current position.
        :type percentage: int

        :param target_dag_path: MDagPath of the target
        :type target_dag_path: maya.api.OpenMaya.MDagPath or str

        :param space: space in which operate the deformation (object or world)
        :type space: constant
        """
        self.base_table = base_table
        self.target_table = target_table
        self.selected_vertices_indices = selected_vertices_indices
        self.percentage = percentage
        self.target_dag_path = target_dag_path
        self.space = space
        self.current_point_array = get_selected_mesh_points(
            create_MDagPath(target_dag_path)
        )
        self.undo_action = self.current_point_array
        self.result = self.deform(
            base_table,
            target_table,
            selected_vertices_indices,
            percentage,
            target_dag_path,
        )
        self.redo_action = self.result

    def deform(
            self,
            base_table,
            target_table,
            selected_vertices_indices=(),
            percentage=100,
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

        :param percentage: percentage used for the bake delta function. This
        is a value from 0 to 100, a value of 100 means we're adding the full
        delta between base and target to the destination meshes, a value of 0
        means we're staying at the current position.
        :type percentage: int

        :param target_dag_path: MDagPath of the target
        :type target_dag_path: maya.api.OpenMaya.MDagPath or str
        """
        raise NotImplementedError

    def undo(self):
        path = create_MDagPath(self.target_dag_path)
        tgt_mesh_functionset = om2.MFnMesh(path)
        tgt_mesh_functionset.setPoints(self.undo_action, self.space)

    def redo(self):
        path = create_MDagPath(self.target_dag_path)
        tgt_mesh_functionset = om2.MFnMesh(path)
        tgt_mesh_functionset.setPoints(self.redo_action, self.space)


class BakeDifferenceCommand(AbstractDeformationCommand):
    def deform(
        self,
        base_table,
        target_table,
        selected_vertices_indices=(),
        percentage=100,
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

        :param percentage: percentage used for the bake delta function. This
        is a value from 0 to 100, a value of 100 means we're adding the full
        delta between base and target to the destination meshes, a value of 0
        means we're staying at the current position.
        :type percentage: int

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
                    + (
                        (target_point_array[i] - base_point_array[i])
                        * (percentage / 100.0)
                    )
                )
            # If the current point is not selected
            else:
                # Do nothing
                destination_table.append(self.current_point_array[i])

        # Modify points position using the new coordinates
        tgt_mesh_functionset.setPoints(destination_table, self.space)

        return destination_table


class RevertToBaseCommand(AbstractDeformationCommand):
    def deform(
        self,
        base_table,
        current_table,
        selected_vertices_indices=(),
        percentage=100,
        target_dag_path=None,
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

        :param target_dag_path: MDagPath of the target
        :type target_dag_path: maya.api.OpenMaya.MDagPath or str
        """
        base_point_array = base_table.point_array
        log.debug("base_point_array :\n%s", pformat(base_point_array))
        current_point_array = current_table.point_array
        log.debug("current_point_array :\n%s", pformat(current_point_array))

        # Create new table for destination position
        destination_table = om2.MPointArray()

        # Init MFnMesh
        tgt_mesh_functionset = om2.MFnMesh(target_dag_path)

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
                    * ((100 - percentage) / 100.0)
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


class SymmetrizeCommand(AbstractDeformationCommand):
    def deform(
        self,
        base_table,
        current_table,
        selected_vertices_indices=(),
        percentage=100,
        target_dag_path=None,
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

        :param target_dag_path: MDagPath of the target
        :type target_dag_path: maya.api.OpenMaya.MDagPath or str
        """
        axis = self.base_table.axis
        axis_indices = {"x": 0, "y": 1, "z": 2}
        axis_index = axis_indices[axis]

        # Create new table for destination position

        current_point_array = current_table.point_array
        base_point_array = self.base_table.point_array
        symmetry_table = self.base_table.symmetry_table[0]
        log.debug("Symmetry table is : %s", symmetry_table)

        destination_point_array = om2.MPointArray()
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
                    (symmetry_position - current_position) * (percentage / 100.0)
                )
            else:
                log.debug("Not mirroring the position of vtx %s", i)

            log.debug(
                "Modifying position from %s to %s", current_position, symmetry_position
            )
            destination_point_array.append(symmetry_position)

        # Modify points position using the new coordinates
        tgt_mesh = om2.MFnMesh(target_dag_path)
        tgt_mesh.setPoints(destination_point_array, self.space)

        return destination_point_array
