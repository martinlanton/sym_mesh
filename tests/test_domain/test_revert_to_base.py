from maya import cmds as mc

from domain import table, mesh_modification, selection
from tests.fixtures import common


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
            vertex_selection=vertex_selection,
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
            vertex_selection=vertex_selection,
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
            vertex_selection=vertex_selection,
            percentage=100,
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)
