import tempfile
import os
import shutil
import logging

import pytest
import sys


logger = logging.getLogger(__name__)

location = os.path.dirname(__file__)
src = os.path.join(location, "src")
logger.info("Adding src path to sys.path, src path : %s" % src)
if src not in sys.path:
    sys.path.insert(0, src)


@pytest.fixture(scope="session")
def session():
    startup = None
    teardown = None
    state = None

    if "IN_MAYA" in os.environ:
        startup = _startup_maya_session
        teardown = _teardown_maya_session

    if startup:
        state = startup()

    yield

    if teardown:
        teardown(state)


def _startup_maya_session():
    currentMayaAppDir = os.environ.get("MAYA_APP_DIR")
    os.environ["MAYA_APP_DIR"] = tempfile.mkdtemp()

    from maya import standalone
    standalone.initialize()

    return {
        "tmpMayaAppDir": os.environ["MAYA_APP_DIR"],
        "origMayaAppDir": currentMayaAppDir
    }


def _teardown_maya_session(state):
    from maya import standalone
    standalone.uninitialize()

    try:
        shutil.rmtree(state["tmpMayaAppDir"])
    # Windows hasn't given up the handles to the files yet. So, ignore it.
    except WindowsError:
        pass

    if state["origMayaAppDir"] is not None:
        os.environ["MAYA_APP_DIR"] = state["origMayaAppDir"]
