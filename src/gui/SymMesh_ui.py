import logging
from Qt import QtWidgets, QtCore

log = logging.getLogger("SymUI")
log.setLevel(logging.INFO)


class Layout(QtWidgets.QVBoxLayout):
    def __init__(self, parent=None):
        super(Layout, self).__init__(parent)
        self.buildUI()

        # self.revert_value_slider.valueChanged.connect(self.get_spinBox_value)
        # self.revert_value_sB.valueChanged.connect(self.get_slider_value)
        self.get_vertex_selection_push_button.clicked.connect(self.store_selection)

        self.vertices_stored = False

    def buildUI(self):
        self.get_base_pB = QtWidgets.QPushButton("Get Base")
        self.get_base_pB.setObjectName("get_base_pB")
        self.addWidget(self.get_base_pB)

        self.base_line_edit = QtWidgets.QLineEdit("base")
        self.base_line_edit.setEnabled(False)
        self.base_line_edit.setObjectName("base_line_edit")
        self.addWidget(self.base_line_edit)

        # Get target
        self.get_target_pB = QtWidgets.QPushButton("Get Target")
        self.get_target_pB.setObjectName("get_target_pB")
        self.addWidget(self.get_target_pB)

        self.target_line_edit = QtWidgets.QLineEdit("target")
        self.target_line_edit.setEnabled(False)
        self.target_line_edit.setObjectName("target_line_edit")
        self.addWidget(self.target_line_edit)

        # Store vertices selection
        self.get_vertex_selection_push_button = QtWidgets.QPushButton("Get Vertex Selection")
        self.get_vertex_selection_push_button.setObjectName("get_vertex_selection_push_button")
        self.addWidget(self.get_vertex_selection_push_button)

        # Select non-symmetrical vertices
        self.select_non_symmetrical_vertices_push_button = QtWidgets.QPushButton(
            "Select Non Symmetrical Vertices"
        )
        self.select_non_symmetrical_vertices_push_button.setObjectName(
            "select_non_symmetrical_vertices_pB"
        )
        self.addWidget(self.select_non_symmetrical_vertices_push_button)

        # Select stored vertex selection
        self.select_vertex_selection_push_button = QtWidgets.QPushButton("Select stored Vertices")
        self.select_vertex_selection_push_button.setObjectName("select_stored_vertices_pB")
        self.addWidget(self.select_vertex_selection_push_button)

        # Bake deltas
        self.bake_deltas_push_button = QtWidgets.QPushButton("Bake Deltas")
        self.bake_deltas_push_button.setObjectName("bake_deltas_pB")
        self.addWidget(self.bake_deltas_push_button)

        # Symmetry
        self.symmetry_push_button = QtWidgets.QPushButton("Symmetry")
        self.symmetry_push_button.setObjectName("symmetry_pB")
        self.addWidget(self.symmetry_push_button)

        # Flip
        self.flip_push_button = QtWidgets.QPushButton("Flip")
        self.flip_push_button.setObjectName("flip_pB")
        self.addWidget(self.flip_push_button)

        # Extract axes
        self.extract_axes_push_button = QtWidgets.QPushButton("Extract X Y Z axes")
        self.extract_axes_push_button.setObjectName("extract_axes_pB")
        self.addWidget(self.extract_axes_push_button)

        # # Revert value
        # self.horizontalLayout = QtWidgets.QHBoxLayout()
        # self.horizontalLayout.setObjectName("horizontalLayout")
        # self.addLayout(self.horizontalLayout)
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
        # self.addWidget(self.revert_to_base_pB)

        # Revert to base on selection
        self.revert_to_base_push_button = QtWidgets.QPushButton(
            "Revert sel to base (live)"
        )
        self.revert_to_base_push_button.setObjectName("revert_to_base_live_pB")
        self.addWidget(self.revert_to_base_push_button)

        # Undo
        self.undo_push_button = QtWidgets.QPushButton("Undo")
        self.undo_push_button.setObjectName("undo_pB")
        self.addWidget(self.undo_push_button)

        # Redo
        self.redo_push_button = QtWidgets.QPushButton("Redo")
        self.redo_push_button.setObjectName("redo_push_button")
        self.addWidget(self.redo_push_button)

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


if __name__ == "__main__":
    import sys                                                                  # pragma: no cover

    app = QtWidgets.QApplication(sys.argv)                                      # pragma: no cover
    dialog = QtWidgets.QDialog()
    layout = Layout(dialog)

    dialog.show()
    sys.exit(app.exec_())                                                       # pragma: no cover
