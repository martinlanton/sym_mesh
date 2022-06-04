import maya.cmds as mc
import unittest
from tests.fixtures import common


class TestMaya(unittest.TestCase):
    state = None

    @classmethod
    def setUpClass(cls):
        cls.state = common.startup_maya_session()

    def setUp(self):
        from sym_mesh.ModifyMesh import ModifyMesh
        self.mesh_modifier = ModifyMesh()

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

    # def test_revert_to_base(self):
    #     self.mesh_modifier.get_base_mesh(self.sym_cube)
    #     symmetry_table = self.mesh_modifier.get_symmetry_table()
    #     base_table = self.mesh_modifier.get
    #     self.mesh_modifier.revert_to_base()
    #
    #     self.assertTrue(self.mesh_modifier)
    #     self.assertEqual(symmetry_table, ({0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6}, []))
