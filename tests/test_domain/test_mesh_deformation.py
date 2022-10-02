import logging

import maya.cmds as mc
from tests.fixtures import common

from domain import table
from domain import mesh_modification
from domain import selection

log = logging.getLogger(__name__)


class TestRevertToBase(common.BaseTest):
    def test_revert_to_current(self):
        """Test that reverting to base with a value of 100% doesn't revert anything."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.revert_to_base(
            base_table=sym_table, target_table=geo_table, percentage=0
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        self.assertEqual(self.expected_asym_position, result)

    def test_revert_to_base(self):
        """Test that reverting to base with a value of 0% reverts to base."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.revert_to_base(
            base_table=sym_table, target_table=geo_table, percentage=100
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        self.assertEqual(self.expected_sym_position, result)

    def test_revert_to_base_with_vertex_selection(self):
        """Test that reverting the mesh to base when a proper vertex selection is
        provided only reverts the selected vertices."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mc.select("{}.vtx[1]".format(self.asym_cube))
        vertex_selection = selection.VertexSelection()
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.revert_to_base(
            base_table=sym_table,
            target_table=geo_table,
            selected_vertices_indices=vertex_selection,
            percentage=100,
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        expected = [
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 1.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 1.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
        ]

        self.assertEqual(expected, result)

    def test_revert_to_base_with_no_vertex_selection(self):
        """Test that reverting to base with a vertex selection when nothing is
        selected does revert the entire mesh and doesn't care about the vertex selection."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mc.select(clear=True)
        vertex_selection = selection.VertexSelection()
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.revert_to_base(
            base_table=sym_table,
            target_table=geo_table,
            selected_vertices_indices=vertex_selection,
            percentage=100,
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_revert_to_base_with_geometry_selected_for_vertex_selection(self):
        """Test that reverting to base with a vertex selection from a full mesh
        selected does revert the entire mesh and doesn't care about the vertex selection."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mc.select(self.asym_cube)
        vertex_selection = selection.VertexSelection()
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.revert_to_base(
            base_table=sym_table,
            target_table=geo_table,
            selected_vertices_indices=vertex_selection,
            percentage=100,
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)


class TestSymmetry(common.BaseTest):
    def test_symmetrization_x_positive(self):
        """Test that symmetrizing on the X axis in the positive direction (-X towards +X)
        symmetrizes properly."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="positive")
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", self.expected_sym_position)
        log.info("Result : %s", result)
        self.assertEqual(self.expected_sym_position, result)

    def test_symmetrization_x_negative(self):
        """Test that symmetrizing on the X axis in the negative direction (+X towards -X)
        symmetrizes properly.
        """
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="negative")
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table)

        expected = [
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 1.5, 0.5],
            [0.5, 1.5, 0.5],
            [-0.5, 1.5, -0.5],
            [0.5, 1.5, -0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 0.5, -0.5],
        ]
        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)

    def test_symmetrization_y_negative(self):
        """Test that symmetrizing on the Y axis in the negative direction (+Y towards -Y)
        symmetrizes properly.
        """
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="y", direction="negative")
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table)

        expected = [
            [-0.5, -0.5, 0.5],
            [0.5, -1.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 1.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 1.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, -1.5, -0.5],
        ]
        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)

    def test_symmetrization_x_positive_zero_percent(self):
        """Test that symmetrizing with a value of 0% doesn't do anything."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="positive")
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(
            base_table=sym_table, target_table=geo_table, percentage=0
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", self.expected_asym_position)
        log.info("Result : %s", result)
        self.assertEqual(self.expected_asym_position, result)

    def test_symmetrization_x_positive_with_vertex_selection(self):
        """Test that symmetrizing on the X axis in the positive direction (-X towards +X)
        with a vertex selection symmetrizes properly."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="positive")
        mc.select("{}.vtx[1]".format(self.asym_cube))
        vertex_selection = selection.VertexSelection()
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table, selected_vertices_indices=vertex_selection)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        expected = [
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 1.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 1.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
        ]

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", self.expected_sym_position)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)


class TestBakeDeltas(common.BaseTest):
    def test_bake_delta(self):
        """Test that baking delta functions properly on one geometry."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.bake_difference(
            sym_table, geo_table, target_dag_path=self.other_cube
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        self.assertEqual(self.expected_asym_position, result)

    def test_bake_delta_zero_percent(self):
        """Test that baking delta functions properly on one geometry."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.bake_difference(
            sym_table, geo_table, percentage=0, target_dag_path=self.other_cube
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        self.assertEqual(self.expected_sym_position, result)


class TestFlip(common.BaseTest):
    def test_flip_y_positive(self):
        """Test that reverting to base with a value of 0% reverts to base."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="y", direction="positive")
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.flip(base_table=sym_table, target_table=geo_table)

        expected = [
            [-0.5, -0.5, 0.5],
            [0.5, -1.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, -0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, -1.5, -0.5],
        ]
        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)


# TODO : add tests with active vertices selection
