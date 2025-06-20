import logging

from maya.api import OpenMaya as om2
from maya import cmds as mc
from sym_mesh.domain import selection
from sym_mesh.domain import shading
from sym_mesh.domain.commands.abstract_commands import AbstractGeometryCommand
from sym_mesh.domain.dag_path import create_MDagPath

log = logging.getLogger(__name__)


class ExtractAxesCommand(AbstractGeometryCommand):
    def __init__(
        self,
        base_table,
        target_table,
        vertex_selection=selection.VertexSelection(from_list=()),
        percentage=100,
        target_dag_path=None,
        translate=20.0,
    ):
        """Extract deltas between target table and base table on a new geometry.

        :param base_table:
        :type base_table: domain.table.GeometryTable

        :param target_table:
        :type target_table: domain.table.GeometryTable

        :param translate: value to use to translate the extracted geometry in Y
        :type translate: float
        """
        self.base_dag_path = base_table.dag_path
        self.point_arrays = list()
        self.meshes = list()
        self.translate = translate
        super().__init__(
            base_table,
            target_table,
            vertex_selection,
            percentage=percentage,
            target_dag_path=target_dag_path,
        )

    def do_it(self):
        """Extract deltas between target table and base table on a new geometry.

        :return: names of the newly created geometries
        :rtype: str, str, str
        """
        target_name = self.target_table.dag_path.fullPathName().split("|")[-1]
        base_point_array = self.base_table.point_array
        target_point_array = self.target_table.point_array

        for i, axis in enumerate(["x", "y", "z"]):
            dag_path = self.duplicate_mesh(self.base_dag_path, target_name, suffix=axis)
            path = dag_path.fullPathName()
            self.meshes.append(path)

            # Init MFnMesh
            destination_table = om2.MPointArray()

            # Loop in MPointArray
            for j in range(len(base_point_array)):
                base_point = base_point_array[j]
                target_point = target_point_array[j]
                new_point = list(base_point)
                new_point[i] = target_point[i]
                destination_table.append(new_point)
            self.point_arrays.append(destination_table)

            # Modify points position using the new coordinates
            tgt_mesh_functionset = om2.MFnMesh(dag_path)
            tgt_mesh_functionset.setPoints(destination_table, self.base_table.space)

        # Adding base point array to point arrays list for redo purposes
        self.point_arrays.append(base_point_array)

        dag_path = self.duplicate_mesh(
            self.base_dag_path, target_name, suffix="extracted"
        )
        self.meshes.append(dag_path.fullPathName())

        return self.create_blendshape()

    def duplicate_mesh(self, dag_path, name, suffix=""):
        """Duplicate the mesh at the selected dag path and rename it with the specified name.

        :param dag_path: dag path of the mesh to duplicate.
        :type dag_path: maya.api.OpenMaya.MDagPath

        :param name: name to give to the new geometry
        :type name: str

        :param suffix: suffix to add to the end of the new name
        :type suffix: str

        :return: dag path of the new mesh
        :rtype: maya.api.OpenMaya.MDagPath
        """
        mesh_function_set = om2.MFnMesh(dag_path)
        mesh = mesh_function_set.duplicate()
        duplicate_function_set = om2.MFnDagNode(mesh)
        dag_path = duplicate_function_set.getPath()
        new_path = self.get_new_name(name, dag_path, suffix=suffix)
        dag_modifier = om2.MDagModifier()
        dag_modifier.renameNode(mesh, new_path)
        dag_modifier.doIt()
        return dag_path

    def get_new_name(self, target_name, dag_path, suffix=""):
        """Renamed the dag object at the specific dag path with the specified
        name and suffix.

        :param target_name: name to give to the object.
        :type target_name: str

        :param dag_path: dag path of the object to rename.
        :type dag_path: maya.api.OpenMaya.MDagPath

        :param suffix: suffix to add at the end of the new name.
        :type suffix: str

        :return: new long name to give to the object
        :rtype: str
        """
        path = dag_path.fullPathName()
        new_path = path.rsplit("|", 1)[:-1]
        if suffix:
            target_name = "{}_{}".format(target_name, suffix)
        new_path.append(target_name)
        new_path = "|".join(new_path)
        return new_path

    def undo(self):
        node = create_MDagPath(self.result[0]).node()
        dag_modifier = om2.MDagModifier()
        dag_modifier.deleteNode(node)
        dag_modifier.doIt()

    def redo(self):
        for i, path in enumerate(self.meshes):
            name = path.split("|")[-1]
            dag_path = self.duplicate_mesh(self.base_dag_path, name)

            # Modify points position using the new coordinates
            tgt_mesh_functionset = om2.MFnMesh(dag_path)
            tgt_mesh_functionset.setPoints(self.point_arrays[i], self.base_table.space)
        mesh, blendshape = self.create_blendshape()
        return mesh, blendshape

    def create_blendshape(self):
        # TODO : update this method to use maya API 2.0 instead of cmds
        blendshape = mc.blendShape(self.meshes)[0]
        blendshape = mc.rename(blendshape, "{}_blendShape".format(self.meshes[-1]))

        # Move the mesh 20 units in Y, placing this here to avoid doing it both
        # in __init__ and redo methods
        mc.delete(self.meshes[:-1])
        position = mc.xform(
            self.target_table.dag_path.fullPathName(),
            query=True,
            worldSpace=True,
            translation=True,
        )
        new_position = [position[0], position[1] + self.translate, position[2]]
        mc.xform(self.meshes[-1], relative=True, translation=new_position)
        shading.assign_default_shader(self.meshes[-1])
        return self.meshes[-1], blendshape
