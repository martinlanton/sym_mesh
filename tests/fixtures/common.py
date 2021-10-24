import tempfile
import os
import shutil


def startup_maya_session():
    currentMayaAppDir = os.environ.get("MAYA_APP_DIR")
    os.environ["MAYA_APP_DIR"] = tempfile.mkdtemp()

    from maya import standalone

    standalone.initialize()

    return {
        "tmpMayaAppDir": os.environ["MAYA_APP_DIR"],
        "origMayaAppDir": currentMayaAppDir,
    }


def teardown_maya_session(state):
    from maya import standalone

    standalone.uninitialize()

    try:
        shutil.rmtree(state["tmpMayaAppDir"])
    # Windows hasn't given up the handles to the files yet. So, ignore it.
    except WindowsError:
        pass

    if state["origMayaAppDir"] is not None:
        os.environ["MAYA_APP_DIR"] = state["origMayaAppDir"]
