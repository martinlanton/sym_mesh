from tests.fixtures import common

from sym_mesh import table


class TestSymmetryTable(common.BaseTest):
    def test_symmetry_table_for_symmetrical_geometry(self):
        """Test that building a symmetry table for a symmetrical geometry produces the right
        symmetry table."""
        geo_table = table.GeometryTable(self.sym_cube)

        expected_sym_table = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6}
        expected_non_mirrored_vertices_indices = []
        expected = (expected_sym_table, expected_non_mirrored_vertices_indices)
        self.assertEqual(geo_table.symmetry_table, expected)

    def test_symmetry_table_for_asymmetrical_geometry(self):
        """Test that building a symmetry table for an asymmetrical geometry produces the right
        symmetry table."""
        geo_table = table.GeometryTable(self.asym_cube)

        expected_sym_table = {1: 2, 2: 1, 4: 7, 7: 4}
        expected_non_mirrored_vertices_indices = [0, 3, 5, 6]
        expected = (expected_sym_table, expected_non_mirrored_vertices_indices)
        self.assertEqual(geo_table.symmetry_table, expected)

    def test_symmetry_table_from_different_geometry(self):
        """Test that building a symmetry table for a specific geometry from a different geometry
        produces the right symmetry table."""
        geo_table = table.GeometryTable(self.asym_cube)
        geo_table.build_symmetry_table(self.sym_cube)

        expected_sym_table = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6}
        expected_non_mirrored_vertices_indices = []
        expected = (expected_sym_table, expected_non_mirrored_vertices_indices)
        self.assertEqual(geo_table.symmetry_table, expected)
