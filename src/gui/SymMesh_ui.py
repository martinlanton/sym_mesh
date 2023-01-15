import logging
from Qt import QtWidgets, QtCore

log = logging.getLogger("SymUI")
log.setLevel(logging.INFO)


class Layout(QtWidgets.QVBoxLayout):
    def __init__(self, parent=None):
        super(Layout, self).__init__(parent)
        self.buildUI()

        self.get_vertex_selection_pb.clicked.connect(self.store_selection)

        self.vertices_are_stored = False

    def buildUI(self):
        # ==========
        # Setup
        # TODO : add line around the groupbox on maya by default
        setup_groupbox = QtWidgets.QGroupBox("Base setup")
        self.addWidget(setup_groupbox)

        setup_layout = QtWidgets.QVBoxLayout(setup_groupbox)

        # Threshold
        threshold_layout = QtWidgets.QHBoxLayout()
        setup_layout.addLayout(threshold_layout)

        threshold_label = QtWidgets.QLabel("Symmetry threshold")
        threshold_layout.addWidget(threshold_label)

        self.threshold_sb = QtWidgets.QDoubleSpinBox()
        self.threshold_sb.setDecimals(3)
        self.threshold_sb.setValue(0.001)
        threshold_layout.addWidget(self.threshold_sb)

        # Direction
        direction_layout = QtWidgets.QHBoxLayout()
        setup_layout.addLayout(direction_layout)

        self.direction_rb_group = QtWidgets.QButtonGroup()

        self.negative_rb = QtWidgets.QRadioButton("Negative: - \u21D0 +")
        direction_layout.addWidget(self.negative_rb)
        self.direction_rb_group.addButton(self.negative_rb)

        self.positive_rb = QtWidgets.QRadioButton("Positive: - \u21D2 +")
        direction_layout.addWidget(self.positive_rb)
        self.direction_rb_group.addButton(self.positive_rb)

        self.negative_rb.setChecked(True)

        # Axis
        axis_layout = QtWidgets.QHBoxLayout()
        setup_layout.addLayout(axis_layout)

        self.axis_rb_group = QtWidgets.QButtonGroup()

        # QtTest.QTest.mouseClick, mousePress and mouseRelease use the .size()
        # method to calculate the center of the widget to simulate the click,
        # however the .size() method doesn't seem to return the proper value.
        # The .sizeHint() method on the other hand DOES return the proper value.
        # This means that if the actual size of the widget (.sizeHint()) is less
        # than half of the size returned by the .size() method, then the center
        # calculated from the result of the .size() method is actually OUTSIDE
        # the widget, therefore the click is not triggered.
        # To remediate that (and therefore have reliable tests) we have to put a
        # widget label longer than what is actually necessary

        self.x_axis_rb = QtWidgets.QRadioButton("Axis : X")
        axis_layout.addWidget(self.x_axis_rb)
        self.axis_rb_group.addButton(self.x_axis_rb)

        self.y_axis_rb = QtWidgets.QRadioButton("Axis : Y")
        axis_layout.addWidget(self.y_axis_rb)
        self.axis_rb_group.addButton(self.y_axis_rb)

        self.z_axis_rb = QtWidgets.QRadioButton("Axis : Z")
        axis_layout.addWidget(self.z_axis_rb)
        self.axis_rb_group.addButton(self.z_axis_rb)

        self.x_axis_rb.setChecked(True)

        # Get base
        base_layout = QtWidgets.QHBoxLayout()
        setup_layout.addLayout(base_layout)

        self.get_base_pb = QtWidgets.QPushButton("Get Base")
        self.get_base_pb.setObjectName("get_base_pB")
        base_layout.addWidget(self.get_base_pb)

        base_label = QtWidgets.QLabel("\u21D2")
        base_layout.addWidget(base_label)

        self.base_line_edit = QtWidgets.QLineEdit("base")
        self.base_line_edit.setEnabled(False)
        self.base_line_edit.setObjectName("base_line_edit")
        base_layout.addWidget(self.base_line_edit)

        # Get target
        target_layout = QtWidgets.QHBoxLayout()
        setup_layout.addLayout(target_layout)

        self.get_target_pb = QtWidgets.QPushButton("Get Target")
        self.get_target_pb.setObjectName("get_target_pB")
        target_layout.addWidget(self.get_target_pb)

        target_label = QtWidgets.QLabel("\u21D2")
        target_layout.addWidget(target_label)

        self.target_line_edit = QtWidgets.QLineEdit("target")
        self.target_line_edit.setEnabled(False)
        self.target_line_edit.setObjectName("target_line_edit")
        target_layout.addWidget(self.target_line_edit)

        # Select non-symmetrical vertices
        self.select_non_symmetrical_vertices_pb = QtWidgets.QPushButton(
            "Select Non Symmetrical Vertices on base"
        )
        self.select_non_symmetrical_vertices_pb.setObjectName(
            "select_non_symmetrical_vertices_pB"
        )
        setup_layout.addWidget(self.select_non_symmetrical_vertices_pb)

        # ==========
        # Selection
        selection_groupbox = QtWidgets.QGroupBox("Selection")
        self.addWidget(selection_groupbox)

        # Store vertices selection
        vertex_selection_layout = QtWidgets.QHBoxLayout(selection_groupbox)
        self.addLayout(vertex_selection_layout)

        self.get_vertex_selection_pb = QtWidgets.QPushButton("Get Vertex Selection")
        self.get_vertex_selection_pb.setObjectName("get_vertex_selection_push_button")
        vertex_selection_layout.addWidget(self.get_vertex_selection_pb)

        # Select stored vertex selection
        self.select_vertex_selection_pb = QtWidgets.QPushButton(
            "Select stored Vertices"
        )
        self.select_vertex_selection_pb.setObjectName("select_stored_vertices_pB")
        vertex_selection_layout.addWidget(self.select_vertex_selection_pb)

        # =========
        # Commands
        commands_groupbox = QtWidgets.QGroupBox("Tools")
        self.addWidget(commands_groupbox)

        commands_layout = QtWidgets.QVBoxLayout(commands_groupbox)

        # Revert to base on selection
        revert_to_base_layout = QtWidgets.QHBoxLayout()
        commands_layout.addLayout(revert_to_base_layout)

        self.revert_to_base_pb = QtWidgets.QPushButton("Revert to base")
        self.revert_to_base_pb.setObjectName("revert_to_base_live_pB")
        self.revert_to_base_pb.setMinimumSize(80, 30)
        revert_to_base_layout.addWidget(self.revert_to_base_pb)

        self.revert_to_base_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.revert_to_base_slider.setMaximum(100)
        self.revert_to_base_slider.setObjectName("revert_to_base_slider")
        revert_to_base_layout.addWidget(self.revert_to_base_slider)

        # Symmetry
        sym_layout = QtWidgets.QHBoxLayout()
        commands_layout.addLayout(sym_layout)

        self.symmetry_pb = QtWidgets.QPushButton("Symmetry")
        self.symmetry_pb.setObjectName("symmetry_pB")
        self.symmetry_pb.setMinimumSize(80, 30)
        sym_layout.addWidget(self.symmetry_pb)

        self.symmetry_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.symmetry_slider.setMaximum(100)
        self.symmetry_slider.setObjectName("symmetry_slider")
        sym_layout.addWidget(self.symmetry_slider)

        # Flip
        self.flip_pb = QtWidgets.QPushButton("Flip")
        self.flip_pb.setObjectName("flip_pB")
        self.flip_pb.setMinimumSize(80, 30)
        commands_layout.addWidget(self.flip_pb)

        # Extract axes
        # TODO : add a doubleSpinbox to set the Y value at which the new mesh
        #  should be translated from the target
        # TODO : add a button to put the deformation of the extracted shape to
        #  the original mesh (based on name) "bake extracted"
        self.extract_axes_pb = QtWidgets.QPushButton("Extract X Y Z")
        self.extract_axes_pb.setObjectName("extract_axes_pB")
        self.extract_axes_pb.setMinimumSize(80, 30)
        commands_layout.addWidget(self.extract_axes_pb)

        # Bake deltas
        self.bake_deltas_pb = QtWidgets.QPushButton("Bake Deltas")
        self.bake_deltas_pb.setObjectName("bake_deltas_pB")
        self.bake_deltas_pb.setMinimumSize(80, 30)
        commands_layout.addWidget(self.bake_deltas_pb)

        # =========
        # Undo Redo
        undo_redo_groupbox = QtWidgets.QGroupBox("Edit")
        self.addWidget(undo_redo_groupbox)

        undo_layout = QtWidgets.QHBoxLayout(undo_redo_groupbox)

        self.undo_push_button = QtWidgets.QPushButton("Undo")
        self.undo_push_button.setObjectName("undo_pB")
        undo_layout.addWidget(self.undo_push_button)

        self.redo_push_button = QtWidgets.QPushButton("Redo")
        self.redo_push_button.setObjectName("redo_push_button")
        undo_layout.addWidget(self.redo_push_button)

        self.add_tooltips()
        log.info("Done Building UI")

    def add_tooltips(self):
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
            "This is used as a mask of the vertices that "
            "should be affected when doing any transformation.\n\n"
            "IMPORTANT : When vertices are currently selected on the mesh on "
            "which we want to perform an operation, the current vertex selection "
            "will be used instead of the stored one."
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

    @staticmethod
    def set_line_edit(line_edit, arg):
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
