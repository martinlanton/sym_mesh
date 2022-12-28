import logging
from maya import cmds as mc

logger = logging.getLogger(__name__)


def get_shading_group_from_shader(shader):
    shading_group = ""
    if mc.objExists(shader):
        shading_groups = mc.listConnections(
            shader, destination=True, exactType=True, type="shadingEngine"
        )
        if shading_groups:
            try:
                shading_groups.remove("initialParticleSE")
                shading_group = shading_groups[0]
            except ValueError:  # pragma: no cover
                # Not covering this statement as there is most likely no reliable way to test it
                logger.error(
                    'No "initialParticleSE" shading group found. The scene might be corrupted.'
                    " Make sure everything works as expected."
                )  # pragma: no cover
    return shading_group


def assign_shader(objects, shader):
    """Assign the shader to each object in the list.

    :param objects: list of objects the shader needs to be applied to.
    :type objects: list[str]

    :param shader: name of the shader to assign
    :type shader: str
    """
    # assign selection to the shader
    shading_group = get_shading_group_from_shader(shader)
    mc.sets(objects, edit=True, forceElement=shading_group)
