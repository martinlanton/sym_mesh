import logging
from maya import cmds as mc

from sym_mesh.domain import selection
from tests.fixtures import common

log = logging.getLogger(__name__)


class TestVertexSelection(common.BaseTest):
    def test_selecting_empty_stored_vertices(self):
        mc.select(clear=True)

        vtx_selection = selection.VertexSelection()
        mc.select(clear=True)

        vtx_selection.select()

        result = mc.ls(sl=True)
        expected = []

        self.assertEqual(expected, result)

    def test_selecting_stored_vertices(self):
        to_select = []
        for vtx in [1, 3, 5, 7]:
            to_select.append("{}.vtx[{}]".format(self.test_extract_axes_cube, vtx))
        mc.select(to_select)

        vtx_selection = selection.VertexSelection()
        mc.select(clear=True)

        vtx_selection.select()

        result = mc.ls(sl=True)
        expected = to_select

        self.assertEqual(expected, result)

    def test_selecting_stored_vertices_for_multiple_selection(self):
        to_select = []
        to_not_select = []
        for vtx in [1, 3, 5, 7]:
            to_select.append("{}.vtx[{}]".format(self.test_extract_axes_cube, vtx))
            to_not_select.append("{}.vtx[{}]".format(self.sym_cube, vtx))
        mc.select(to_select)

        vtx_selection = selection.VertexSelection()
        mc.select(clear=True)

        vtx_selection.select()

        result = mc.ls(sl=True)
        expected = to_select

        self.assertEqual(expected, result)
