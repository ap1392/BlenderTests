import bpy
from mathutils import Vector
src=bpy.data.objects['REF08_Stair_overhead']
for name,target in [('TEST08_A_lower_floor',(-.8,1.5,5.5804)),('TEST08_B_lower_left',(-.5,4.1,5.5804))]:
 old=bpy.data.objects.get(name)
 if old:bpy.data.objects.remove(old,do_unlink=True)
 ob=src.copy();ob.data=src.data.copy();ob.name=name;bpy.context.scene.collection.objects.link(ob)
 ob.location=(.75,-.75,19.3034);ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.lens=18
print('Two 18 mm camera-only overhead tests created')
