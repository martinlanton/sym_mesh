import logging

import maya.cmds as mc
from tests.fixtures import common

from domain import table, mesh_modification, selection

log = logging.getLogger(__name__)


class TestFlip(common.BaseTest):
    def test_flip_y_positive(self):
        """Test that flipping works properly.
        Flipping on the Y axis positive direction for this test."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="y", direction="positive")
        mesh_modifier = mesh_modification.Executor()
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

    def test_flip_with_base_and_vertex_selection(self):
        """Test that flipping works properly.
        Flipping on the X axis positive direction for this test."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mc.select("{}.vtx[1]".format(self.asym_cube))
        vertex_selection = selection.VertexSelection()
        mesh_modifier = mesh_modification.Executor()
        mesh_modifier.flip(
            base_table=sym_table,
            target_table=geo_table,
            vertex_selection=vertex_selection,
        )

        expected = [
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 1.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 1.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
        ]

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(expected, result)

    def test_flip_y_positive_with_no_vertex_selection(self):
        """Test that flipping without a vertex selection works properly.
        Flipping on the Y axis positive direction for this test."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="y", direction="positive")
        mc.select(clear=True)
        vertex_selection = selection.VertexSelection()
        mesh_modifier = mesh_modification.Executor()
        mesh_modifier.flip(
            base_table=sym_table,
            target_table=geo_table,
            vertex_selection=vertex_selection,
        )

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

    def test_flip_y_positive_with_geometry_selected_for_vertex_selection(self):
        """Test that flipping with the mesh selected for vertex selection works properly.
        Flipping on the Y axis positive direction for this test."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="y", direction="positive")
        mc.select(self.asym_cube)
        vertex_selection = selection.VertexSelection()
        mesh_modifier = mesh_modification.Executor()
        mesh_modifier.flip(
            base_table=sym_table,
            target_table=geo_table,
            vertex_selection=vertex_selection,
        )

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
