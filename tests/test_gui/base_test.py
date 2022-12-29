import sys
from Qt import QtWidgets

from gui import connection_widget
from tests.fixtures import common


class BaseGUITest(common.BaseTest):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication(sys.argv)
        cls.state = common.startup_maya_session()

    def setUp(self):
        super(BaseGUITest, self).setUp()
        self.dialog = QtWidgets.QDialog()
        self.connector = connection_widget.ConnectionWidget(self.dialog)
        self.gui = self.connector.gui
        self.dialog.show()

    def tearDown(self):
        self.dialog.close()
