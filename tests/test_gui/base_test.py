import sys
from Qt import QtWidgets

from tests.fixtures import common
from gui import connector


class GUITest(common.BaseTest):
    @classmethod
    def setUpClass(cls):
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = QtWidgets.QApplication.instance()
        cls.state = common.startup_maya_session()

    def setUp(self):
        super(GUITest, self).setUp()
        self.dialog = QtWidgets.QDialog()
        self.connector = connector.Connector(self.dialog)
        self.gui = self.connector.gui
        self.dialog.show()

    def tearDown(self):
        self.dialog.close()

    @classmethod
    def tearDownClass(cls) -> None:
        del cls.app
        return super(GUITest, cls).tearDownClass()
