from maya.app.general.mayaMixin import MayaQWidgetDockableMixin as dockable

from Qt import QtWidgets


class DockableDialog(dockable, QtWidgets.QDialog):
    _instance = None

    def __init__(self, connector, parent=None):
        """This dialog merely exists so that we can pass it other widgets to parent to it.

        It is mostly used for dockability in Maya.
        One thing to note is that we create a Layout inside this widget so that
        we can parent the contained widget to it. Parenting the contained widget
        without a layout does work BUT prevents the resizing of the dialog and
        the widget in relation to each other. As a consequence the dialog just
        opens tiny and its content does not resize when the dialog is
        resized.

        :param connector:
        :type connector: gui.startup.ConnectionWidget

        :param parent:
        """
        super(DockableDialog, self).__init__(parent=parent)     # pragma: no cover
        self.connector = connector(self)                        # pragma: no cover

        self.setWindowTitle("Sym Mesh")                         # pragma: no cover
        self.layout = QtWidgets.QVBoxLayout(self)               # pragma: no cover
        self.layout.addWidget(self.connector)                   # pragma: no cover

    @classmethod
    def instance(cls, connector, parent=None):
        if not cls._instance:                                   # pragma: no cover
            cls._instance = DockableDialog(connector, parent)   # pragma: no cover
        return cls._instance                                    # pragma: no cover
