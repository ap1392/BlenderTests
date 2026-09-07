"""Build a small studio scene to verify Blender scripting, saving, and rendering."""
from pathlib import Path
import json
import math
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "setup_check"
OUTPUT.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)

def material(name, color, metallic=0.0, roughness=0.3):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = roughness
    return mat

def finish(obj, name, mat, bevel=0):
    obj.name = name
    obj.data.materials.append(mat)
    if bevel:
        modifier = obj.modifiers.new("Soft edges", "BEVEL")
        modifier.width = bevel
        modifier.segments = 5
        obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return obj

teal = material("Teal ceramic", (0.018, 0.33, 0.32), 0.2)
gold = material("Brushed gold", (0.72, 0.38, 0.09), 0.75, 0.24)
coral = material("Coral ceramic", (0.8, 0.13, 0.07), 0.1)
stone = material("Warm stone", (0.48, 0.45, 0.39), 0, 0.65)
floor = material("Midnight floor", (0.025, 0.038, 0.055), 0, 0.5)

bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=2.7, depth=0.28, location=(0, 0, 0.14))
finish(bpy.context.object, "Display plinth", stone, 0.08)
bpy.ops.mesh.primitive_cube_add(size=1.45, location=(-0.85, 0.15, 1.005), rotation=(0, 0, 0.18))
finish(bpy.context.object, "Beveled teal cube", teal, 0.14)
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.66, location=(0.95, -0.6, 0.94))
finish(bpy.context.object, "Coral sphere", coral)
bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_torus_add(major_segments=96, minor_segments=32, location=(0.8, 0.85, 1.22), rotation=(math.pi / 2, 0, 0.25), major_radius=0.71, minor_radius=0.22)
finish(bpy.context.object, "Gold ring", gold)
bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_plane_add(size=200)
finish(bpy.context.object, "Studio ground", floor)

def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()

for name, location, energy, size, color in [
    ("Key softbox", (0, -4, 7), 850, 5, (1, 0.83, 0.65)),
    ("Cool fill", (-4, -1, 3), 600, 4, (0.55, 0.77, 1)),
    ("Rim softbox", (3, 4, 5), 1100, 3, (1, 0.8, 0.55)),
]:
    data = bpy.data.lights.new(name, 'AREA')
    data.energy, data.shape, data.size, data.color = energy, 'DISK', size, color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    aim(obj, (0, 0, 0.6))

bpy.ops.object.camera_add(location=(6, -9, 6.2))
camera = bpy.context.object
camera.name = "Studio camera"
aim(camera, (0, 0, 0.75))
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 7.4
scene = bpy.context.scene
scene.camera = camera
scene.world = bpy.data.worlds.new("Studio world")
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs[0].default_value = (0.09, 0.12, 0.18, 1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value = 0.3
scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.render.resolution_x = 1200
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = str(OUTPUT / "setup_check.png")

# Prefer Apple's Metal device when Blender exposes it; retain CPU fallback.
devices = []
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'METAL'
    prefs.get_devices()
    for device in prefs.devices:
        device.use = device.type == 'METAL'
        if device.use:
            devices.append(device.name)
    if devices:
        scene.cycles.device = 'GPU'
except Exception as exc:
    print(f"Metal unavailable; using CPU: {exc}")

for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.region_3d.view_perspective = 'CAMERA'

blend = OUTPUT / "setup_check.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
bpy.ops.render.render(write_still=True)
report = {"blender_version": bpy.app.version_string, "render_engine": scene.render.engine,
          "device": scene.cycles.device, "gpu_devices": devices,
          "objects": len(scene.objects), "blend_file": str(blend),
          "render_file": scene.render.filepath}
(OUTPUT / "setup_report.json").write_text(json.dumps(report, indent=2) + "\n")
print("SETUP_CHECK_PASSED " + json.dumps(report))
