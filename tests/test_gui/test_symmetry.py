import logging
from maya import cmds as mc
from PySide2 import QtTest, QtCore
import unittest
from tests.test_gui import base_test

log = logging.getLogger(__name__)


class TestGUI(base_test.BaseGUITest):
    def test_symmetry_no_base(self):
        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.symmetry_push_button, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_push_button, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_symmetry_with_base(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pB, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pB, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.symmetry_push_button, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_push_button, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_symmetry_with_base_and_vertex_selection(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pB, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pB, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mousePress(self.gui.symmetry_push_button, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_push_button, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        expected = [
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 1.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 1.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
        ]

        self.assertEqual(expected, result)

    def test_flip_no_base(self):
        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.flip_push_button, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.flip_push_button, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_flip_with_base(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pB, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pB, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.flip_push_button, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.flip_push_button, QtCore.Qt.LeftButton)

        expected = [
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 1.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 1.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [0.5, -0.5, -0.5],
        ]

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
