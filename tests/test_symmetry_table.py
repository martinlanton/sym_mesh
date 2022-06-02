import maya.cmds as mc
import unittest
from tests.fixtures import common


class TestMaya(unittest.TestCase):
    state = None

    @classmethod
    def setUpClass(cls):
        cls.state = common.startup_maya_session()
        from sym_mesh.ModifyMesh import ModifyMesh
        cls.mesh_modifier = ModifyMesh()

    def setUp(self):
        mc.file(newFile=True, force=True)
        self.sphere = mc.polySphere(name="This_is_a_test_sphere")
        self.sym_cube = mc.polyCube(name="symmetrical_cube", constructionHistory=False)[0]
        self.asym_cube = mc.polyCube(name="asymmetrical_cube", constructionHistory=False)[0]
        for vtx in [1, 3, 5, 7]:
            vtx_name = "{}.vtx[{}]".format(self.asym_cube, vtx)
            mc.xform(vtx_name, relative=True, translation=[0, 1, 0])

    @classmethod
    def tearDownClass(cls):
        common.teardown_maya_session(cls.state)

    def test_world_space_symmetry(self):
        print("Nothing to see")
        self.mesh_modifier.get_base_mesh(self.sym_cube)
        symmetry_table = self.mesh_modifier.get_symmetry_table()

        print(symmetry_table)

