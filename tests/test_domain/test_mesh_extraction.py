import logging

from maya import cmds as mc

from domain import table
from domain import mesh_modification
from tests.fixtures import common


log = logging.getLogger(__name__)


class TestExtractAxes(common.BaseTest):
    def test_extract_axes_creates_geometry(self):
        target_table = table.GeometryTable(self.test_extract_axes_cube)
        base_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        extracted_mesh, blendshape = mesh_modifier.extract_axes(
            base_table=base_table, target_table=target_table
        )

        self.assertTrue(mc.objExists(blendshape))
        self.assertEqual("{}_extracted_blendShape".format(self.test_extract_axes_cube), blendshape)
        targets = mc.listAttr("{}.weight".format(blendshape), multi=True)
        self.assertTrue("{}_x".format(self.test_extract_axes_cube) in targets)
        self.assertTrue("{}_y".format(self.test_extract_axes_cube) in targets)
        self.assertTrue("{}_z".format(self.test_extract_axes_cube) in targets)
        self.assertTrue(not mc.objExists("{}_x".format(self.test_extract_axes_cube)))
        self.assertTrue(not mc.objExists("{}_y".format(self.test_extract_axes_cube)))
        self.assertTrue(not mc.objExists("{}_z".format(self.test_extract_axes_cube)))
        self.assertEqual(
            "|{}_extracted".format(self.test_extract_axes_cube), extracted_mesh
        )
        self.assertTrue(
            mc.objExists("|{}_extracted".format(self.test_extract_axes_cube))
        )

    def test_extract_axes_geometries_point_positions(self):
        vtx_number = len(mc.ls("{}.vtx[*]".format(self.sym_cube), flatten=True))

        target_table = table.GeometryTable(self.test_extract_axes_cube)
        base_table = table.GeometryTable(self.sym_cube)
        mesh_modifier = mesh_modification.MeshModifier()
        extracted_mesh, blendshape = mesh_modifier.extract_axes(
            base_table=base_table, target_table=target_table
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

        mc.setAttr("{}.{}_x".format(blendshape, self.test_extract_axes_cube), 1)
        result_x = [
            mc.pointPosition("{}.vtx[{}]".format(extracted_mesh, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        mc.setAttr("{}.{}_x".format(blendshape, self.test_extract_axes_cube), 0)

        mc.setAttr("{}.{}_y".format(blendshape, self.test_extract_axes_cube), 1)
        result_y = [
            mc.pointPosition("{}.vtx[{}]".format(extracted_mesh, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        mc.setAttr("{}.{}_y".format(blendshape, self.test_extract_axes_cube), 0)

        mc.setAttr("{}.{}_z".format(blendshape, self.test_extract_axes_cube), 1)
        result_z = [
            mc.pointPosition("{}.vtx[{}]".format(extracted_mesh, vtx), world=True)
            for vtx in range(vtx_number)
        ]
        mc.setAttr("{}.{}_z".format(blendshape, self.test_extract_axes_cube), 0)

        self.assertEqual(expected_x, result_x)
        self.assertEqual(expected_y, result_y)
        self.assertEqual(expected_z, result_z)

    # def test_timing_extract_axes(self):
    #     import time
    #     from sym_mesh import dag_path
    #     from maya.api import OpenMaya as om2
    #     cube1 = mc.polyCube(sx=10, sy=30, sz=100, ch=False)[0]
    #     cube2 = mc.polyCube(sx=10, sy=30, sz=100, ch=False)[0]
    #     vtx_number = len(mc.ls("{}.vtx[*]".format(cube1), flatten=True))
    #     base_table = table.GeometryTable(cube1)
    #     base_point_array = base_table.point_array
    #     dag_path = dag_path.create_MDagPath(cube2)
    #     tgt_mesh_functionset = om2.MFnMesh(dag_path)
    #     destination_table = om2.MPointArray()
    #     for i in range(vtx_number):
    #         # Modify new position
    #         base_position = base_point_array[i]
    #         new_position = [pos + 1 for pos in base_position]
    #         destination_table.append(new_position)
    #     tgt_mesh_functionset.setPoints(destination_table, om2.MSpace.kObject)
    #
    #     before = time.time()
    #     target_table = table.GeometryTable(cube2)
    #     mesh_modifier = mesh_modification.MeshModifier()
    #     extracted_shapes = mesh_modifier.extract_axes(
    #         base_table=base_table, target_table=target_table
    #     )
    #     after = time.time()
    #     log.critical("It took %s seconds", (after-before))
