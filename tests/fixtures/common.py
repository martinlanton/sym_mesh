import tempfile
import os
import unittest
from maya import cmds as mc


class BaseTest(unittest.TestCase):
    expected_asym_position = [
        [-0.5, -0.5, 0.5],
        [0.5, 0.5, 0.5],
        [-0.5, 0.5, 0.5],
        [0.5, 1.5, 0.5],
        [-0.5, 0.5, -0.5],
        [0.5, 1.5, -0.5],
        [-0.5, -0.5, -0.5],
        [0.5, 0.5, -0.5],
    ]
    expected_sym_position = [
        [-0.5, -0.5, 0.5],
        [0.5, -0.5, 0.5],
        [-0.5, 0.5, 0.5],
        [0.5, 0.5, 0.5],
        [-0.5, 0.5, -0.5],
        [0.5, 0.5, -0.5],
        [-0.5, -0.5, -0.5],
        [0.5, -0.5, -0.5],
    ]
    vtx_number = 8

    @classmethod
    def setUpClass(cls):
        startup_maya_session()

    def setUp(self):
        mc.file(newFile=True, force=True)
        self.sym_cube = mc.polyCube(name="sym_cube", constructionHistory=False)[0]
        self.other_cube = mc.polyCube(name="other_cube", constructionHistory=False)[0]
        self.asym_cube = mc.polyCube(name="asym_cube", constructionHistory=False)[0]
        for vtx in [1, 3, 5, 7]:
            vtx_name = "{}.vtx[{}]".format(self.asym_cube, vtx)
            mc.xform(vtx_name, relative=True, translation=[0, 1, 0])
        self.test_extract_axes_cube = mc.polyCube(
            name="axes_cube", constructionHistory=False
        )[0]
        for vtx in range(8):
            vtx_name = "{}.vtx[{}]".format(self.test_extract_axes_cube, vtx)
            mc.xform(vtx_name, relative=True, translation=[1, 1, 1])


def get_src_folder_path():
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(path, "src")
    return path


def startup_maya_session():
    currentMayaAppDir = os.environ.get("MAYA_APP_DIR")
    os.environ["MAYA_APP_DIR"] = tempfile.mkdtemp()

    from maya import standalone

    standalone.initialize()

    return {
        "tmpMayaAppDir": os.environ["MAYA_APP_DIR"],
        "origMayaAppDir": currentMayaAppDir,
    }
