import maya.cmds as mc
import pytest

from sym_mesh.ModifyMesh import ModifyMesh


@pytest.mark.usefixtures("session")
class TestMaya:
    @classmethod
    def setup_class(cls):
        mc.file(newFile=True, force=True)
        cls.sphere = mc.polySphere(name="This_is_a_test_sphere")
        cls.sym_cube = mc.polyCube(name="symmetrical_cube", constructionHistory=False)[0]
        cls.asym_cube = mc.polyCube(name="asymmetrical_cube", constructionHistory=False)[0]
        for vtx in [1, 3, 5, 7]:
            vtx_name = "{}.vtx[{}]".format(cls.asym_cube, vtx)
            mc.xform(vtx_name, relative=True, translation=[0, 1, 0])

    def test_sphere_has_been_created(self):
        assert mc.objExists('This_is_a_test_sphere')
        assert mc.nodeType('This_is_a_test_sphere') == 'transform'

    def test_cube_has_not_been_created(self):
        mesh_modifier = ModifyMesh()
        mesh_modifier.get_base_mesh(self.sym_cube)
        symmetry_table = mesh_modifier.get_symmetry_table()

        assert mesh_modifier
        assert symmetry_table == ({0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6}, [])
