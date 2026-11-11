import bpy, sys
print("BLENDER_HEADLESS_OK", bpy.app.version_string)
print("движки:", [e for e in bpy.types.RenderEngine.__subclasses__()][:3])
