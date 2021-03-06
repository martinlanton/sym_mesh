from tests.fixtures import common

from sym_mesh import table


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


# base_cube_positions = [
#     (-0.5, -0.5, 0.5),
#     (0.5, -0.5, 0.5),
#     (-0.5, 0.5, 0.5),
#     (0.5, 0.5, 0.5),
#     (-0.5, 0.5, -0.5),
#     (0.5, 0.5, -0.5),
#     (-0.5, -0.5, -0.5),
#     (0.5, -0.5, -0.5),
# ]
