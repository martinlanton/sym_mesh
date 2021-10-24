import maya.cmds as mc
import unittest
from tests.fixtures import common


class TestMaya(unittest.TestCase):
    state = None

    @classmethod
    def setUpClass(cls):
        cls.state = common.startup_maya_session()
        mc.polySphere(name="This_is_a_test_sphere")
        # TODO : Create a non symmetrical cube and a normal cube and use it to
        #  test revert and symmetry methods

    @classmethod
    def tearDownClass(cls):
        common.teardown_maya_session(cls.state)

    def test_sphere_has_been_created(self):
        self.assertTrue(mc.objExists("This_is_a_test_sphere"))
        self.assertEqual(mc.nodeType("This_is_a_test_sphere"), "transform")

    def test_cube_has_not_been_created(self):
        self.assertFalse(mc.objExists("This_is_a_test_cube"))

    def test_cone_has_not_been_created(self):
        self.assertFalse(mc.objExists("This_is_a_test_cone"))
