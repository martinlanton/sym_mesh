from gui.connection_widget import ConnectionWidget
from gui.dockable_dialog import DockableDialog


def startup():  # pragma: no cover
    dialog = DockableDialog.instance(ConnectionWidget)  # pragma: no cover
    dialog.show(dockable=True)  # pragma: no cover

    return dialog
