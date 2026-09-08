"""Save the finite final polish and camera rig without rebuilding architecture."""
import bpy
from pathlib import Path
root=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
s=bpy.context.scene
for folder in ['blender/scripts/fidelity']:
    for p in sorted((root/folder).glob('*.py')):
        name='fidelity/'+p.name
        t=bpy.data.texts.get(name) or bpy.data.texts.new(name)
        t.clear();t.write(p.read_text())
for relative in ['references/fidelity/cinematic_confidence_map.md',
                 'references/fidelity/visual/final_polish_triage.md',
                 'references/fidelity/cinematic_polish_report.md',
                 'references/fidelity/calibration/cinematic_clearance.json',
                 'unreal/source/cinematic_camera_manifest.json']:
    p=root/relative
    t=bpy.data.texts.get(relative) or bpy.data.texts.new(relative)
    t.clear();t.write(p.read_text())
s['cinematic_material_revision']='62 accepted after reference preview review; fabric shell revision63'
s['cinematic_status']='Finite Blender polish saved. Six camera tracks,72seconds. Unreal import and movie still pending.'
s['fidelity_status']='Reference-supported reconstruction with documented dimensional and material approximations; not an as-built survey.'
s.render.engine='CYCLES';s.cycles.samples=256;s.cycles.use_denoising=True
s.cycles.max_bounces=12;s.cycles.diffuse_bounces=6;s.cycles.glossy_bounces=6;s.cycles.transmission_bounces=12
s.frame_set(1);s.camera=bpy.data.objects['CINE_01_Atrium']
s.render.resolution_x=3840;s.render.resolution_y=2160;s.render.resolution_percentage=100
s.view_settings.exposure=.7
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(root/'blender/ISEC_Master.blend'))
print('Authoritative master saved with final polish, confidence map and six cinematic camera tracks')
