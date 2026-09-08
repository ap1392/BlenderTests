"""Five 4K Cycles stills from the accepted camera rig; a resumable timer queue."""
import bpy,json,time
from pathlib import Path
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
OUT=ROOT/'renders/cinematic/cycles_heroes';OUT.mkdir(parents=True,exist_ok=True)
queue=[('CINE_01_Atrium',144),('CINE_02_Lower_stair',432),('CINE_03_Upper_ribbon',720),('CINE_04_Social_hub',1008),('CINE_05_Stair_well',1296)]
results=[]
if (OUT/'progress.json').exists():
    previous=json.loads((OUT/'progress.json').read_text())
    results=previous.get('results',[])
    done={r['camera'] for r in results}
    queue=[entry for entry in queue if entry[0]not in done]
def render_next(queue=queue,results=results,out=OUT,root=ROOT):
    import bpy,json,time,traceback
    if not queue:
        (out/'progress.json').write_text(json.dumps({'complete':True,'revision':'polish67','results':results},indent=2));return None
    if (out/'STOP').exists():
        (out/'progress.json').write_text(json.dumps({'complete':False,'stopped':True,'remaining':queue,'results':results},indent=2));return None
    name,frame=queue.pop(0);s=bpy.context.scene
    bindings=[(m,m.camera)for m in s.timeline_markers if m.camera]
    s.frame_set(frame)
    for m,c in bindings:m.camera=None
    s.camera=bpy.data.objects[name];s.view_settings.exposure=.7
    s.render.engine='CYCLES';s.render.resolution_x=3840;s.render.resolution_y=2160;s.render.resolution_percentage=100
    s.cycles.samples=256;s.cycles.adaptive_threshold=.006;s.cycles.use_denoising=True
    s.cycles.use_auto_tile=True;s.cycles.tile_size=512;s.render.use_persistent_data=False
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='16'
    s.render.filepath=str(out/(name+'.png'));start=time.time()
    try:
        bpy.ops.render.render(write_still=True)
        results.append({'camera':name,'frame':frame,'width':3840,'height':2160,'samples':256,'seconds':time.time()-start,'file':s.render.filepath})
    except Exception:
        (out/'error.txt').write_text(traceback.format_exc());return None
    finally:
        for m,c in bindings:m.camera=c
    (out/'progress.json').write_text(json.dumps({'complete':False,'revision':'polish67','remaining':queue,'results':results},indent=2));return .5
(OUT/'progress.json').write_text(json.dumps({'complete':False,'revision':'polish67','remaining':queue,'results':results},indent=2))
bpy.app.driver_namespace['isec_hero_queue']=render_next
bpy.app.timers.register(render_next,first_interval=.5)
print('Queued five3840x2160 Cycles hero stills at256samples,16bit PNG')
