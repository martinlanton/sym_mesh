import sys
from Qt import QtWidgets

from tests.fixtures import common
from gui import connector


class GUITest(common.BaseTest):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication(sys.argv)
        cls.state = common.startup_maya_session()

    def setUp(self):
        super(GUITest, self).setUp()
        self.dialog = QtWidgets.QDialog()
        self.connector = connector.Connector(self.dialog)
        self.gui = self.connector.gui
        self.dialog.show()

    def tearDown(self):
        self.dialog.close()
