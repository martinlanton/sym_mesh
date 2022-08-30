from tests.fixtures import common
from gui.SymMesh_ui import SymMeshUI
from gui.controller import Controller


class GUITest(common.BaseTest):
    def setUp(self):
        super(GUITest, self).setUp()
        self.controller = Controller
        self.gui = SymMeshUI(self.controller)

