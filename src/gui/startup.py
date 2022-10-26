from functools import partial

from gui import controller
from gui import SymMesh_ui
from gui.dockable_dialog import DockableDialog
from Qt import QtWidgets, QtCore


class Connector(object):
    def __init__(self, parent=None):
        self.ctrl = controller.Controller()
        self.gui = SymMesh_ui.Layout(parent)

        self.gui.get_base_pb.clicked.connect(self.ctrl.get_base)
        self.gui.get_target_pb.clicked.connect(self.ctrl.get_target)

        self.gui.symmetry_pb.clicked.connect(self.ctrl.symmetrize)
        self.gui.flip_pb.clicked.connect(self.ctrl.flip)
        self.gui.extract_axes_pb.clicked.connect(self.ctrl.extract_axes)
        self.gui.bake_deltas_pb.clicked.connect(self.ctrl.bake_deltas)
        self.gui.revert_to_base_pb.clicked.connect(self.ctrl.revert_to_base)

        store_selection = partial(
            self.ctrl.get_vertex_selection, self.gui.vertices_are_stored
        )
        self.gui.get_vertex_selection_pb.clicked.connect(store_selection)

        self.gui.select_vertex_selection_pb.clicked.connect(
            self.ctrl.select_stored_vertices
        )
        self.gui.select_non_symmetrical_vertices_pb.clicked.connect(
            self.ctrl.select_non_mirrored_vertices
        )

        self.gui.undo_push_button.clicked.connect(self.ctrl.undo)
        self.gui.redo_push_button.clicked.connect(self.ctrl.redo)

        set_base_line_edit = partial(self.gui.set_line_edit, self.gui.base_line_edit)
        self.ctrl.set_base.connect(set_base_line_edit)
        set_target_line_edit = partial(
            self.gui.set_line_edit, self.gui.target_line_edit
        )
        self.ctrl.set_target.connect(set_target_line_edit)

        # self.undo_action = QtWidgets.QAction("undo", self)
        # self.undo_action.setShortcut("Ctrl+Z")
        # self.undo_action.triggered.connect(self.ctrl.undo)

    def keyPressEvent(self, event):
        if QtCore.Qt.Key_A <= event.key() <= QtCore.Qt.Key_Z:
            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.ctrl.undo()
            elif event.modifiers() & QtCore.Qt.ControlModifier & QtCore.Qt.ShiftModifier:
                self.ctrl.redo()
        else:
            QtWidgets.QWidget.keyPressEvent(self, event)


def startup():  # pragma: no cover
    dialog = DockableDialog.instance(Connector)  # pragma: no cover
    dialog.show(dockable=True)  # pragma: no cover
