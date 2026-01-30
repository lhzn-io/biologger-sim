import os

import bpy

# This script converts TIF textures to PNG and re-links them
for img in bpy.data.images:
    if img.filepath.lower().endswith(".tif"):
        # Determine new path
        old_path = bpy.path.abspath(img.filepath)
        new_path = os.path.splitext(old_path)[0] + ".png"

        # Change format and save a new version to disk
        img.file_format = "PNG"
        img.save_render(new_path)  # save_render is safer for format conversion

        # Update Blender to use the new file
        img.filepath = bpy.path.relpath(new_path)
        img.reload()
        print(f"Converted: {old_path} -> {new_path}")

print("Conversion complete. All TIFs are now PNGs.")
