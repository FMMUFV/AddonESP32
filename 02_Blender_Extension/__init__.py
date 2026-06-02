import bpy
from . import operators, panels, preferences

ADDON_VERSION = "0.1.0"


def register():
    preferences.register()
    operators.register()
    panels.register()


def unregister():
    panels.unregister()
    operators.unregister()
    preferences.unregister()
