import logging
from Qt import QtWidgets, QtCore

log = logging.getLogger("SymUI")
log.setLevel(logging.INFO)


class SymMeshUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """

        :param parent:

        """
        super(SymMeshUI, self).__init__(parent=parent)

        self.setWindowTitle("SymMesh UI")
        # UI
        self.buildUI()

        # self.revert_value_slider.valueChanged.connect(self.get_spinBox_value)
        # self.revert_value_sB.valueChanged.connect(self.get_slider_value)

        self.vertices_stored = False

    def buildUI(self):
        log.info("Building UI")
        self.layout = QtWidgets.QVBoxLayout(self)

        # Get base
        self.get_base_pB = QtWidgets.QPushButton("Get Base")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(self.get_base_pB.sizePolicy().hasHeightForWidth())
        self.get_base_pB.setSizePolicy(sizePolicy)
        self.get_base_pB.setMinimumSize(QtCore.QSize(0, 25))
        self.get_base_pB.setObjectName("get_base_pB")
        self.layout.addWidget(self.get_base_pB)

        self.base_line_edit = QtWidgets.QLineEdit("base")
        self.base_line_edit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(self.base_line_edit.sizePolicy().hasHeightForWidth())
        self.base_line_edit.setSizePolicy(sizePolicy)
        self.base_line_edit.setMinimumSize(QtCore.QSize(0, 25))
        self.base_line_edit.setObjectName("base_line_edit")
        self.layout.addWidget(self.base_line_edit)

        # Get target
        self.get_target_pB = QtWidgets.QPushButton("Get Target")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.get_target_pB.sizePolicy().hasHeightForWidth()
        )
        self.get_target_pB.setSizePolicy(sizePolicy)
        self.get_target_pB.setMinimumSize(QtCore.QSize(0, 25))
        self.get_target_pB.setObjectName("get_target_pB")
        self.layout.addWidget(self.get_target_pB)

        self.target_line_edit = QtWidgets.QLineEdit("target")
        self.target_line_edit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(self.target_line_edit.sizePolicy().hasHeightForWidth())
        self.target_line_edit.setSizePolicy(sizePolicy)
        self.target_line_edit.setMinimumSize(QtCore.QSize(0, 25))
        self.target_line_edit.setObjectName("target_line_edit")
        self.layout.addWidget(self.target_line_edit)

        # Store vertices selection
        self.get_vertex_selection_push_button = QtWidgets.QPushButton("Get Vtx Selection")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.get_vertex_selection_push_button.sizePolicy().hasHeightForWidth()
        )
        self.get_vertex_selection_push_button.setSizePolicy(sizePolicy)
        self.get_vertex_selection_push_button.setMinimumSize(QtCore.QSize(0, 25))
        self.get_vertex_selection_push_button.setObjectName("get_vertex_selection_push_button")
        self.layout.addWidget(self.get_vertex_selection_push_button)

        self.get_vertex_selection_push_button.clicked.connect(self.store_selection)

        # Select non-symmetrical vertices
        self.select_non_symmetrical_vertices_push_button = QtWidgets.QPushButton(
            "Select Non Symmetrical Vtcs"
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.select_non_symmetrical_vertices_push_button.sizePolicy().hasHeightForWidth()
        )
        self.select_non_symmetrical_vertices_push_button.setSizePolicy(sizePolicy)
        self.select_non_symmetrical_vertices_push_button.setMinimumSize(QtCore.QSize(0, 25))
        self.select_non_symmetrical_vertices_push_button.setObjectName(
            "select_non_symmetrical_vtcs_pB"
        )
        self.layout.addWidget(self.select_non_symmetrical_vertices_push_button)

        # Select stored vertex selection
        self.select_vertex_selection_push_button = QtWidgets.QPushButton("Select stored Vtcs")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.select_vertex_selection_push_button.sizePolicy().hasHeightForWidth()
        )
        self.select_vertex_selection_push_button.setSizePolicy(sizePolicy)
        self.select_vertex_selection_push_button.setMinimumSize(QtCore.QSize(0, 25))
        self.select_vertex_selection_push_button.setObjectName("select_stored_vtcs_pB")
        self.layout.addWidget(self.select_vertex_selection_push_button)

        # Bake deltas
        self.bake_deltas_push_button = QtWidgets.QPushButton("Bake Deltas")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(self.bake_deltas_push_button.sizePolicy().hasHeightForWidth())
        self.bake_deltas_push_button.setSizePolicy(sizePolicy)
        self.bake_deltas_push_button.setMinimumSize(QtCore.QSize(0, 25))
        self.bake_deltas_push_button.setObjectName("bake_deltas_pB")
        self.layout.addWidget(self.bake_deltas_push_button)

        # Symmetry
        self.symmetry_push_button = QtWidgets.QPushButton("Symmetry")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.symmetry_push_button.sizePolicy().hasHeightForWidth()
        )
        self.symmetry_push_button.setSizePolicy(sizePolicy)
        self.symmetry_push_button.setMinimumSize(QtCore.QSize(0, 25))
        self.symmetry_push_button.setObjectName("symmetry_pB")
        self.layout.addWidget(self.symmetry_push_button)

        # Flip
        self.flip_push_button = QtWidgets.QPushButton("Flip")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.flip_push_button.sizePolicy().hasHeightForWidth()
        )
        self.flip_push_button.setSizePolicy(sizePolicy)
        self.flip_push_button.setMinimumSize(QtCore.QSize(0, 25))
        self.flip_push_button.setObjectName("flip_pB")
        self.layout.addWidget(self.flip_push_button)

        # # Revert value
        # self.horizontalLayout = QtWidgets.QHBoxLayout()
        # self.horizontalLayout.setObjectName("horizontalLayout")
        # self.layout.addLayout(self.horizontalLayout)
        #
        # self.revert_value_slider = QtWidgets.QSlider()
        # sizePolicy = QtWidgets.QSizePolicy(
        #     QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        # )
        # sizePolicy.setHeightForWidth(
        #     self.revert_value_slider.sizePolicy().hasHeightForWidth()
        # )
        # self.revert_value_slider.setSizePolicy(sizePolicy)
        # self.revert_value_slider.setMinimumSize(QtCore.QSize(0, 25))
        # self.revert_value_slider.setMaximum(100)
        # self.revert_value_slider.setProperty("value", 100)
        # self.revert_value_slider.setOrientation(QtCore.Qt.Horizontal)
        # self.revert_value_slider.setObjectName("percentage_slider")
        # self.horizontalLayout.addWidget(self.revert_value_slider)
        #
        # self.revert_value_sB = QtWidgets.QSpinBox()
        # sizePolicy = QtWidgets.QSizePolicy(
        #     QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        # )
        # sizePolicy.setHeightForWidth(
        #     self.revert_value_sB.sizePolicy().hasHeightForWidth()
        # )
        # self.revert_value_sB.setSizePolicy(sizePolicy)
        # self.revert_value_sB.setMinimumSize(QtCore.QSize(0, 25))
        # self.revert_value_sB.setMaximum(100)
        # self.revert_value_sB.setProperty("value", 100)
        # self.revert_value_sB.setObjectName("percentage_sB")
        # self.horizontalLayout.addWidget(self.revert_value_sB)
        #
        # # Revert to base from target
        # self.revert_to_base_pB = QtWidgets.QPushButton("Revert sel to base (target)")
        # sizePolicy = QtWidgets.QSizePolicy(
        #     QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        # )
        # sizePolicy.setHeightForWidth(
        #     self.revert_to_base_pB.sizePolicy().hasHeightForWidth()
        # )
        # self.revert_to_base_pB.setSizePolicy(sizePolicy)
        # self.revert_to_base_pB.setMinimumSize(QtCore.QSize(0, 25))
        # self.revert_to_base_pB.setObjectName("revert_to_base_pB")
        # self.layout.addWidget(self.revert_to_base_pB)

        # Revert to base on selection
        self.revert_to_base_push_button = QtWidgets.QPushButton(
            "Revert sel to base (live)"
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.revert_to_base_push_button.sizePolicy().hasHeightForWidth()
        )
        self.revert_to_base_push_button.setSizePolicy(sizePolicy)
        self.revert_to_base_push_button.setMinimumSize(QtCore.QSize(0, 25))
        self.revert_to_base_push_button.setObjectName("revert_to_base_live_pB")
        self.layout.addWidget(self.revert_to_base_push_button)

        # Undo
        self.undo_push_button = QtWidgets.QPushButton("Undo")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(self.undo_push_button.sizePolicy().hasHeightForWidth())
        self.undo_push_button.setSizePolicy(sizePolicy)
        self.undo_push_button.setMinimumSize(QtCore.QSize(0, 25))
        self.undo_push_button.setObjectName("undo_pB")
        self.layout.addWidget(self.undo_push_button)

        # Redo
        self.redo_push_button = QtWidgets.QPushButton("Redo")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(self.redo_push_button.sizePolicy().hasHeightForWidth())
        self.redo_push_button.setSizePolicy(sizePolicy)
        self.redo_push_button.setMinimumSize(QtCore.QSize(0, 25))
        self.redo_push_button.setObjectName("redo_push_button")
        self.layout.addWidget(self.redo_push_button)

        # Tooltips
        self.revert_to_base_push_button.setToolTip(
            QtWidgets.QApplication.translate(
                "MainWindow",
                "Revert selected mesh or vertices to base, from current position.",
                None,
            )
        )
        self.undo_push_button.setToolTip(
            QtWidgets.QApplication.translate(
                "MainWindow",
                "Undo the last action.",
                None,
            )
        )
        self.redo_push_button.setToolTip(
            QtWidgets.QApplication.translate(
                "MainWindow",
                "Redo the last undone action.",
                None,
            )
        )
        log.info("Done Building UI")

    def set_line_edit(self, line_edit, arg):
        line_edit.setText(arg)

    def store_selection(self):
        self.vertices_stored = not self.vertices_stored

        if self.vertices_stored:
            self.get_vertex_selection_push_button.setStyleSheet(
                "QPushButton {background-color: red;}"
            )
        else:
            self.get_vertex_selection_push_button.setStyleSheet(
                "QPushButton {background-color: rgb(240, 240, 240);}"
            )


# TODO : all getter methods should trigger a signal, and the signal should be
#  connected to the relevant logic in the controller
# def get_spinBox_value(self):
#     """Get spinBox value and set slider value"""
#     value = self.revert_value_slider.value()
#
#     self.controller._revert_value = value
#
#     self.revert_value_sB.setValue(value)
#
# def get_slider_value(self):
#     """Get slider value and set spinBox value"""
#     value = self.revert_value_sB.value()
#
#     self.controller._revert_value = value
#
#     self.revert_value_slider.setValue(value)


if __name__ == "__main__":
    import sys                                                                  # pragma: no cover

    app = QtWidgets.QApplication(sys.argv)                                      # pragma: no cover
    dialog = QtWidgets.QDialog()                                                # pragma: no cover
    sizePolicy = QtWidgets.QSizePolicy(                                         # pragma: no cover
        QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding        # pragma: no cover
    )                                                                           # pragma: no cover
    dialog.setSizePolicy(sizePolicy)                                            # pragma: no cover
    widget = SymMeshUI(dialog)                                                  # pragma: no cover
    dialog.show()                                                               # pragma: no cover
    sys.exit(app.exec_())                                                       # pragma: no cover
