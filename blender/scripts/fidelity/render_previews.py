import bpy,json,time
from pathlib import Path
root=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests');out=root/'renders/fidelity';out.mkdir(exist_ok=True)
names=globals().get('REF_NAMES',[o.name for o in bpy.data.objects if o.type=='CAMERA' and o.name.startswith('REF')]);suffix=globals().get('REF_SUFFIX','geometry');queue=list(sorted(names));results=[]
def next_frame(queue=queue,results=results,root=root,out=out,suffix=suffix):
 import bpy,json,time
 if not queue:
  (out/f'queue_{suffix}.json').write_text(json.dumps({'complete':True,'results':results},indent=2));return None
 name=queue.pop(0);s=bpy.context.scene;c=bpy.data.objects[name]
 if c.name.startswith('CINE_'):s.frame_set(c.get('first_frame',1))
 bindings=[(m,m.camera)for m in s.timeline_markers if m.camera]
 for m,cam in bindings:m.camera=None
 s.camera=c;s.view_settings.exposure=c.get('photographic_exposure',.7)
 w=c.get('render_width',1149);h=c.get('render_height',900);scale=850/max(w,h)
 s.render.resolution_x=int(w*scale);s.render.resolution_y=int(h*scale);s.render.resolution_percentage=100;s.cycles.samples=24;s.cycles.use_denoising=True;s.render.filepath=str(out/f'{name}_{suffix}.png')
 start=time.time()
 try:bpy.ops.render.render(write_still=True)
 finally:
  for m,cam in bindings:m.camera=cam
 results.append({'camera':name,'seconds':time.time()-start,'file':s.render.filepath})
 (out/f'queue_{suffix}.json').write_text(json.dumps({'complete':False,'remaining':queue,'results':results},indent=2));return .5
bpy.app.timers.register(next_frame,first_interval=.5)
print('Queued',len(queue),'reference previews',suffix)
