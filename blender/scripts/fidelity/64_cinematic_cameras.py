"""Six deliberate 12-second camera moves; master camera tracks and export manifest."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path('/Users/aditya2610/Desktop/Projects3/BlenderTests')
specs=[
 ('01_Atrium', (20.0,10.0,6.05),(19.1,9.55,6.05),(-1,3,11.0),24,'Atrium organization HIGH; exact gallery curves MEDIUM/LOW'),
 ('02_Lower_stair',(12.0,11.5,1.65),(10.5,10.1,1.65),(2.0,0.0,4.2),35,'Lower stair relationship HIGH; curvature MEDIUM'),
 ('03_Upper_ribbon',(16.2,11.7,14.91),(15.0,11.4,14.91),(0,0,14.0),50,'Upper spiral form HIGH; fabrication MEDIUM/LOW. Stabilized atrium-side rig move, not a pedestrian route.'),
 ('04_Social_hub',(-6.8,-12.75,10.44),(-6.25,-12.15,10.44),(-1.1,-6.3,10.8),32,'Documented social feature combination HIGH; canopy and furniture MEDIUM'),
 ('05_Stair_well',(.75,-.75,19.30),(.55,-.60,19.30),(-.5,4.1,5.58),24,'Stair repetition and guards HIGH; exact bottom well contour MEDIUM/LOW'),
 ('06_Final_atrium',(19.1,9.55,6.05),(20.0,10.0,6.05),(-1.5,3.0,10.4),26,'Atrium arrangement HIGH; roof dimensional details LOW and incidental'),
]
collection=bpy.data.collections.get('Cinematic Cameras') or bpy.data.collections.new('Cinematic Cameras')
if collection.name not in bpy.context.scene.collection.children:bpy.context.scene.collection.children.link(collection)
records=[];s=bpy.context.scene;s.render.fps=24;s.frame_start=1;s.frame_end=1728
for idx,(name,start,end,target,lens,confidence) in enumerate(specs):
    name='CINE_'+name
    ob=bpy.data.objects.get(name)
    if not ob:
        ob=bpy.data.objects.new(name,bpy.data.cameras.new(name));collection.objects.link(ob)
    ob.animation_data_clear();ob.data.type='PERSP';ob.data.lens=lens;ob.data.sensor_width=36;ob.data.clip_start=.08;ob.data.clip_end=500
    ob.data.dof.use_dof=False;ob['render_width']=3840;ob['render_height']=2160;ob['photographic_exposure']=.7
    ob['confidence_scope']=confidence
    first=1+idx*288;last=first+287;prev=None;keys=[];ob['first_frame']=first
    for k in range(25):
        f=first+round(287*k/24);t=k/24;e=t*t*(3-2*t)
        p=Vector(start).lerp(Vector(end),e)
        rotation=(Vector(target)-p).to_track_quat('-Z','Y').to_euler('XYZ',prev) if prev else (Vector(target)-p).to_track_quat('-Z','Y').to_euler('XYZ')
        prev=rotation.copy();ob.location=p;ob.rotation_euler=rotation
        ob.keyframe_insert(data_path='location',frame=f);ob.keyframe_insert(data_path='rotation_euler',frame=f)
        keys.append({'frame':f,'location_m':list(p),'rotation_radians':list(rotation)})
    marker=s.timeline_markers.get(name) or s.timeline_markers.new(name,frame=first);marker.frame=first;marker.camera=ob
    records.append({'name':name,'first_frame':first,'last_frame':last,'duration_seconds':12,'lens_mm':lens,'sensor_width_mm':36,'confidence':confidence,'keys':keys})
s.frame_set(1);s.camera=bpy.data.objects['CINE_01_Atrium']
out=ROOT/'unreal/source';out.mkdir(parents=True,exist_ok=True)
(out/'cinematic_camera_manifest.json').write_text(json.dumps({'fps':24,'duration_seconds':72,'resolution':[3840,2160],'units':'meters; Blender right-handed Z-up; convert explicitly at import','shots':records},indent=2))
print('Six 12-second cinematic tracks authored; movement clearance and composition review pending')
