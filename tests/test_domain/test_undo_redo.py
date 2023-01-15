import logging

from maya import cmds as mc

from domain import table
from domain import executor
from tests.fixtures import common


log = logging.getLogger(__name__)


class TestUndo(common.BaseTest):
    def test_nothing_to_undo(self):
        executor_ = executor.Executor()

        with self.assertLogs(executor.log, logging.ERROR) as captured:
            executor_.undo()

        self.assertTrue("No action to undo." in captured.records[0].message)

    def test_undo_revert_to_base(self):
        """Test that undo after revert to base works properly."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        asym_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        executor_ = executor.Executor()
        executor_.revert_to_base(
            base_table=sym_table, target_table=asym_table, percentage=100
        )
        executor_.stash_command()
        executor_.undo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)

    def test_undo_symmetry(self):
        """Test that undo after symmetrization works properly."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="positive")
        executor_ = executor.Executor()
        executor_.symmetrize(base_table=sym_table, target_table=geo_table)
        executor_.stash_command()
        executor_.undo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)

    def test_undo_bake_deltas(self):
        """Test that undo after baking delta works properly."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        executor_ = executor.Executor()
        executor_.bake_difference(
            sym_table, geo_table, target_dag_path=self.other_cube
        )
        executor_.stash_command()
        executor_.undo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        self.assertEqual(expected, result)

    def test_undo_extract_axes(self):
        """Test that undo after extracting axes works properly."""
        target_table = table.GeometryTable(self.test_extract_axes_cube)
        base_table = table.GeometryTable(self.sym_cube)
        executor_ = executor.Executor()
        extracted_mesh, blendshape = executor_.extract_axes(
            base_table=base_table, target_table=target_table
        )
        executor_.stash_command()
        executor_.undo()

        self.assertFalse(mc.objExists(extracted_mesh))
        self.assertFalse(mc.objExists(blendshape))

    def test_undo_flip(self):
        """Test that undo after symmetrization works properly."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="positive")
        executor_ = executor.Executor()
        executor_.flip(base_table=sym_table, target_table=geo_table)
        executor_.stash_command()
        executor_.undo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)


class TestRedo(common.BaseTest):
    def test_nothing_to_redo(self):
        executor_ = executor.Executor()

        with self.assertLogs(executor.log, logging.ERROR) as captured:
            executor_.redo()

        self.assertTrue("No action to redo." in captured.records[0].message)

    def test_redo_revert_to_base(self):
        """Test that undo after revert to base works properly."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.sym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        asym_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        executor_ = executor.Executor()
        executor_.revert_to_base(
            base_table=sym_table, target_table=asym_table, percentage=100
        )
        executor_.stash_command()
        executor_.undo()
        executor_.redo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)

    def test_undo_redo_revert_to_base(self):
        """Test that undo after redoing a revert to base works properly."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        asym_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        executor_ = executor.Executor()
        executor_.revert_to_base(
            base_table=sym_table, target_table=asym_table, percentage=100
        )
        executor_.stash_command()
        executor_.undo()
        executor_.redo()
        executor_.undo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)

    def test_redo_symmetry(self):
        """Test that undo after symmetrization works properly."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
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

        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="positive")
        executor_ = executor.Executor()
        executor_.symmetrize(base_table=sym_table, target_table=geo_table)
        executor_.stash_command()
        executor_.undo()
        executor_.redo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)

    def test_redo_bake_deltas(self):
        """Test that undo after baking delta works properly."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        executor_ = executor.Executor()
        executor_.bake_difference(
            sym_table, geo_table, target_dag_path=self.other_cube
        )
        executor_.stash_command()
        executor_.undo()
        executor_.redo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        self.assertEqual(expected, result)

    def test_redo_extract_axes(self):
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))

        target_table = table.GeometryTable(self.test_extract_axes_cube)
        base_table = table.GeometryTable(self.sym_cube)
        executor_ = executor.Executor()
        extracted_mesh, blendshape = executor_.extract_axes(
            base_table=base_table, target_table=target_table
        )
        executor_.stash_command()
        executor_.undo()
        executor_.redo()

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

        x, y, z = [
            self.get_blendshape_target_vertices_positions(
                axis, blendshape, extracted_mesh
            )
            for axis in ["x", "y", "z"]
        ]

        self.assertEqual(expected_x, x)
        self.assertEqual(expected_y, y)
        self.assertEqual(expected_z, z)

    def test_redo_flip(self):
        """Test that undo after symmetrization works properly."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            [-0.5, -0.5, 0.5],
            [0.5, -1.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, -0.5],
            [0.5, -0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, -1.5, -0.5],
        ]

        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="y", direction="positive")
        executor_ = executor.Executor()
        executor_.flip(base_table=sym_table, target_table=geo_table)
        executor_.stash_command()
        executor_.undo()
        executor_.redo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)
