from maya import cmds as mc

from domain import table, mesh_modification
from tests.fixtures import common


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

# TODO : add tests with active vertices selection
