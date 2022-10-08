import logging
from maya import cmds as mc

from domain import table, mesh_modification, selection
from tests.fixtures import common

log = logging.getLogger(__name__)


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
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table, vertex_selection=vertex_selection)

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

    def test_symmetrization_x_positive_with_no_vertex_selection(self):
        """Test that symmetrizing on the X axis in the positive direction (-X towards +X)
        without vertex selection symmetrizes properly."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="positive")
        mc.select(clear=True)
        vertex_selection = selection.VertexSelection()
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table, vertex_selection=vertex_selection)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", self.expected_sym_position)
        log.info("Result : %s", result)
        self.assertEqual(self.expected_sym_position, result)

    def test_symmetrization_x_positive_with_geometry_selected_for_vertex_selection(self):
        """Test that symmetrizing on the X axis in the positive direction (-X towards +X)
        without vertex selection symmetrizes properly."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="positive")
        mc.select(self.asym_cube)
        vertex_selection = selection.VertexSelection()
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table, vertex_selection=vertex_selection)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", self.expected_sym_position)
        log.info("Result : %s", result)
        self.assertEqual(self.expected_sym_position, result)
