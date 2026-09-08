exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# University011 places the camera at the undercroft edge, with blue/gray seatingright
# and white café seatingleft. Move only those documented cluster families.
for ob in bpy.data.objects:
 x,y,z=ob.location
 if z>.1:continue
 if ob.name.startswith(('Petrol lounge','Pewter lounge','Ground cafe table'))and 12<x<14 and 5<y<7:ob.location.x-=3;ob.location.y+=8.5
 if ob.name.startswith(('White cafe chair','Ground cafe table'))and 10<x<12 and -2<y<0:ob.location.x-=1;ob.location.y+=9
cam=bpy.data.objects['REF09_Ground_wide'];cam.location=(13,12.5,1.1);cam.rotation_euler=(Vector((-3,6,8.3))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=16
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Ground photo position and bounded seating cluster placement refined')
