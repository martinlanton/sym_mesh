from maya.app.general.mayaMixin import MayaQWidgetDockableMixin as dockable

from Qt import QtWidgets


class DockableDialog(dockable, QtWidgets.QDialog):
    _instance = None

    def __init__(self, connector, parent=None):
        """

        :param connector:
        :type connector: gui.startup.Connector

        :param parent:
        """
        super(DockableDialog, self).__init__(parent=parent)
        self.connector = connector(self)

        self.setWindowTitle("Sym Mesh")

    @classmethod
    def instance(cls, connector, parent=None):
        if not cls._instance:
            cls._instance = DockableDialog(connector, parent)
        return cls._instance
