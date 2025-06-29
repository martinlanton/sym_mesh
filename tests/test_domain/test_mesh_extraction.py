import logging

from maya import cmds as mc

from sym_mesh.domain import table, executor
from sym_mesh.domain import shading
from sym_mesh.domain.commands.geometry_commands import ExtractAxesCommand
from tests.fixtures import common


log = logging.getLogger(__name__)


class TestExtractAxes(common.BaseTest):
    def test_extract_axes_creates_geometry(self):
        target_table = table.GeometryTable(self.test_extract_axes_cube)
        base_table = table.GeometryTable(self.sym_cube)
        executor_ = executor.Executor()
        extracted_mesh, blendshape = executor_.execute(
            ExtractAxesCommand, base_table=base_table, target_table=target_table
        )

        shader = shading.get_assigned_shader(extracted_mesh)

        self.assertTrue(mc.objExists(blendshape))
        self.assertEqual(
            "{}_extracted_blendShape".format(self.test_extract_axes_cube), blendshape
        )
        targets = mc.listAttr("{}.weight".format(blendshape), multi=True)
        print("Targets: ", targets)
        print("{}_x".format(self.test_extract_axes_cube))
        self.assertTrue(any("{}_x".format(self.test_extract_axes_cube) in s for s in targets))
        self.assertTrue(any("{}_y".format(self.test_extract_axes_cube) in s for s in targets))
        self.assertTrue(any("{}_z".format(self.test_extract_axes_cube) in s for s in targets))
        self.assertTrue(not mc.objExists("{}_x".format(self.test_extract_axes_cube)))
        self.assertTrue(not mc.objExists("{}_y".format(self.test_extract_axes_cube)))
        self.assertTrue(not mc.objExists("{}_z".format(self.test_extract_axes_cube)))
        self.assertEqual(
            "|{}_extracted".format(self.test_extract_axes_cube), extracted_mesh
        )
        self.assertTrue(
            mc.objExists("|{}_extracted".format(self.test_extract_axes_cube))
        )
        self.assertIn(shader, ["lambert1", "standardSurface1"])

    def test_extract_axes_geometries_point_positions(self):
        target_table = table.GeometryTable(self.test_extract_axes_cube)
        base_table = table.GeometryTable(self.sym_cube)
        executor_ = executor.Executor()
        extracted_mesh, blendshape = executor_.execute(
            ExtractAxesCommand, base_table=base_table, target_table=target_table
        )
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
        expected_pos = [10, 30, 10]
        pos = mc.xform(extracted_mesh, query=True, translation=True)

        self.assertEqual(expected_x, x)
        self.assertEqual(expected_y, y)
        self.assertEqual(expected_z, z)
        self.assertEqual(expected_pos, pos)

    def test_extract_axes_geometry_translate(self):
        target_table = table.GeometryTable(self.test_extract_axes_cube)
        base_table = table.GeometryTable(self.sym_cube)
        executor_ = executor.Executor()
        extracted_mesh, blendshape = executor_.execute(
            ExtractAxesCommand,
            base_table=base_table,
            target_table=target_table,
            translate=40,
        )

        expected_pos = [10, 50, 10]
        pos = mc.xform(extracted_mesh, query=True, translation=True)

        self.assertEqual(expected_pos, pos)

    # def test_timing_extract_axes(self):
    #     """Uncomment to test the performance of the extraction.
    #     This is a long-running test, so it is commented out by default.
    #     """
    #     import time
    #     from sym_mesh import dag_path
    #     from maya.api import OpenMaya as om2
    #     cube1 = mc.polyCube(sx=10, sy=30, sz=100, ch=False)[0]
    #     cube2 = mc.polyCube(sx=10, sy=30, sz=100, ch=False)[0]
    #     base_table = table.GeometryTable(cube1)
    #     base_point_array = base_table.point_array
    #     dag_path = dag_path.create_MDagPath(cube2)
    #     tgt_mesh_functionset = om2.MFnMesh(dag_path)
    #     destination_table = om2.MPointArray()
    #     for i in range(self.vtx_number):
    #         # Modify new position
    #         base_position = base_point_array[i]
    #         new_position = [pos + 1 for pos in base_position]
    #         destination_table.append(new_position)
    #     tgt_mesh_functionset.setPoints(destination_table, om2.MSpace.kObject)
    #
    #     before = time.time()
    #     target_table = table.GeometryTable(cube2)
    #     executor_ = executor.MeshModifier()
    #     extracted_shapes = executor_.execute(ExtractAxesCommand,
    #         base_table=base_table, target_table=target_table
    #     )
    #     after = time.time()
    #     log.critical("It took %s seconds", (after-before))
