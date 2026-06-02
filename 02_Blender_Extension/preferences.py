import bpy


def _on_enabled_changed(self, context):
    for area in context.screen.areas:
        if area.type == "VIEW_3D":
            area.tag_redraw()


class AddonESP32Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    enabled: bpy.props.BoolProperty(
        name="Activar AddonESP32",
        description=(
            "Activa o desactiva el addon. "
            "Al desactivar se oculta el panel ESP32."
        ),
        default=True,
        update=_on_enabled_changed,
    )

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.scale_y = 1.2
        col.prop(self, "enabled", icon="CHECKMARK" if self.enabled else "X")

        if not self.enabled:
            box = layout.box()
            box.label(text="Addon desactivado: el panel ESP32 está oculto.", icon="INFO")
            box.label(text="Reactiva la casilla para volver a usarlo.")


def get_prefs(context=None):
    ctx = context or bpy.context
    addon = ctx.preferences.addons.get(__package__)
    return addon.preferences if addon else None


def is_enabled(context=None) -> bool:
    prefs = get_prefs(context)
    if prefs is None:
        return True
    return bool(prefs.enabled)


def register():
    bpy.utils.register_class(AddonESP32Preferences)


def unregister():
    bpy.utils.unregister_class(AddonESP32Preferences)
