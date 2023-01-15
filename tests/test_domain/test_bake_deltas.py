import logging

from maya import cmds as mc

from domain import executor, selection, table
from domain.commands.deformation_commands import BakeDifferenceCommand
from tests.fixtures import common

logging.basicConfig()
log = logging.getLogger(__name__)


class TestBakeDeltas(common.BaseTest):
    def test_bake_delta(self):
        """Test that baking delta functions properly on one geometry."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        executor_ = executor.Executor()
        executor_.execute(
            BakeDifferenceCommand,
            base_table=sym_table,
            target_table=geo_table,
            target_dag_path=self.other_cube,
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        self.assertEqual(self.expected_asym_position, result)

    def test_bake_delta_zero_percent(self):
        """Test that baking delta functions properly on one geometry."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        executor_ = executor.Executor()
        executor_.execute(
            BakeDifferenceCommand,
            base_table=sym_table,
            target_table=geo_table,
            percentage=0,
            target_dag_path=self.other_cube,
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        self.assertEqual(self.expected_sym_position, result)

    def test_bake_deltas_with_vertex_selection(self):
        """Test that baking the deltas on a mesh when a proper vertex selection is
        provided only bakes the deltas for the selected vertices."""
        sym_table = table.GeometryTable(self.sym_cube)
        geo_table = table.GeometryTable(self.asym_cube)
        mc.select("{}.vtx[1]".format(self.asym_cube))
        vertex_selection = selection.VertexSelection()
        executor_ = executor.Executor()
        executor_.execute(
            BakeDifferenceCommand,
            base_table=sym_table,
            target_table=geo_table,
            vertex_selection=vertex_selection,
            target_dag_path=self.other_cube,
        )

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

        log.info("Symmetry table : %s", sym_table.symmetry_table)
        log.info("Expected : %s", expected_sym_position)
        log.info("Result : %s", result)
        self.assertEqual(expected_sym_position, result)

    def test_bake_delta_with_no_vertex_selection(self):
        """Test that baking the deltas on a mesh when a proper vertex selection is
        provided only bakes the deltas for the selected vertices."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mc.select(clear=True)
        vertex_selection = selection.VertexSelection()
        executor_ = executor.Executor()
        executor_.execute(
            BakeDifferenceCommand,
            base_table=sym_table,
            target_table=geo_table,
            vertex_selection=vertex_selection,
            target_dag_path=self.other_cube,
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        self.assertEqual(self.expected_asym_position, result)

    def test_bake_delta_with_geometry_selected_for_vertex_selection(self):
        """Test that baking delta functions properly on one geometry."""
        geo_table = table.GeometryTable(self.asym_cube)
        sym_table = table.GeometryTable(self.sym_cube)
        mc.select(self.asym_cube)
        vertex_selection = selection.VertexSelection()
        executor_ = executor.Executor()
        executor_.execute(
            BakeDifferenceCommand,
            base_table=sym_table,
            target_table=geo_table,
            vertex_selection=vertex_selection,
            target_dag_path=self.other_cube,
        )

        result = [
            mc.pointPosition("{}.vtx[{}]".format(self.other_cube, vtx), world=True)
            for vtx in range(self.vtx_number)
        ]
        self.assertEqual(self.expected_asym_position, result)
