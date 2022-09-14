from gui import controller
from gui import SymMesh_ui


class Connector(object):
    def __init__(self, parent=None):
        self.ctrl = controller.Controller()
        self.gui = SymMesh_ui.SymMeshUI(parent)

        self.gui.get_base_pB.clicked.connect(self.ctrl.get_base)
        # gui.get_target_pB.clicked.connect(ctrl.get_target)
        self.gui.symmetry_push_button.clicked.connect(self.ctrl.symmetrize)
        self.gui.flip_push_button.clicked.connect(self.ctrl.flip)
        # gui.get_selected_vtcs_pB.clicked.connect(ctrl.get_vtcs_selection)
        # gui.select_stored_vtcs_pB.clicked.connect(ctrl.select_stored_vertices)
        # gui.select_non_symmetrical_vtcs_pB.clicked.connect(
        #     ctrl.select_non_mirrored_vertices
        # )
        # gui.bake_diff_pB.clicked.connect(ctrl.bake_difference)
        # gui.revert_to_base_pB.clicked.connect(ctrl.revert_to_base)
        self.gui.revert_to_base_push_button.clicked.connect(self.ctrl.revert_to_base)
        self.gui.undo_push_button.clicked.connect(self.ctrl.undo)
