from sym_mesh.gui import connection_widget
from sym_mesh.gui import dockable_dialog


def startup():  # pragma: no cover
    dialog = dockable_dialog.DockableDialog.instance(
        connection_widget.ConnectionWidget
    )  # pragma: no cover
    dialog.show(dockable=True)  # pragma: no cover

    return dialog
