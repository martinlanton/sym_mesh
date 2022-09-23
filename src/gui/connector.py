from functools import partial

from gui import controller
from gui import SymMesh_ui


class Connector(object):
    def __init__(self, parent=None):
        self.ctrl = controller.Controller()
        self.gui = SymMesh_ui.SymMeshUI(parent)

        self.gui.get_base_pB.clicked.connect(self.ctrl.get_base)
        self.gui.get_target_pB.clicked.connect(self.ctrl.get_target)
        self.gui.symmetry_push_button.clicked.connect(self.ctrl.symmetrize)
        self.gui.flip_push_button.clicked.connect(self.ctrl.flip)

        store_selection = partial(self.ctrl.get_vertex_selection, self.gui.vertices_stored)
        self.gui.get_vertex_selection_push_button.clicked.connect(
            store_selection
        )

        self.gui.select_vertex_selection_push_button.clicked.connect(
            self.ctrl.select_stored_vertices
        )
        self.gui.select_non_symmetrical_vertices_push_button.clicked.connect(
            self.ctrl.select_non_mirrored_vertices
        )
        self.gui.bake_deltas_push_button.clicked.connect(self.ctrl.bake_deltas)
        # gui.revert_to_base_pB.clicked.connect(ctrl.revert_to_base)
        self.gui.revert_to_base_push_button.clicked.connect(self.ctrl.revert_to_base)
        self.gui.undo_push_button.clicked.connect(self.ctrl.undo)
        self.gui.redo_push_button.clicked.connect(self.ctrl.redo)

        set_base_line_edit = partial(self.gui.set_line_edit, self.gui.base_line_edit)
        self.ctrl.set_base.connect(set_base_line_edit)
        set_target_line_edit = partial(
            self.gui.set_line_edit, self.gui.target_line_edit
        )
        self.ctrl.set_target.connect(set_target_line_edit)
