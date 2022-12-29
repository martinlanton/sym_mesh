import logging
from maya import cmds as mc

from domain import selection
from tests.fixtures import common

log = logging.getLogger(__name__)


class TestVertexSelection(common.BaseTest):
    # TODO : add error test when creating a VertexSelection with an active
    #  selection containing more than one mesh.

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
