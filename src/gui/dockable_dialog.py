from maya.app.general.mayaMixin import MayaQWidgetDockableMixin as dockable

from Qt import QtWidgets


class DockableDialog(dockable, QtWidgets.QDialog):
    _instance = None

    def __init__(self, connector, parent=None):
        """

        :param connector:
        :type connector: gui.startup.ConnectionWidget

        :param parent:
        """
        super(DockableDialog, self).__init__(parent=parent)  # pragma: no cover
        # TODO : fix problem with dialog not resizing to the ConnectionWidget's size
        self.connector = connector(self)  # pragma: no cover

        self.setWindowTitle("Sym Mesh")  # pragma: no cover

    @classmethod
    def instance(cls, connector, parent=None):
        if not cls._instance:  # pragma: no cover
            cls._instance = DockableDialog(connector, parent)  # pragma: no cover
        return cls._instance  # pragma: no cover
