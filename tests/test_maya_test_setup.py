import maya.cmds as mc
import pytest


@pytest.mark.usefixtures("session")
class TestMaya:
    @classmethod
    def setup_class(cls):
        mc.polySphere(name='This_is_a_test_sphere')

    def test_sphere_has_been_created(self):
        assert mc.objExists('This_is_a_test_sphere')
        assert mc.nodeType('This_is_a_test_sphere') == 'transform'

    def test_cube_has_not_been_created(self):
        assert mc.objExists('This_is_a_test_cube') is False

    def test_cone_has_not_been_created(self):
        assert mc.objExists('This_is_a_test_cone') is False
