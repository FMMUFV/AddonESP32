import bpy


class ADDESP32_OT_reload_addon(bpy.types.Operator):
    """Recarga todos los scripts del addon"""
    bl_idname  = "addesp32.reload_addon"
    bl_label   = "Refrescar Addon"
    bl_options = {"REGISTER"}

    def execute(self, context):
        bpy.app.timers.register(lambda: bpy.ops.script.reload(), first_interval=0.1)
        self.report({"INFO"}, "Recargando addon...")
        return {"FINISHED"}


_classes = [
    ADDESP32_OT_reload_addon,
]


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
