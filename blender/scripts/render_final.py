"""Configure Cycles on Apple Metal and render requested final cameras.
Invoke one camera per MCP call with ISEC_CAMERA='01_Ground_spiral' etc.
"""
import bpy,json,time
from pathlib import Path
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
 prefs.compute_device_type='METAL';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='METAL'
 s.cycles.device='GPU' if any(d.type=='METAL'for d in prefs.devices)else'CPU'
except Exception:s.cycles.device='CPU'
s.render.engine='CYCLES';s.cycles.samples=96;s.cycles.use_denoising=True;s.render.resolution_x=1600;s.render.resolution_y=1200;s.render.resolution_percentage=100
name=globals().get('ISEC_CAMERA','01_Ground_spiral');s.camera=bpy.data.objects[name];s.render.filepath=str(ROOT/'renders/final'/f'{name}.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
t=time.time();bpy.ops.render.render(write_still=True)
(ROOT/'renders/validation'/f'{name}_render.json').write_text(json.dumps({'camera':name,'engine':'CYCLES','device':s.cycles.device,'samples':96,'resolution':[1600,1200],'seconds':time.time()-t},indent=2))
print('Rendered',name,s.cycles.device,round(time.time()-t,1),'seconds')
