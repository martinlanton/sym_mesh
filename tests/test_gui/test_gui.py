import logging
from maya import cmds as mc
from qtpy import QtTest, QtCore, QtGui
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
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_symmetry_no_target(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(clear=True)
        with self.assertLogs(
            base_test.connection_widget.controller.log, logging.ERROR
        ) as captured:
            QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        self.assertTrue(
            "Unable to symmetrize, no target selected." in captured.records[0].message
        )

    def test_symmetry_with_base(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_symmetry_with_base_negative_direction(self):
        QtTest.QTest.mouseClick(self.gui.negative_rb, QtCore.Qt.LeftButton)

        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

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

    def test_symmetry_with_base_negative_direction_after(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        QtTest.QTest.mouseClick(self.gui.negative_rb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

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

    def test_symmetry_with_base_y_axis(self):
        QtTest.QTest.mouseClick(self.gui.negative_rb, QtCore.Qt.LeftButton)

        QtTest.QTest.mouseClick(self.gui.y_axis_rb, QtCore.Qt.LeftButton)

        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        expected = [
            [-0.5, -0.5, 0.5],
            [0.5, -1.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 1.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 1.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, -1.5, -0.5],
        ]

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(expected, result)

    def test_symmetry_with_base_y_axis_after(self):
        QtTest.QTest.mouseClick(self.gui.negative_rb, QtCore.Qt.LeftButton)

        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        QtTest.QTest.mouseClick(self.gui.y_axis_rb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        expected = [
            [-0.5, -0.5, 0.5],
            [0.5, -1.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 1.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 1.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, -1.5, -0.5],
        ]

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(expected, result)

    def test_symmetry_with_base_and_vertex_selection(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

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
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mouseClick(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube, replace=True)
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

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

    def test_symmetry_table_threshold(self):
        """Test that building a symmetry table for an asymmetrical geometry produces the right
        symmetry table when a threshold is provided."""
        self.gui.threshold_sb.setValue(0.2)

        mc.select(self.asym_threshold_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube, replace=True)
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_symmetry_table_threshold_after(self):
        """Test that building a symmetry table for an asymmetrical geometry produces the right
        symmetry table when a threshold is provided."""
        mc.select(self.asym_threshold_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        self.gui.threshold_sb.setValue(0.2)

        mc.select(self.asym_cube, replace=True)
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_symmetry_from_slider_at_0(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        self.gui.symmetry_slider.setValue(0)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_symmetry_from_slider_at_100(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        self.gui.symmetry_slider.setValue(100)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_symmetry_from_slider_with_different_values(self):
        """Test that moving the slider continuously changes the value dynamically,
        but that the command is only added to the undo queue once the slider is released.
        """
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        self.gui.symmetry_slider.setValue(50)
        self.gui.symmetry_slider.setValue(100)
        self.gui.symmetry_slider.sliderReleased.emit()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

        log.info("LOOK HERE : %s", len(self.connector.ctrl.executor.undo_queue))
        QtTest.QTest.mouseClick(self.gui.undo_push_button, QtCore.Qt.LeftButton)
        log.info("LOOK HERE : %s", len(self.connector.ctrl.executor.undo_queue))

        with self.assertLogs(
            base_test.connection_widget.controller.executor.log, logging.ERROR
        ) as captured:
            QtTest.QTest.mouseClick(self.gui.undo_push_button, QtCore.Qt.LeftButton)

        self.assertTrue("No action to undo." in captured.records[0].message)

    def test_flip_no_base(self):
        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.flip_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_flip_no_target(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(clear=True)
        with self.assertLogs(
            base_test.connection_widget.controller.log, logging.ERROR
        ) as captured:
            QtTest.QTest.mouseClick(self.gui.flip_pb, QtCore.Qt.LeftButton)

        self.assertTrue(
            "Unable to flip, no target selected." in captured.records[0].message
        )

    def test_flip_with_base(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.flip_pb, QtCore.Qt.LeftButton)

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
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mouseClick(self.gui.flip_pb, QtCore.Qt.LeftButton)

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
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mouseClick(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube, replace=True)
        QtTest.QTest.mouseClick(self.gui.flip_pb, QtCore.Qt.LeftButton)

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

    def test_flip_from_slider_at_0(self):
        """Test that moving the slider to 0 doesn't flip the geometry."""
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        self.gui.flip_slider.setValue(0)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_flip_from_slider_at_100(self):
        """Test that moving the slider to 100 flips the geometry."""
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        self.gui.flip_slider.setValue(100)

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

    def test_flip_from_slider_with_different_values(self):
        """Test that moving the slider continuously changes the value dynamically,
        but that the command is only added to the undo queue once the slider is released.
        """
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        self.gui.flip_slider.setValue(50)
        self.gui.flip_slider.setValue(100)
        self.gui.flip_slider.sliderReleased.emit()

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

        QtTest.QTest.mouseClick(self.gui.undo_push_button, QtCore.Qt.LeftButton)

        with self.assertLogs(
            base_test.connection_widget.controller.executor.log, logging.ERROR
        ) as captured:
            QtTest.QTest.mouseClick(self.gui.undo_push_button, QtCore.Qt.LeftButton)

        self.assertTrue("No action to undo." in captured.records[0].message)

    def test_revert_to_base_no_base(self):
        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_revert_to_base_no_target(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(clear=True)
        with self.assertLogs(
            base_test.connection_widget.controller.log, logging.ERROR
        ) as captured:
            QtTest.QTest.mouseClick(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)

        self.assertTrue(
            "Unable to revert to base, no target selected."
            in captured.records[0].message
        )

    def test_revert_to_base_with_base(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_revert_to_base_with_base_and_vertex_selection(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mouseClick(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)

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
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mouseClick(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube, replace=True)
        QtTest.QTest.mouseClick(self.gui.revert_to_base_pb, QtCore.Qt.LeftButton)

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

    def test_revert_to_base_from_slider_at_0(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        self.gui.revert_to_base_slider.setValue(0)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_revert_to_base_from_slider_at_100(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        self.gui.revert_to_base_slider.setValue(100)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_revert_to_base_from_slider_with_different_values(self):
        """Test that moving the slider continuously changes the value dynamically,
        but that the command is only added to the undo queue once the slider is released.
        """
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        self.gui.revert_to_base_slider.setValue(50)
        self.gui.revert_to_base_slider.setValue(100)
        self.gui.revert_to_base_slider.sliderReleased.emit()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

        QtTest.QTest.mouseClick(self.gui.undo_push_button, QtCore.Qt.LeftButton)

        with self.assertLogs(
            base_test.connection_widget.controller.executor.log, logging.ERROR
        ) as captured:
            QtTest.QTest.mouseClick(self.gui.undo_push_button, QtCore.Qt.LeftButton)

        self.assertTrue("No action to undo." in captured.records[0].message)

    def test_bake_deltas_no_base(self):
        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.get_target_pb, QtCore.Qt.LeftButton)

        mc.select(self.other_cube)
        with self.assertLogs(
            base_test.connection_widget.controller.log, logging.ERROR
        ) as captured:
            QtTest.QTest.mouseClick(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertTrue(
            "Unable to bake deltas, no base position defined."
            in captured.records[0].message
        )
        self.assertEqual(self.expected_sym_position, result)

    def test_bake_deltas_no_target(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.other_cube)
        with self.assertLogs(
            base_test.connection_widget.controller.log, logging.ERROR
        ) as captured:
            QtTest.QTest.mouseClick(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertTrue(
            "Unable to bake deltas, no target position defined."
            in captured.records[0].message
        )
        self.assertEqual(self.expected_sym_position, result)

    def test_bake_deltas_with_no_selection(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.get_target_pb, QtCore.Qt.LeftButton)

        mc.select(clear=True)
        with self.assertLogs(
            base_test.connection_widget.controller.log, logging.ERROR
        ) as captured:
            QtTest.QTest.mouseClick(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)

        self.assertTrue(
            "Unable to bake deltas, no selected geometries to bake onto."
            in captured.records[0].message
        )

    def test_bake_deltas_with_base_and_target(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.get_target_pb, QtCore.Qt.LeftButton)

        mc.select(self.other_cube)
        QtTest.QTest.mouseClick(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_bake_deltas_with_stored_vertex_selection(self):
        """Test that baking the deltas on a mesh when a proper vertex selection is
        provided only bakes the deltas for the selected vertices."""
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.get_target_pb, QtCore.Qt.LeftButton)

        mc.select("{}.vtx[1]".format(self.asym_cube))
        QtTest.QTest.mouseClick(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)

        mc.select(self.other_cube, replace=True)
        QtTest.QTest.mouseClick(self.gui.bake_deltas_pb, QtCore.Qt.LeftButton)

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

    def test_extract_axes_no_base(self):
        mc.select(self.test_extract_axes_cube)
        with self.assertLogs(
            base_test.connection_widget.controller.log, logging.ERROR
        ) as captured:
            QtTest.QTest.mouseClick(self.gui.extract_axes_pb, QtCore.Qt.LeftButton)

        self.assertTrue(
            "Unable to extract axes, no base defined." in captured.records[0].message
        )

    def test_extract_axes_no_selection(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(clear=True)
        with self.assertLogs(
            base_test.connection_widget.controller.log, logging.ERROR
        ) as captured:
            QtTest.QTest.mouseClick(self.gui.extract_axes_pb, QtCore.Qt.LeftButton)

        self.assertTrue(
            "Unable to extract axes, no target selected." in captured.records[0].message
        )

    def test_extract_axes_creates_geometry(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.test_extract_axes_cube)
        QtTest.QTest.mouseClick(self.gui.extract_axes_pb, QtCore.Qt.LeftButton)

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
        expected_pos = [10, 30, 10]
        pos = mc.xform(extracted_mesh, query=True, translation=True)

        self.assertTrue(
            mc.objExists("|{}_extracted".format(self.test_extract_axes_cube))
        )
        self.assertTrue(mc.objExists(blendshape))
        self.assertEqual(expected_x, x)
        self.assertEqual(expected_y, y)
        self.assertEqual(expected_z, z)
        self.assertEqual(expected_pos, pos)

    def test_extract_axes_moves_geometry(self):
        self.gui.extract_sb.setValue(40)
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.test_extract_axes_cube)
        QtTest.QTest.mouseClick(self.gui.extract_axes_pb, QtCore.Qt.LeftButton)

        extracted_mesh = "{}_extracted".format(self.test_extract_axes_cube)

        expected_pos = [10, 50, 10]
        pos = mc.xform(extracted_mesh, query=True, translation=True)
        self.assertEqual(expected_pos, pos)

    def test_base_line_edit(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        result = self.gui.base_line_edit.text()

        self.assertEqual(self.sym_cube, result)

    def test_target_line_edit(self):
        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.get_target_pb, QtCore.Qt.LeftButton)

        result = self.gui.target_line_edit.text()

        self.assertEqual(self.asym_cube, result)

    def test_select_stored_vertex_selection(self):
        mc.select("{}.vtx[1]".format(self.sym_cube))
        QtTest.QTest.mouseClick(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)

        mc.select(clear=True)
        QtTest.QTest.mouseClick(
            self.gui.select_vertex_selection_pb, QtCore.Qt.LeftButton
        )

        result = mc.ls(selection=True)
        color = self.gui.get_vertex_selection_pb.palette().button().color()

        self.assertEqual(["{}.vtx[1]".format(self.sym_cube)], result)
        self.assertEqual("red", color)

    def test_reset_vertex_selection(self):
        mc.select("{}.vtx[1]".format(self.sym_cube))
        QtTest.QTest.mouseClick(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)

        mc.select(clear=True)
        QtTest.QTest.mouseClick(self.gui.get_vertex_selection_pb, QtCore.Qt.LeftButton)

        QtTest.QTest.mouseClick(
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
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(clear=True)
        QtTest.QTest.mouseClick(
            self.gui.select_non_symmetrical_vertices_pb, QtCore.Qt.LeftButton
        )

        result = mc.ls(selection=True, flatten=True)
        expected = ["{}.vtx[{}]".format(self.asym_cube, nb) for nb in [0, 3, 5, 6]]
        self.assertEqual(expected, result)

    def test_undo(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        QtTest.QTest.mouseClick(self.gui.undo_push_button, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_undo_shortcut(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        QtTest.QTest.keyClicks(self.connector, "z", QtCore.Qt.ControlModifier)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_asym_position, result)

    def test_redo(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        QtTest.QTest.mouseClick(self.gui.undo_push_button, QtCore.Qt.LeftButton)

        QtTest.QTest.mouseClick(self.gui.redo_push_button, QtCore.Qt.LeftButton)

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)

    def test_redo_shortcut(self):
        mc.select(self.sym_cube)
        QtTest.QTest.mouseClick(self.gui.get_base_pb, QtCore.Qt.LeftButton)

        mc.select(self.asym_cube)
        QtTest.QTest.mouseClick(self.gui.symmetry_pb, QtCore.Qt.LeftButton)

        QtTest.QTest.keyClicks(self.connector, "z", QtCore.Qt.ControlModifier)

        QtTest.QTest.keyClicks(
            self.connector, "z", QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]

        self.assertEqual(self.expected_sym_position, result)


if __name__ == "__main__":
    unittest.main()
