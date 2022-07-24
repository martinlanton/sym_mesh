from pprint import pprint

import maya.cmds as mc
from tests.fixtures import common

from sym_mesh import table
from sym_mesh import mesh_modification


class TestMeshDeformation(common.BaseTest):
    def test_revert_to_base(self):
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.revert_to_base(
            base_table=sym_table, current_table=geo_table, percentage=0
        )

        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))

        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.sym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        pprint(expected)
        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        pprint(result)

        self.assertEqual(expected, result)
