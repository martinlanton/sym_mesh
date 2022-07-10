from Qt import QtWidgets, QtCore, QtGui
import logging

from MultiPipe.file_utils import Multi_import_utils as import_utils
from MultiPipe.general_utils import Multi_ui_utils as ui_utils
from MultiPipe.general_utils import logger as mla_logger
import mesh_modification as mla_MM


log = mla_logger.get_logger("SymUI", shell=True)
log.setLevel(logging.INFO)

application = import_utils.get_application()
dockable = ui_utils.get_dockable_widget(application)


class SymMeshUI(dockable, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SymMeshUI, self).__init__(parent=parent)

        self.setWindowTitle("SymMesh UI")
        # UI
        self.buildUI()
        self.sym_mesh = mla_MM.MeshModifier()

        self.sym_mesh._revert_value = 100

        self.revert_value_slider.valueChanged.connect(self.get_spinBox_value)
        self.revert_value_sB.valueChanged.connect(self.get_slider_value)

        self.vertices_stored = False

        # Connexion
        self.get_base_pB.clicked.connect(self.get_base)
        self.get_target_pB.clicked.connect(self.get_target)
        self.get_selected_vtcs_pB.clicked.connect(self.get_selected_vertices)
        self.select_stored_vtcs_pB.clicked.connect(self.select_stored_vertices)
        self.select_non_symmetrical_vtcs_pB.clicked.connect(
            self.select_non_mirrored_vertices
        )
        self.bake_diff_pB.clicked.connect(self.bake_difference)
        self.revert_to_base_pB.clicked.connect(self.revert_to_base)
        self.revert_to_base_live_pB.clicked.connect(self.revert_to_base_live)
        self.undo_pB.clicked.connect(self.undo)

    def buildUI(self):
        log.info("Building UI")
        self.layout = QtWidgets.QVBoxLayout(self)

        self.get_base_pB = QtWidgets.QPushButton("Get Base")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(self.get_base_pB.sizePolicy().hasHeightForWidth())
        self.get_base_pB.setSizePolicy(sizePolicy)
        self.get_base_pB.setMinimumSize(QtCore.QSize(0, 25))
        self.get_base_pB.setObjectName("get_base_pB")
        self.layout.addWidget(self.get_base_pB)

        self.base_lE = QtWidgets.QLineEdit("base_LE")
        self.base_lE.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(self.base_lE.sizePolicy().hasHeightForWidth())
        self.base_lE.setSizePolicy(sizePolicy)
        self.base_lE.setMinimumSize(QtCore.QSize(0, 25))
        self.base_lE.setObjectName("base_lE")
        self.layout.addWidget(self.base_lE)

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

        self.target_lE = QtWidgets.QLineEdit("target_LE")
        self.target_lE.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(self.target_lE.sizePolicy().hasHeightForWidth())
        self.target_lE.setSizePolicy(sizePolicy)
        self.target_lE.setMinimumSize(QtCore.QSize(0, 25))
        self.target_lE.setObjectName("target_lE")
        self.layout.addWidget(self.target_lE)

        self.get_selected_vtcs_pB = QtWidgets.QPushButton("Get Vtx Selection")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.get_selected_vtcs_pB.sizePolicy().hasHeightForWidth()
        )
        self.get_selected_vtcs_pB.setSizePolicy(sizePolicy)
        self.get_selected_vtcs_pB.setMinimumSize(QtCore.QSize(0, 25))
        self.get_selected_vtcs_pB.setObjectName("get_selected_vtcs_pB")
        self.layout.addWidget(self.get_selected_vtcs_pB)

        self.select_non_symmetrical_vtcs_pB = QtWidgets.QPushButton(
            "Select Non Symmetrical Vtcs"
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.select_non_symmetrical_vtcs_pB.sizePolicy().hasHeightForWidth()
        )
        self.select_non_symmetrical_vtcs_pB.setSizePolicy(sizePolicy)
        self.select_non_symmetrical_vtcs_pB.setMinimumSize(QtCore.QSize(0, 25))
        self.select_non_symmetrical_vtcs_pB.setObjectName(
            "select_non_symmetrical_vtcs_pB"
        )
        self.layout.addWidget(self.select_non_symmetrical_vtcs_pB)

        self.select_stored_vtcs_pB = QtWidgets.QPushButton("Select stored Vtcs")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.select_stored_vtcs_pB.sizePolicy().hasHeightForWidth()
        )
        self.select_stored_vtcs_pB.setSizePolicy(sizePolicy)
        self.select_stored_vtcs_pB.setMinimumSize(QtCore.QSize(0, 25))
        self.select_stored_vtcs_pB.setObjectName("select_stored_vtcs_pB")
        self.layout.addWidget(self.select_stored_vtcs_pB)

        self.bake_diff_pB = QtWidgets.QPushButton("Bake Difference")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(self.bake_diff_pB.sizePolicy().hasHeightForWidth())
        self.bake_diff_pB.setSizePolicy(sizePolicy)
        self.bake_diff_pB.setMinimumSize(QtCore.QSize(0, 25))
        self.bake_diff_pB.setObjectName("bake_diff_pB")
        self.layout.addWidget(self.bake_diff_pB)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layout.addLayout(self.horizontalLayout)

        self.revert_value_slider = QtWidgets.QSlider()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.revert_value_slider.sizePolicy().hasHeightForWidth()
        )
        self.revert_value_slider.setSizePolicy(sizePolicy)
        self.revert_value_slider.setMinimumSize(QtCore.QSize(0, 25))
        self.revert_value_slider.setMaximum(100)
        self.revert_value_slider.setProperty("value", 100)
        self.revert_value_slider.setOrientation(QtCore.Qt.Horizontal)
        self.revert_value_slider.setObjectName("revert_value_slider")
        self.horizontalLayout.addWidget(self.revert_value_slider)

        self.revert_value_sB = QtWidgets.QSpinBox()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.revert_value_sB.sizePolicy().hasHeightForWidth()
        )
        self.revert_value_sB.setSizePolicy(sizePolicy)
        self.revert_value_sB.setMinimumSize(QtCore.QSize(0, 25))
        self.revert_value_sB.setMaximum(100)
        self.revert_value_sB.setProperty("value", 100)
        self.revert_value_sB.setObjectName("revert_value_sB")
        self.horizontalLayout.addWidget(self.revert_value_sB)

        self.revert_to_base_pB = QtWidgets.QPushButton("Revert sel to base (target)")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.revert_to_base_pB.sizePolicy().hasHeightForWidth()
        )
        self.revert_to_base_pB.setSizePolicy(sizePolicy)
        self.revert_to_base_pB.setMinimumSize(QtCore.QSize(0, 25))
        self.revert_to_base_pB.setObjectName("revert_to_base_pB")
        self.layout.addWidget(self.revert_to_base_pB)

        self.revert_to_base_live_pB = QtWidgets.QPushButton("Revert sel to base (live)")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(
            self.revert_to_base_live_pB.sizePolicy().hasHeightForWidth()
        )
        self.revert_to_base_live_pB.setSizePolicy(sizePolicy)
        self.revert_to_base_live_pB.setMinimumSize(QtCore.QSize(0, 25))
        self.revert_to_base_live_pB.setObjectName("revert_to_base_live_pB")
        self.layout.addWidget(self.revert_to_base_live_pB)

        self.undo_pB = QtWidgets.QPushButton("Undo")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(self.undo_pB.sizePolicy().hasHeightForWidth())
        self.undo_pB.setSizePolicy(sizePolicy)
        self.undo_pB.setMinimumSize(QtCore.QSize(0, 25))
        self.undo_pB.setObjectName("undo_pB")
        self.layout.addWidget(self.undo_pB)

        self.revert_to_base_pB.setToolTip(
            QtWidgets.QApplication.translate(
                "MainWindow",
                "Revert selected mesh or vertices to base, from registered position.",
                None,
            )
        )
        self.revert_to_base_live_pB.setToolTip(
            QtWidgets.QApplication.translate(
                "MainWindow",
                "Revert selected mesh or vertices to base, from current position.",
                None,
            )
        )
        self.undo_pB.setToolTip(
            QtWidgets.QApplication.translate(
                "MainWindow",
                "Revert selected mesh or vertices to base, from current position.",
                None,
            )
        )

    def get_spinBox_value(self):
        """Get spinBox value and set slider value"""
        value = self.revert_value_slider.value()

        self.sym_mesh._revert_value = value

        self.revert_value_sB.setValue(value)

    def get_slider_value(self):
        """Get slider value and set spinBox value"""
        value = self.revert_value_sB.value()

        self.sym_mesh._revert_value = value

        self.revert_value_slider.setValue(value)

    def get_base(self):
        self.sym_mesh.get_base()
        self.base_lE.setText(self.sym_mesh.base)

    def get_target(self):
        self.sym_mesh.get_target()
        self.target_lE.setText(self.sym_mesh.target)

    def get_selected_vertices(self):
        if not self.sym_mesh.are_vertices_stored:
            self.sym_mesh.get_vtcs_selection()
        else:
            self.sym_mesh.get_vtcs_selection(True)

        if self.sym_mesh.are_vertices_stored:
            self.vertices_stored = True
            self.get_selected_vtcs_pB.setStyleSheet(
                "QPushButton {background-color: red;}"
            )
        else:
            self.vertices_stored = False
            self.get_selected_vtcs_pB.setStyleSheet(
                "QPushButton {background-color: dark gray;}"
            )

    def select_stored_vertices(self):
        self.sym_mesh.select_stored_vertices()

    def select_non_mirrored_vertices(self):
        self.sym_mesh.select_non_mirrored_vertices()

    def bake_difference(self):
        self.sym_mesh.bake_difference_on_selected()

    def revert_to_base(self):
        self.sym_mesh.revert_selected_to_base()

    def revert_to_base_live(self):
        self.sym_mesh.revert_selected_to_base_live()

    def undo(self):
        self.sym_mesh.undo_last_action()
