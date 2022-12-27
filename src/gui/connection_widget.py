from functools import partial
from Qt import QtWidgets, QtCore

from gui import controller
from gui import SymMesh_ui


class ConnectionWidget(QtWidgets.QGroupBox):
    """Group box that can be parented to a dialog to open it in Maya or other DCCs."""

    def __init__(self, parent=None):
        super(ConnectionWidget, self).__init__(parent)

        self.ctrl = controller.Controller()
        self.gui = SymMesh_ui.Layout(self)

        self.gui.threshold_sb.valueChanged.connect(self.set_threshold)
        self.gui.direction_rb_group.buttonReleased.connect(self.set_direction)
        self.gui.axis_rb_group.buttonReleased.connect(self.set_axis)

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

    def keyPressEvent(self, event):
        """Overriding this method is necessary to force the key event to be accepted.

        This is necessary to set up shortcuts.

        """
        if event.key() == QtCore.Qt.Key_Z:
            if event.modifiers() == QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier:
                self.ctrl.redo()
                return event.accept()
            elif event.modifiers() & QtCore.Qt.ControlModifier:
                self.ctrl.undo()
                return event.accept()

        return super(ConnectionWidget, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        """Overriding this method is necessary to force the focus on the widget when clicking it.

        Without the widget focused, then Maya takes the priority for all key press events

        """
        super(ConnectionWidget, self).mousePressEvent(event)
        self.setFocus()

    def set_threshold(self, value):
        self.ctrl.threshold = value

    def set_direction(self, button):
        button_text = button.text()
        direction = button_text.split(":")[0].lower()
        self.ctrl.direction = direction

    def set_axis(self, button):
        button_text = button.text()
        axis = button_text.split(" : ")[-1].lower()
        self.ctrl.axis = axis
