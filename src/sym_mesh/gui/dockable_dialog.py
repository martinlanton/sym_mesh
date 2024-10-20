from maya.app.general.mayaMixin import MayaQWidgetDockableMixin as dockable

from qtpy import QtWidgets


class DockableDialog(dockable, QtWidgets.QDialog):
    _instance = None

    def __init__(self, connector, parent=None):
        """This dialog merely exists so that we can pass it other widgets to parent to it.

        It is used for dockability in Maya.

        Notes :
        - we create a Layout inside this widget so that
        we can parent the contained widget to it. Parenting the contained widget
        without a layout does work BUT prevents the resizing of the dialog and
        the widget in relation to each other. As a consequence the dialog just
        opens tiny and its content does not resize when the dialog is
        resized.
        - this window is required for dockability in Maya, however it requires
        Maya's GUI to be open, which makes it unsuitable for automated testing,
        this is why all the key event and connections between the gui objects
        and the controller have been done inside the ConnectionWidget itself.

        :param connector: Class in charge of connecting the functionality of the layout to the controller.
        :type connector: sym_mesh.gui.connection_widget.ConnectionWidget

        :param parent:
        """
        super(DockableDialog, self).__init__(parent=parent)  # pragma: no cover
        self.connector = connector(self)  # pragma: no cover

        self.setWindowTitle("Sym Mesh")  # pragma: no cover
        self.layout = QtWidgets.QVBoxLayout(self)  # pragma: no cover
        self.layout.addWidget(self.connector)  # pragma: no cover

    @classmethod
    def instance(cls, connector, parent=None):
        if not cls._instance:  # pragma: no cover
            cls._instance = DockableDialog(connector, parent)  # pragma: no cover
        return cls._instance  # pragma: no cover
