from maya.app.general.mayaMixin import MayaQWidgetDockableMixin as dockable

from Qt import QtWidgets, QtCore


class DockableDialog(dockable, QtWidgets.QDialog):
    _instance = None

    def __init__(self, connector, parent=None):
        """

        :param connector:
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

    def keyPressEvent(self, event):
        if QtCore.Qt.Key_A <= event.key() <= QtCore.Qt.Key_Z:
            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.connector.ctrl.undo()
            elif event.modifiers() & QtCore.Qt.ControlModifier & QtCore.Qt.ShiftModifier:
                self.connector.ctrl.redo()
        else:
            QtWidgets.QWidget.keyPressEvent(self, event)
