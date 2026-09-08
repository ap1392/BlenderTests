"""Resume hero stills from the saved master, synchronously with durable progress."""
import bpy,json,time,traceback
from pathlib import Path
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
OUT=ROOT/'renders/cinematic/cycles_heroes';OUT.mkdir(parents=True,exist_ok=True)
state=json.loads((OUT/'progress.json').read_text())if(OUT/'progress.json').exists()else{}
results=state.get('results',[])
done={r['camera']for r in results if Path(r['file']).exists()}
queue=[(n,f)for n,f in [('CINE_01_Atrium',144),('CINE_02_Lower_stair',432),('CINE_03_Upper_ribbon',720),('CINE_04_Social_hub',1008),('CINE_05_Stair_well',1296)]if n not in done]
s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='METAL';prefs.refresh_devices()
for d in prefs.devices:d.use=(d.type=='METAL')
s.cycles.device='GPU';s.render.engine='CYCLES'
s.cycles.use_auto_tile=True;s.cycles.tile_size=512;s.render.use_persistent_data=False
s.cycles.samples=256;s.cycles.use_adaptive_sampling=True;s.cycles.adaptive_threshold=.006;s.cycles.use_denoising=True
s.render.resolution_x=3840;s.render.resolution_y=2160;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='16'
for m in s.timeline_markers:m.camera=None
try:
    while queue:
        name,frame=queue[0];s.frame_set(frame);s.camera=bpy.data.objects[name];s.view_settings.exposure=.7
        s.render.filepath=str(OUT/(name+'.png'))
        (OUT/'progress.json').write_text(json.dumps({'complete':False,'revision':'polish67','active':name,'remaining':queue,'results':results,'runner':'background CLI'},indent=2))
        print('ISEC_HERO_BEGIN',name,flush=True);start=time.time()
        bpy.ops.render.render(write_still=True)
        results.append({'camera':name,'frame':frame,'width':3840,'height':2160,'samples':256,'seconds':time.time()-start,'file':s.render.filepath})
        queue.pop(0)
        (OUT/'progress.json').write_text(json.dumps({'complete':not queue,'revision':'polish67','remaining':queue,'results':results,'runner':'background CLI'},indent=2))
        print('ISEC_HERO_COMPLETE',name,flush=True)
except Exception:
    (OUT/'error.txt').write_text(traceback.format_exc());raise
print('ISEC_HERO_QUEUE_COMPLETE',flush=True)
