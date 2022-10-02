import tempfile
import os
import shutil
import sys
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

    def get_blendshape_target_vertices_positions(self, axis, blendshape, mesh):
        """Get the vertices positions for the specified blendshape target.

        :param axis: name of the axis for which we want the vertices positions.
        :type axis: str

        :param blendshape: name of the blendshape node from which we want the target
        :type blendshape: str

        :param mesh: name of the mesh from which we need to query the position
        :type mesh: str

        :return: vertices positions for the specified blendshape target.
        :rtype: list[tuple(int, int, int)]
        """
        mc.setAttr("{}.{}_{}".format(blendshape, self.test_extract_axes_cube, axis), 1)
        result = [
            mc.pointPosition("{}.vtx[{}]".format(mesh, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        mc.setAttr("{}.{}_{}".format(blendshape, self.test_extract_axes_cube, axis), 0)
        return result


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


def setup_environment():
    # Adding package into the environment
    path = get_src_folder_path()
    print(path)
    if path not in sys.path:
        sys.path.append(path)
    from pprint import pprint

    pprint(sys.path)


def teardown_maya_session(state):
    from maya import standalone

    standalone.uninitialize()

    try:
        shutil.rmtree(state["tmpMayaAppDir"])
    # Windows hasn't given up the handles to the files yet. So, ignore it.
    except WindowsError:
        pass

    if state["origMayaAppDir"] is not None:
        os.environ["MAYA_APP_DIR"] = state["origMayaAppDir"]
