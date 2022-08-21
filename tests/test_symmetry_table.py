import logging

from tests.fixtures import common

from sym_mesh import table


log = logging.getLogger(__name__)


class TestSymmetryTable(common.BaseTest):
    def test_symmetry_table_for_x_symmetrical_geometry_positive(self):
        """Test that building a symmetry table for a symmetrical geometry produces the right
        symmetry table."""
        geo_table = table.GeometryTable(self.sym_cube, axis="x")

        expected_sym_table = {1: 0, 3: 2, 5: 4, 7: 6}
        expected_non_mirrored_vertices_indices = []
        expected = (expected_sym_table, expected_non_mirrored_vertices_indices)
        self.assertEqual(geo_table.symmetry_table, expected)

    def test_symmetry_table_for_x_symmetrical_geometry_negative(self):
        """Test that building a symmetry table for a symmetrical geometry produces the right
        symmetry table."""
        geo_table = table.GeometryTable(self.sym_cube, axis="x", direction="negative")

        expected_sym_table = {0: 1, 2: 3, 4: 5, 6: 7}
        expected_non_mirrored_vertices_indices = []
        expected = (expected_sym_table, expected_non_mirrored_vertices_indices)
        self.assertEqual(geo_table.symmetry_table, expected)

    def test_symmetry_table_for_y_symmetrical_geometry_positive(self):
        """Test that building a symmetry table for a symmetrical geometry produces the right
        symmetry table."""
        geo_table = table.GeometryTable(self.sym_cube, axis="y")

        expected_sym_table = {2: 0, 3: 1, 4: 6, 5: 7}
        expected_non_mirrored_vertices_indices = []
        expected = (expected_sym_table, expected_non_mirrored_vertices_indices)
        self.assertEqual(geo_table.symmetry_table, expected)

    def test_symmetry_table_for_asymmetrical_geometry(self):
        """Test that building a symmetry table for an asymmetrical geometry produces the right
        symmetry table."""
        geo_table = table.GeometryTable(self.asym_cube)

        expected_sym_table = {1: 2, 7: 4}
        expected_non_mirrored_vertices_indices = [0, 3, 5, 6]
        expected = (expected_sym_table, expected_non_mirrored_vertices_indices)
        self.assertEqual(geo_table.symmetry_table, expected)

    def test_symmetry_table_from_different_geometry(self):
        """Test that building a symmetry table for a specific geometry from a different geometry
        produces the right symmetry table."""
        geo_table = table.GeometryTable(self.asym_cube)
        geo_table.build_symmetry_table(self.sym_cube)

        expected_sym_table = {1: 0, 3: 2, 5: 4, 7: 6}
        expected_non_mirrored_vertices_indices = []
        expected = (expected_sym_table, expected_non_mirrored_vertices_indices)
        self.assertEqual(geo_table.symmetry_table, expected)

    # TODO : add test to create a new table from the difference of 2 tables,
    #  this can then be used to bake the difference on other meshes and have a
    #  more streamlined method signature

    # def test_timing_symmetry_table(self):
    #     import time
    #     from maya import cmds as mc
    #     cube1 = mc.polyCube(sx=20, sy=20, sz=20, ch=False)[0]
    #     before = time.time()
    #     for i in range(1000):
    #         base_table = table.GeometryTable(cube1)
    #     after = time.time()
    #     log.critical("It took %s seconds", (after-before))
