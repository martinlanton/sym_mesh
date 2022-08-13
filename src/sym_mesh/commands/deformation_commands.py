import logging

from maya.api import OpenMaya as om2

from sym_mesh.commands.abstract_commands import AbstractDeformationCommand

log = logging.getLogger(__name__)


class BakeDifferenceCommand(AbstractDeformationCommand):
    """Bake the difference between 2 mesh on a list of vertices on a mesh."""
    def compute_point_position(self, base_point_array, target_point_array):
        destination_table = om2.MPointArray()
        # Loop in MPointArray
        for i in range(len(base_point_array)):
            # If the current point is also in selection
            if (
                i in self.selected_vertices_indices
                or self.selected_vertices_indices.__len__() == 0
            ):
                # Modify new position
                destination_table.append(
                    self.current_point_array[i]
                    + (
                        (target_point_array[i] - base_point_array[i])
                        * (self.percentage / 100.0)
                    )
                )
            # If the current point is not selected
            else:
                # Do nothing
                destination_table.append(self.current_point_array[i])
        return destination_table


class RevertToBaseCommand(AbstractDeformationCommand):
    """Revert selected vertices on the target mesh to the base position."""
    def compute_point_position(self, base_point_array, target_point_array):
        destination_table = om2.MPointArray()
        # Loop in MPointArray
        for i in range(base_point_array.__len__()):
            # If the current point is also in selection
            if (
                i in self.selected_vertices_indices
                or self.selected_vertices_indices.__len__() == 0
            ):
                # Modify new position
                base_position = base_point_array[i]
                new_position = base_position + (
                    (target_point_array[i] - base_position)
                    * ((100 - self.percentage) / 100.0)
                )
                log.debug("New position : %s", new_position)
                destination_table.append(new_position)
            # If the current point is not selected
            else:
                # Do nothing
                destination_table.append(target_point_array[i])
        return destination_table


class SymmetrizeCommand(AbstractDeformationCommand):
    """Symmetrize selected vertices on the target mesh."""
    def compute_point_position(self, base_point_array, target_point_array):
        axis = self.base_table.axis
        axis_indices = {"x": 0, "y": 1, "z": 2}
        axis_index = axis_indices[axis]

        symmetry_table = self.base_table.symmetry_table[0]
        log.debug("Symmetry table is : %s", symmetry_table)

        destination_point_array = om2.MPointArray()
        # Loop in MPointArray
        for i in range(len(base_point_array)):
            # If the current point is also in selection
            current_position = symmetry_position = target_point_array[i]
            if (
                i in self.selected_vertices_indices
                or self.selected_vertices_indices.__len__() == 0
            ) and i in symmetry_table:
                # Modify new position
                source_index = symmetry_table[i]
                target_vertex_position = target_point_array[source_index]
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
                    (symmetry_position - current_position) * (self.percentage / 100.0)
                )
            else:
                log.debug("Not mirroring the position of vtx %s", i)

            log.debug(
                "Modifying position from %s to %s", current_position, symmetry_position
            )
            destination_point_array.append(symmetry_position)
        return destination_point_array
