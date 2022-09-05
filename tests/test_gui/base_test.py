import sys
from Qt import QtWidgets

from tests.fixtures import common
from gui.SymMesh_ui import SymMeshUI
from gui.controller import Controller


class GUITest(common.BaseTest):

    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication(sys.argv)
        cls.state = common.startup_maya_session()

    def setUp(self):
        super(GUITest, self).setUp()
        self.dialog = QtWidgets.QDialog()
        self.controller = Controller()
        self.gui = SymMeshUI(self.dialog, self.controller)
        self.dialog.show()

    def tearDown(self):
        self.dialog.close()
        # sys.exit()

