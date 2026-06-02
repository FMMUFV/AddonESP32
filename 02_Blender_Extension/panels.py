import bpy
from . import preferences


class ADDESP32_PT_main(bpy.types.Panel):
    bl_label       = "ESP32"
    bl_idname      = "ADDESP32_PT_main"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "ESP32"

    @classmethod
    def poll(cls, context):
        return preferences.is_enabled(context)

    def draw(self, context):
        layout = self.layout

        layout.label(text="AddonESP32 v0.1.0", icon="DECORATE_LINKED")

        layout.separator()

        layout.operator("addesp32.reload_addon",
                        text="Refrescar Addon",
                        icon="FILE_REFRESH")


_classes = [ADDESP32_PT_main]


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
