import logging
from maya import cmds as mc
from PySide2 import QtTest, QtCore
import unittest
from tests.test_gui import base_test

log = logging.getLogger(__name__)


class TestSymmetry(base_test.GUITest):
    def test_symmetry_no_base(self):
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.symmetry_push_button, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_push_button, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        self.assertEqual(expected, result)

    def test_symmetry_with_base(self):
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))

        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pB, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pB, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.symmetry_push_button, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_push_button, QtCore.Qt.LeftButton)

        expected = [
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
        ]
        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
