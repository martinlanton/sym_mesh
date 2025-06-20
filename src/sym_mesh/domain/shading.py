import logging
from maya import cmds as mc

logger = logging.getLogger(__name__)


def get_assigned_shader(geometry):
    shapes = mc.listRelatives(geometry, shapes=True, fullPath=True)
    if not shapes:
        logger.warning("No shapes found for geometry: {}".format(geometry))
        return None
    # Get shading groups assigned to the geometry
    shading_groups = mc.listConnections(shapes[0], type='shadingEngine')
    if not shading_groups:
        return None
    # Get surface shader connected to the shading group
    shader = mc.listConnections(shading_groups[0] + '.surfaceShader')
    if shader:
        return shader[0]
    return None


def assign_default_shader(objects):
    """Assign the default shader to each object in the list.

    :param objects: list of objects the shader needs to be applied to.
    :type objects: list[str]
    """
    mc.sets(objects, edit=True, forceElement="initialShadingGroup")
