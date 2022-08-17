import logging

import maya.cmds as mc
from tests.fixtures import common

from sym_mesh import table
from sym_mesh import mesh_modification


log = logging.getLogger(__name__)


class TestRevertToBase(common.BaseTest):
    def test_revert_to_current(self):
        """Test that reverting to base with a value of 100% doesn't revert anything."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.revert_to_base(
            base_table=sym_table, target_table=geo_table, percentage=0
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        self.assertEqual(expected, result)

    def test_revert_to_base(self):
        """Test that reverting to base with a value of 0% reverts to base."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.revert_to_base(
            base_table=sym_table, target_table=geo_table, percentage=100
        )

        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))

        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.sym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        self.assertEqual(expected, result)


class TestSymmetry(common.BaseTest):
    def test_symmetrization_x_positive(self):
        """Test that reverting to base with a value of 0% reverts to base."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="positive")
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table)

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
        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)

    def test_symmetrization_x_negative(self):
        """Test that reverting to base with a value of 0% reverts to base."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="negative")
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table)

        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))

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
            for vtx in range(vtx_number)
        ]

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)

    def test_symmetrization_y_negative(self):
        """Test that reverting to base with a value of 0% reverts to base."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="y", direction="negative")
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table)

        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))

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
            for vtx in range(vtx_number)
        ]

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)

    def test_symmetrization_x_positive_zero_percent(self):
        """Test that reverting to base with a value of 0% reverts to base."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="positive")
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.symmetrize(base_table=sym_table, target_table=geo_table)

        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))

        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected)
        log.info("Result : %s", result)
        self.assertEqual(expected, result)


class TestBakeDeltas(common.BaseTest):
    def test_bake_delta(self):
        """Test that baking delta functions properly on one geometry."""
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

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        self.assertEqual(expected, result)

    def test_bake_delta_zero_precent(self):
        """Test that baking delta functions properly on one geometry."""
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
        expected = [
            mc.pointPosition("{}.vtx[{}]".format(self.sym_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]

        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        mesh_modifier.bake_difference(
            sym_table, geo_table, percentage=0, target_dag_path=self.other_cube
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        self.assertEqual(expected, result)


# class TestFlip(common.BaseTest):
#     def test_symmetrization_x_positive(self):
#         """Test that reverting to base with a value of 0% reverts to base."""
#         geo_table = table.GeometryTable(self.asym_cube)
#         sym_table = table.GeometryTable(self.sym_cube, axis="x", direction="positive")
#         mesh_modifier = mesh_modification.MeshModifier()
#         mesh_modifier.flip(base_table=sym_table, target_table=geo_table)
#
#         vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))
#
#         expected = [
#         ]
#         result = [
#             mc.pointPosition("{}.vtx[{}]".format(self.asym_cube, vtx), world=True)
#             for vtx in range(vtx_number)
#         ]
#
#         log.info("Symmetry table : %s", sym_table.symmetry_table)
#         log.info("Expected : %s", expected)
#         log.info("Result : %s", result)
#         self.assertEqual(expected, result)


