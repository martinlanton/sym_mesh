import sys
from Qt import QtWidgets

from tests.fixtures import common
from gui.SymMesh_ui import SymMeshUI
from gui.controller import Controller


class GUITest(common.BaseTest):
    def setUp(self):
        super(GUITest, self).setUp()
        app = QtWidgets.QApplication(sys.argv)
        dialog = QtWidgets.QDialog()
        self.controller = Controller()
        self.gui = SymMeshUI(dialog, self.controller)
        dialog.show()
        sys.exit(app.exec_())
