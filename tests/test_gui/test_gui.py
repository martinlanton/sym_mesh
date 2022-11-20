import logging
from maya import cmds as mc
from Qt import QtTest, QtCore, QtGui
import unittest
from tests.test_gui import base_test

log = logging.getLogger(__name__)


class TestGUI(base_test.BaseGUITest):
    """All the gui tests must be in the same class.
    This is because the github maya docker container doesn't seem to support the
    recuperation of the QApplication instance with an if statement without crashing.
    The QApplication being a singleton, it cannot be re-instantiated and must be
    deleted before creating a new one.

    """

    def test_symmetry_no_base(self):
        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.symmetry_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_symmetry_with_base(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.symmetry_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_symmetry_with_base_negative_direction(self):
        QtTest.QTest.mousePress(self.gui.negative_rb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.negative_rb, QtCore.Qt.LeftButton)

        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.symmetry_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        expected = [
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 1.5, 0.5],
            [0.5, 1.5, 0.5],
            [-0.5, 1.5, -0.5],
            [0.5, 1.5, -0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 0.5, -0.5],
        ]

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(expected, result)

    # def test_symmetry_with_base_y_axis(self):
    #     QtTest.QTest.mousePress(self.gui.y_axis_rb, QtCore.Qt.LeftButton)
    #     QtTest.QTest.mouseRelease(self.gui.y_axis_rb, QtCore.Qt.LeftButton)
    #
    #     mc.select(self.sym_cube)
    #     QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
    #     QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)
    #
    #     mc.select(self.asym_cube)
    #     QtTest.QTest.mousePress(self.gui.symmetry_pb, QtCore.Qt.LeftButton)
    #     QtTest.QTest.mouseRelease(self.gui.symmetry_pb, QtCore.Qt.LeftButton)
    #
    #     result = [
    #         mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
    #         for vtx in range(self.vtx_number)
    #     ]
    #
    #     self.assertEqual(self.expected_sym_position, result)

    def test_symmetry_with_base_and_vertex_selection(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mousePress(self.gui.symmetry_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

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

    def test_symmetry_with_base_and_stored_vertex_selection(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mousePress(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(
            self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton
        )

        mc.select(self.asym_cube, replace=True)
        QtTest.QTest.mousePress(self.gui.symmetry_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

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
        QtTest.QTest.mousePress(self.gui.flip_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.flip_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_flip_with_base(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.flip_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.flip_pb, QtCore.Qt.LeftButton)

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

    def test_flip_with_base_and_vertex_selection(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mousePress(self.gui.flip_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.flip_pb, QtCore.Qt.LeftButton)

        expected = [
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 1.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 1.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
        ]

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(expected, result)

    def test_flip_with_base_and_stored_vertex_selection(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mousePress(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(
            self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton
        )

        mc.select(self.asym_cube, replace=True)
        QtTest.QTest.mousePress(self.gui.flip_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.flip_pb, QtCore.Qt.LeftButton)

        expected = [
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 1.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 1.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
        ]

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(expected, result)

    def test_revert_to_base_no_base(self):
        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_revert_to_base_with_base(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_revert_to_base_with_base_and_vertex_selection(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mousePress(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)

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

    def test_revert_to_base_with_base_and_stored_vertex_selection(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mousePress(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(
            self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton
        )

        mc.select(self.asym_cube, replace=True)
        QtTest.QTest.mousePress(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)

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

    def test_bake_deltas_no_base(self):
        mc.select(self.other_cube)
        QtTest.QTest.mousePress(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_bake_deltas_no_target(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.other_cube)
        QtTest.QTest.mousePress(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_bake_deltas_with_base_and_target(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.get_target_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_target_pb, QtCore.Qt.LeftButton)

        mc.select(self.other_cube)
        QtTest.QTest.mousePress(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_bake_deltas_with_stored_vertex_selection(self):
        """Test that baking the deltas on a mesh when a proper vertex selection is
        provided only bakes the deltas for the selected vertices."""
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.get_target_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_target_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mousePress(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(
            self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton
        )

        mc.select(self.other_cube, replace=True)
        QtTest.QTest.mousePress(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        expected_sym_position = [
            [-0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
        ]

        self.assertEqual(expected_sym_position, result)

    def test_extract_axes_creates_geometry(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.test_extract_axes_cube)
        QtTest.QTest.mousePress(self.gui.extract_axes_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.extract_axes_pb, QtCore.Qt.LeftButton)

        expected_x = [
            [0.5, -0.5, 0.5],
            [1.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [1.5, 0.5, 0.5],
            [0.5, 0.5, -0.5],
            [1.5, 0.5, -0.5],
            [0.5, -0.5, -0.5],
            [1.5, -0.5, -0.5],
        ]
        expected_y = [
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, 1.5, 0.5],
            [0.5, 1.5, 0.5],
            [-0.5, 1.5, -0.5],
            [0.5, 1.5, -0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 0.5, -0.5],
        ]
        expected_z = [
            [-0.5, -0.5, 1.5],
            [0.5, -0.5, 1.5],
            [-0.5, 0.5, 1.5],
            [0.5, 0.5, 1.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
        ]

        extracted_mesh = "{}_extracted".format(self.test_extract_axes_cube)
        blendshape = "{}_blendShape".format(extracted_mesh)

        x, y, z = [
            self.get_blendshape_target_vertices_positions(
                axis, blendshape, extracted_mesh
            )
            for axis in ["x", "y", "z"]
        ]

        self.assertTrue(
            mc.objExists("|{}_extracted".format(self.test_extract_axes_cube))
        )
        self.assertTrue(mc.objExists(blendshape))
        self.assertEqual(expected_x, x)
        self.assertEqual(expected_y, y)
        self.assertEqual(expected_z, z)

    def test_base_line_edit(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        result = self.gui.base_line_edit.text()

        self.assertEqual(self.sym_cube, result)

    def test_target_line_edit(self):
        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.get_target_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_target_pb, QtCore.Qt.LeftButton)

        result = self.gui.target_line_edit.text()

        self.assertEqual(self.asym_cube, result)

    def test_select_stored_vertex_selection(self):
        mc.select("{}.vtx[1]".format(self.sym_cube))
        QtTest.QTest.mousePress(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(
            self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton
        )

        mc.select(clear=True)
        QtTest.QTest.mousePress(
            self.gui.select_vertex_selection_pb, QtCore.Qt.LeftButton
        )
        QtTest.QTest.mouseRelease(
            self.gui.select_vertex_selection_pb, QtCore.Qt.LeftButton
        )

        result = mc.ls(selection=True)
        color = self.gui.get_vertex_selection_pb.palette().button().color()

        self.assertEqual(["{}.vtx[1]".format(self.sym_cube)], result)
        self.assertEqual("red", color)

    def test_reset_vertex_selection(self):
        mc.select("{}.vtx[1]".format(self.sym_cube))
        QtTest.QTest.mousePress(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(
            self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton
        )

        mc.select(clear=True)
        QtTest.QTest.mousePress(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(
            self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton
        )

        QtTest.QTest.mousePress(
            self.gui.select_vertex_selection_pb, QtCore.Qt.LeftButton
        )
        QtTest.QTest.mouseRelease(
            self.gui.select_vertex_selection_pb, QtCore.Qt.LeftButton
        )

        result = mc.ls(selection=True)
        color = self.gui.get_vertex_selection_pb.palette().button().color()

        self.assertEqual([], result)
        self.assertEqual(
            QtGui.QColor.fromRgbF(0.364706, 0.364706, 0.364706, 1.000000), color
        )

    def test_non_symmetrical_vertices_selection(self):
        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(clear=True)
        QtTest.QTest.mousePress(
            self.gui.select_non_symmetrical_vertices_pb, QtCore.Qt.LeftButton
        )
        QtTest.QTest.mouseRelease(
            self.gui.select_non_symmetrical_vertices_pb, QtCore.Qt.LeftButton
        )

        result = mc.ls(selection=True, flatten=True)
        expected = ["{}.vtx[{}]".format(self.asym_cube, nb) for nb in [0, 3, 5, 6]]
        self.assertEqual(expected, result)

    def test_undo(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.symmetry_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        QtTest.QTest.mousePress(self.gui.undo_push_button, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.undo_push_button, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_undo_shortcut(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.symmetry_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        QtTest.QTest.keyClicks(self.connector, "z", QtCore.Qt.ControlModifier)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_redo(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mousePress(self.gui.symmetry_pb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        QtTest.QTest.mousePress(self.gui.undo_push_button, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.undo_push_button, QtCore.Qt.LeftButton)

        QtTest.QTest.mousePress(self.gui.redo_push_button, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(self.gui.redo_push_button, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    # def test_redo_shortcut(self):
    #     mc.select(self.sym_cube)
    #     QtTest.QTest.mousePress(self.gui.get_base_pb, QtCore.Qt.LeftButton)
    #     QtTest.QTest.mouseRelease(self.gui.get_base_pb, QtCore.Qt.LeftButton)
    #
    #     mc.select(self.asym_cube)
    #     QtTest.QTest.mousePress(self.gui.symmetry_pb, QtCore.Qt.LeftButton)
    #     QtTest.QTest.mouseRelease(self.gui.symmetry_pb, QtCore.Qt.LeftButton)
    #
    #     QtTest.QTest.keyClicks(self.connector, "z", QtCore.Qt.ControlModifier)
    #
    #     QtTest.QTest.keyClicks(
    #         self.connector, "z", QtCore.Qt.ControlModifier, QtCore.Qt.ShiftModifier
    #     )
    #
    #     result = [
    #         mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
    #         for vtx in range(self.vtx_number)
    #     ]
    #
    #     self.assertEqual(self.expected_sym_position, result)


if __name__ == "__main__":
    unittest.main()
