from maya.app.general.mayaMixin import MayaQWidgetDockableMixin as dockable

from Qt import QtWidgets


class DockableDialog(dockable, QtWidgets.QDialog):
    _instance = None

    def __init__(self, connector, parent=None):
        """

        :param connector: Class in charge of connecting the functionality of the layout to the controller.
        :type connector: gui.startup.Connector

        :param parent:
        """
        super(DockableDialog, self).__init__(parent=parent)  # pragma: no cover
        self.connector = connector(self)  # pragma: no cover

        self.setWindowTitle("Sym Mesh")  # pragma: no cover

    @classmethod
    def instance(cls, connector, parent=None):
        if not cls._instance:  # pragma: no cover
            cls._instance = DockableDialog(connector, parent)  # pragma: no cover
        return cls._instance  # pragma: no cover
