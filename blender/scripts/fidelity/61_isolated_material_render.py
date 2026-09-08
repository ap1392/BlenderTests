import bpy,time,json
from pathlib import Path
root=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
exec(compile((root/'blender/scripts/fidelity/61_photometric_wood_trial.py').read_text(),'61_photometric_wood_trial.py','exec'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.render.threads_mode='FIXED';s.render.threads=4;s.cycles.samples=24;s.cycles.adaptive_threshold=.025;s.cycles.use_denoising=True
s.camera=bpy.data.objects['REF04_Writeup'];s.view_settings.exposure=.7;s.render.resolution_x=1024;s.render.resolution_y=494;s.render.resolution_percentage=100;s.render.filepath=str(root/'renders/fidelity/REF04_Writeup_photometric61.png')
start=time.time();bpy.ops.render.render(write_still=True)
(root/'renders/fidelity/material_trial61.json').write_text(json.dumps({'complete':True,'file':s.render.filepath,'seconds':time.time()-start,'device':'isolated CPU process','master_saved':False},indent=2))
print('Isolated material preview complete; live master unchanged')
