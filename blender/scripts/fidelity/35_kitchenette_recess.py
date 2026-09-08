exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Source REF03 shows a deep curved soffit projecting toward the peninsula. The old
# cove extended behind its mural and was visually buried in the backing wall.
for ob in bpy.data.objects:
 if ob.name.startswith(('Kitchenette curved gray upper surround','Kitchenette white cove underside'))and not ob.get('projected_soffit_v35'):
  ob.location.x-=1.10;ob['projected_soffit_v35']=True
C='Rooms';remove_where(lambda o:o.name.startswith('Kitchenette recessed dark plinth'))
for ob in list(bpy.data.objects):
 if ob.name.startswith('Kitchenette rounded white peninsula'):
  cp=ob.copy();cp.data=ob.data.copy();cp.name='Kitchenette recessed dark plinth';COL[C].objects.link(cp);bottom=min(v.co.z for v in cp.data.vertices);top=max(v.co.z for v in cp.data.vertices);level=round(bottom/H)*H
  for v in cp.data.vertices:v.co.z=level+.035 if abs(v.co.z-bottom)<.001 else level+.13
  cp.data.materials.clear();cp.data.materials.append(dark);finish(cp)
C='Lighting'
for z in FLOORS[1:]:
 for y in [-9.5,-8.3,-7.1]:
  finish(beam('Kitchenette soffit recessed downlight',(.35,y,z+2.753),(.35,y,z+2.775),.048,em),True)
  d=bpy.data.lights.new('Kitchenette soffit warm downlight','AREA');d.energy=20;d.shape='DISK';d.size=.16;d.color=(1,.8,.6);ob=bpy.data.objects.new(d.name,d);COL[C].objects.link(ob);ob.location=(.35,y,z+2.746)
bpy.data.objects['REF03_Social_hub'].data.shift_y=.12;bpy.data.objects['REF03_Social_hub'].data.shift_x=-.06
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
# Camera experiments retain original REF01 until compared.
base=bpy.data.objects['REF01_Payette_atrium'];C='Cameras';remove_where(lambda o:o.name.startswith('TEST01_'))
for idx,(pos,target,lens) in enumerate([((17,3,6.065),(-3,5.1,6.065),20),((15,.6,6.065),(-5,5.6,6.065),18),((18.5,5.5,6.065),(-3,5.4,6.065),21)]):
 ob=bpy.data.objects.new('TEST01_'+str(idx+1),base.data.copy());COL[C].objects.link(ob);ob.location=pos;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.lens=lens;ob['render_width']=1149;ob['render_height']=900
