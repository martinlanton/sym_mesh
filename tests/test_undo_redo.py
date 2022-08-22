import logging

from maya import cmds as mc

from sym_mesh.domain import table, mesh_modification
from tests.fixtures import common


log = logging.getLogger(__name__)


class TestUndo(common.BaseTest):
    def test_undo_revert_to_base(self):
        """Test that undo after revert to base works properly."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        asym_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.revert_to_base(
            base_table=sym_table, target_table=asym_table, percentage=100
        )
        mesh_modifier.undo()

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
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table)
        mesh_modifier.undo()

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
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.bake_difference(
            sym_table, geo_table, target_dag_path=self.other_cube
        )
        mesh_modifier.undo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        self.assertEqual(expected, result)

    def test_undo_extract_axes(self):
        """Test that undo after extracting axes works properly."""
        target_table = table.GeometryTable(self.test_extract_axes_cube)
        base_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        extracted_shapes = mesh_modifier.extract_axes(
            base_table=base_table, target_table=target_table
        )
        mesh_modifier.undo()

        self.assertFalse(mc.objExists(extracted_shapes[0]))
        self.assertFalse(mc.objExists(extracted_shapes[1]))
        self.assertFalse(mc.objExists(extracted_shapes[2]))
        self.assertFalse(mc.objExists(extracted_shapes[3]))

    def test_undo_flip(self):
        """Test that undo after symmetrization works properly."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="positive")
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.flip(base_table=sym_table, target_table=geo_table)
        mesh_modifier.undo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)


class TestRedo(common.BaseTest):
    def test_redo_revert_to_base(self):
        """Test that undo after revert to base works properly."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.sym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        asym_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.revert_to_base(
            base_table=sym_table, target_table=asym_table, percentage=100
        )
        mesh_modifier.undo()
        mesh_modifier.redo()

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
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.revert_to_base(
            base_table=sym_table, target_table=asym_table, percentage=100
        )
        mesh_modifier.undo()
        mesh_modifier.redo()
        mesh_modifier.undo()

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
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table)
        mesh_modifier.undo()
        mesh_modifier.redo()

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
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.bake_difference(
            sym_table, geo_table, target_dag_path=self.other_cube
        )
        mesh_modifier.undo()
        mesh_modifier.redo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        self.assertEqual(expected, result)

    def test_redo_extract_axes(self):
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))

        target_table = table.GeometryTable(self.test_extract_axes_cube)
        base_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        extracted_shapes = mesh_modifier.extract_axes(
            base_table=base_table, target_table=target_table
        )

        mesh_modifier.undo()
        mesh_modifier.redo()

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

        result_x = [
            mc.pointPosition("{}.vtx[{}]".format(extracted_shapes[0], vtx), world=True)
            for vtx in range(vtx_number)
        ]
        result_y = [
            mc.pointPosition("{}.vtx[{}]".format(extracted_shapes[1], vtx), world=True)
            for vtx in range(vtx_number)
        ]
        result_z = [
            mc.pointPosition("{}.vtx[{}]".format(extracted_shapes[2], vtx), world=True)
            for vtx in range(vtx_number)
        ]

        self.assertEqual(expected_x, result_x)
        self.assertEqual(expected_y, result_y)
        self.assertEqual(expected_z, result_z)

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
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.flip(base_table=sym_table, target_table=geo_table)
        mesh_modifier.undo()
        mesh_modifier.redo()

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)
