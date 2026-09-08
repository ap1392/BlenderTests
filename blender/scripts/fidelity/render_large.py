import bpy,json,time
from pathlib import Path
root=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests');out=root/'renders/fidelity/large';out.mkdir(exist_ok=True)
queue=sorted([o.name for o in bpy.data.objects if o.type=='CAMERA'and o.name.startswith('REF')]);queue=queue[6:]+queue[:6];results=[]
(out/'progress.json').write_text(json.dumps({'complete':False,'remaining':queue,'results':results,'revision':'post60','maximum_dimension':2048,'samples':160},indent=2))
def next_frame(queue=queue,results=results,out=out,root=root):
 import bpy,json,time
 if (root/'renders/fidelity/STOP_RENDER_QUEUE').exists():
  (out/'progress.json').write_text(json.dumps({'complete':False,'interrupted':True,'remaining':queue,'results':results},indent=2));return None
 if not queue:
  (out/'progress.json').write_text(json.dumps({'complete':True,'results':results,'revision':'post60','maximum_dimension':2048,'samples':160},indent=2));return None
 name=queue.pop(0);s=bpy.context.scene;c=bpy.data.objects[name];s.camera=c;s.view_settings.exposure=c.get('photographic_exposure',.7)
 w=c.get('render_width',1149);h=c.get('render_height',900);scale=2048/max(w,h)
 s.render.resolution_x=int(w*scale);s.render.resolution_y=int(h*scale);s.render.resolution_percentage=100;s.cycles.samples=160;s.cycles.adaptive_threshold=.007;s.cycles.use_denoising=True;s.render.filepath=str(out/f'{name}_validation.png')
 start=time.time();bpy.ops.render.render(write_still=True);results.append({'camera':name,'seconds':time.time()-start,'file':s.render.filepath,'width':s.render.resolution_x,'height':s.render.resolution_y})
 (out/'progress.json').write_text(json.dumps({'complete':False,'remaining':queue,'results':results,'revision':'post60','maximum_dimension':2048,'samples':160},indent=2));return .5
bpy.app.driver_namespace['isec_render_queue_callback']=next_frame
bpy.app.timers.register(next_frame,first_interval=.5)
print('Queued12 reference views at2048px/160samples; stop marker supported')
