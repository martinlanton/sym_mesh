import logging

from maya.api import OpenMaya as om2
from sym_mesh.domain.dag_path import create_MDagPath

log = logging.getLogger(__name__)


class ExtractAxesCommand(object):
    def __init__(self, base_table, target_table):
        self.point_arrays = list()
        self.base_dag_path = base_table.dag_path
        self.result = self.extract_axes(base_table, target_table)

    def extract_axes(self, base_table, target_table):
        """Extract deltas between target table and base table on a new geometry.

        :param base_table:
        :type base_table: sym_mesh.table.GeometryTable

        :param target_table:
        :type target_table: sym_mesh.table.GeometryTable

        :return: names of the newly created geometries
        :rtype: str, str, str
        """
        target_name = target_table.dag_path.fullPathName().split("|")[-1]
        base_point_array = base_table.point_array
        target_point_array = target_table.point_array

        pathes = list()
        for i, axis in enumerate(["x", "y", "z"]):
            dag_path = self.duplicate_mesh(self.base_dag_path, target_name, suffix=axis)
            path = dag_path.fullPathName()
            pathes.append(path)

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
            tgt_mesh_functionset.setPoints(destination_table, om2.MSpace.kObject)

        # TODO : add duplicated meshes as blendshapes to the last duplicated one
        # TODO : move the last duplicated mesh up from the position of the target
        # TODO : add an option to automatically delete the x, y, z shapes
        # TODO : add an option to reassign the shader or assign the default lambert????

        # Adding base point array to point arrays list for redo purposes
        self.point_arrays.append(base_point_array)

        dag_path = self.duplicate_mesh(self.base_dag_path, target_name, suffix="extracted")
        pathes.append(dag_path.fullPathName())

        return pathes

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
        new_x_path = self.get_new_name(name, dag_path, suffix=suffix)
        dag_modifier = om2.MDagModifier()
        dag_modifier.renameNode(mesh, new_x_path)
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
        for path in self.result:
            node = create_MDagPath(path).node()
            dag_modifier = om2.MDagModifier()
            dag_modifier.deleteNode(node)
            dag_modifier.doIt()

    def redo(self):
        for i, path in enumerate(self.result):
            name = path.split("|")[-1]
            dag_path = self.duplicate_mesh(self.base_dag_path, name)

            # Modify points position using the new coordinates
            tgt_mesh_functionset = om2.MFnMesh(dag_path)
            tgt_mesh_functionset.setPoints(self.point_arrays[i], om2.MSpace.kObject)
