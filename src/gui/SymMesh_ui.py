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
        self.get_vertex_selection_pb.clicked.connect(self.store_selection)

        self.vertices_are_stored = False

    def buildUI(self):
        # Direction
        direction_layout = QtWidgets.QHBoxLayout()
        self.addLayout(direction_layout)

        self.direction_rb_group = QtWidgets.QButtonGroup()

        self.negative_rb = QtWidgets.QRadioButton("Negative: - <= +")
        direction_layout.addWidget(self.negative_rb)
        self.direction_rb_group.addButton(self.negative_rb)

        self.positive_rb = QtWidgets.QRadioButton("Positive: - => +")
        direction_layout.addWidget(self.positive_rb)
        self.direction_rb_group.addButton(self.positive_rb)
        self.positive_rb.setChecked(True)

        # Get base
        self.get_base_pb = QtWidgets.QPushButton("Get Base")
        self.get_base_pb.setObjectName("get_base_pB")
        self.addWidget(self.get_base_pb)

        self.base_line_edit = QtWidgets.QLineEdit("base")
        self.base_line_edit.setEnabled(False)
        self.base_line_edit.setObjectName("base_line_edit")
        self.addWidget(self.base_line_edit)

        # Get target
        self.get_target_pb = QtWidgets.QPushButton("Get Target")
        self.get_target_pb.setObjectName("get_target_pB")
        self.addWidget(self.get_target_pb)

        self.target_line_edit = QtWidgets.QLineEdit("target")
        self.target_line_edit.setEnabled(False)
        self.target_line_edit.setObjectName("target_line_edit")
        self.addWidget(self.target_line_edit)

        # Store vertices selection
        self.get_vertex_selection_pb = QtWidgets.QPushButton("Get Vertex Selection")
        self.get_vertex_selection_pb.setObjectName("get_vertex_selection_push_button")
        self.addWidget(self.get_vertex_selection_pb)

        # Select non-symmetrical vertices
        self.select_non_symmetrical_vertices_pb = QtWidgets.QPushButton(
            "Select Non Symmetrical Vertices on base"
        )
        self.select_non_symmetrical_vertices_pb.setObjectName(
            "select_non_symmetrical_vertices_pB"
        )
        self.addWidget(self.select_non_symmetrical_vertices_pb)

        # Select stored vertex selection
        self.select_vertex_selection_pb = QtWidgets.QPushButton(
            "Select stored Vertices"
        )
        self.select_vertex_selection_pb.setObjectName("select_stored_vertices_pB")
        self.addWidget(self.select_vertex_selection_pb)

        # Bake deltas
        self.bake_deltas_pb = QtWidgets.QPushButton("Bake Deltas")
        self.bake_deltas_pb.setObjectName("bake_deltas_pB")
        self.addWidget(self.bake_deltas_pb)

        # Symmetry
        self.symmetry_pb = QtWidgets.QPushButton("Symmetry")
        self.symmetry_pb.setObjectName("symmetry_pB")
        self.addWidget(self.symmetry_pb)

        # Flip
        self.flip_pb = QtWidgets.QPushButton("Flip")
        self.flip_pb.setObjectName("flip_pB")
        self.addWidget(self.flip_pb)

        # Extract axes
        self.extract_axes_pb = QtWidgets.QPushButton("Extract X Y Z axes")
        self.extract_axes_pb.setObjectName("extract_axes_pB")
        self.addWidget(self.extract_axes_pb)

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
        self.revert_to_base_pb = QtWidgets.QPushButton("Revert sel to base (live)")
        self.revert_to_base_pb.setObjectName("revert_to_base_live_pB")
        self.addWidget(self.revert_to_base_pb)

        # Undo
        self.undo_push_button = QtWidgets.QPushButton("Undo")
        self.undo_push_button.setObjectName("undo_pB")
        self.addWidget(self.undo_push_button)

        # Redo
        self.redo_push_button = QtWidgets.QPushButton("Redo")
        self.redo_push_button.setObjectName("redo_push_button")
        self.addWidget(self.redo_push_button)

        # Tooltips
        self.get_base_pb.setToolTip(
            "Store the currently selected geometry as Base geometry.\n"
            "This mesh is used as symmetry table for all operations that require one."
        )
        self.get_target_pb.setToolTip(
            "Store the currently selected geometry as Target geometry.\n"
            "Currently only used when baking deltas."
        )
        self.get_vertex_selection_pb.setToolTip(
            "Store the currently selected vertices.\n"
            "This is used a mask of the vertices that "
            "should be affected when doing any transformation.\n\n"
            "IMPORTANT : When vertices are currently selected on the mesh on "
            "which we want to perform an operation, the current vertex selection "
            "will be used instead."
        )
        self.select_non_symmetrical_vertices_pb.setToolTip(
            "Select non symmetrical vertices on the " "model stored as base."
        )
        self.select_vertex_selection_pb.setToolTip(
            "Select the currently stored vertex selection."
        )
        self.bake_deltas_pb.setToolTip(
            "Bake the difference between the `Base` mesh and the "
            "`Target` mesh on all currently selected meshes."
        )
        self.symmetry_pb.setToolTip(
            "Symmetrize the selected mesh.\n"
            "The `Base` mesh is used as a symmetry table."
        )
        self.flip_pb.setToolTip(
            "Flip the selected mesh.\n"
            "The `Base` mesh is used as a symmetry table to "
            "identify which vertices should be associated "
            "together for the flipping operation."
        )
        self.extract_axes_pb.setToolTip(
            "Extract the difference in the x, y and z "
            "axes between the selected mesh and the `Base` mesh.\n"
            "That difference is then split and added as a blendshape "
            "on the extracted mesh. The blendshape will have 3 targets, "
            "one for each of the x, y, and z axes of the extracted difference."
        )
        self.revert_to_base_pb.setToolTip(
            "Revert the selected mesh to the position of the base mesh."
        )
        self.undo_push_button.setToolTip(
            "Straightforward : Undo the last deformation/extraction action."
        )
        self.redo_push_button.setToolTip(
            "Straightforward : Redo the last undone action."
        )
        log.info("Done Building UI")

    def set_line_edit(self, line_edit, arg):
        line_edit.setText(arg)

    def store_selection(self):
        self.vertices_are_stored = not self.vertices_are_stored

        if self.vertices_are_stored:
            self.get_vertex_selection_pb.setStyleSheet(
                "QPushButton {background-color: red;}"
            )
        else:
            self.get_vertex_selection_pb.setStyleSheet(
                "QPushButton {background-color: rgb(93, 93, 93);}"
            )


if __name__ == "__main__":
    """This is used to test the gui visually through the following command : 
    `python -m SymMesh_ui`
    This has to be run in a terminal after cd'ing in the `gui` folder.
    """
    import sys  # pragma: no cover

    app = QtWidgets.QApplication(sys.argv)  # pragma: no cover
    dialog = QtWidgets.QDialog()  # pragma: no cover
    layout = Layout(dialog)  # pragma: no cover

    dialog.show()  # pragma: no cover
    sys.exit(app.exec_())  # pragma: no cover
