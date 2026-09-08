import bpy
from pathlib import Path
src=bpy.data.objects['TEST08_C_crop_estimate'];ob=bpy.data.objects['REF08_Stair_overhead']
ob.location=src.location;ob.rotation_euler=src.rotation_euler
for name in ['lens','sensor_width','sensor_height','shift_x','shift_y']:setattr(ob.data,name,getattr(src.data,name))
ob['photographic_exposure']=1.7
ob['crop_estimate']=src['crop_estimate']
ob['calibration_note']='One story lower, at L5 eye height; three-turn source count. 18 mm EXIF retained, inferred 5904/7360 sensor crop. One-stop exposure increase to match the bright photographic source; geometry unchanged.'
bpy.data.batch_remove([o for o in bpy.data.objects if o.type=='CAMERA'and o.name.startswith('TEST08_')])
bpy.context.scene.camera=ob
bpy.ops.wm.save_as_mainfile(filepath='/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/ISEC_Master.blend')
print('Accepted source-matched overhead camera C; test cameras removed')
