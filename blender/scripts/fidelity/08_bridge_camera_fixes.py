exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Strip offsets must point into the building, away from the atrium void.
remove_where(lambda o:'restored end bridge floor'in o.name or 'restored end bridge carpet'in o.name)
C='Architecture'
for lev,z in enumerate(FLOORS[1:],2):
 for path,width in [([(-20.1,7.1),(-17.9,-.7)],3.3),([(18.8,12.3),(19,5.0)],-4.)]:
  finish(strip(f'L{lev} corrected end bridge floor',path,width,z,.42,white));strip(f'L{lev} corrected end bridge carpet',path,width,z+.016,.016,carpet)
# At the end lounges the outer boundary is exterior glass, not repeating office leaves.
def centroid(o):
 if o.type!='MESH':return o.location
 return o.matrix_world@(sum((Vector(v)for v in o.bound_box),Vector())/8)
remove_where(lambda o:o.name.startswith(('Office glazed public frontage','Closed oak office leaf','Office silver vertical frame')) and ((centroid(o).x>17 and centroid(o).y>2)or(-5<centroid(o).x<4)))
remove_where(lambda o:o.name.startswith(('Office continuous gray header','Office interior limited closure')))
C='Rooms';back=path_resample(offset(south,3.32),45);gray=bpy.data.materials['Office charcoal paint']
for lev,z in enumerate(FLOORS[1:],2):
 for i in range(len(back)-1):
  p,q=back[i:i+2];x=(p[0]+q[0])/2;y=(p[1]+q[1])/2
  if (x>17 and y>2)or(-5<x<4):continue
  ribbon('Office corrected gray header',[p,q],[z+2.76]*2,H-2.76,.18,gray)
  inner=offset([p,q],2.8);ribbon('Office shallow rear closure',inner,[z]*2,3.0,.18,white)
  poly('Office shallow interior floor',[p,q]+inner[::-1],z,.18,carpet)
  poly('Office shallow interior ceiling',[p,q]+inner[::-1],z+2.98,.08,white,False)
def camera(name,loc,target,lens,shift=0):
 o=bpy.data.objects[name];o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;o.data.shift_y=shift
p=json.loads((ROOT/'references/fidelity/calibration/hero_near_far_fit.json').read_text())['parameters'];camera('REF01_Payette_atrium',p[:3],(p[0]-cos(p[3]),p[1]+sin(p[3]),p[2]),p[4]/1149*36,(p[5]-450)/1149)
camera('REF02_Reverse_soffit',(3.0,-2.7,2*H+1.45),(16,10.5,7.2),22)
camera('REF08_Stair_overhead',(0.0,0.0,24.9),(0,0,10),13)
o=bpy.data.objects['REF08_Stair_overhead'];o['reference']='references/fidelity/atrium/isec_reflections_004-1.jpg';o['render_width']=1280;o['render_height']=1280
# Primitive old lounge seating is replaced in the following furniture pass.
remove_where(lambda o:COL['Furniture'] in o.users_collection and o.name.startswith(('Egg lounge','Sculpted upholstered','Bucket chair','Swivel stem','Four star base','Chair collision')))
# Panes span groups of treads, as-built clamping is much less busy than per-tread.
remove_where(lambda o:o.name.startswith('Circular glass clamp') and int(o.name.rsplit('.',1)[-1])%3!=0 if '.'in o.name and o.name.startswith('Circular glass clamp')else False)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Bridge directions, public openings and near/far camera corrected')
