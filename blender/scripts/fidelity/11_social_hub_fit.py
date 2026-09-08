exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
def center(o):return o.matrix_world@(sum((Vector(v)for v in o.bound_box),Vector())/8)if o.type=='MESH'else o.location
remove_where(lambda o:o.name.startswith(('Office glazed public frontage','Closed oak office leaf','Office silver vertical frame','Office corrected gray header','Office shallow rear closure','Office shallow interior ceiling')) and -8.5<center(o).x<4)
for lev,z in enumerate(FLOORS[1:],2):
 C='Architecture';poly('Social pod plan-supported rear public floor',[(-8,-9),(-4,-6),(3,-3.3),(4,-13.5),(-8,-13.5)],z,.42,white);poly('Social pod rear public carpet',[(-8,-9),(-4,-6),(3,-3.3),(4,-13.5),(-8,-13.5)],z+.018,.018,carpet)
 C='Ceiling';poly('Social pod overhead acoustic plane',[(-8,-9),(-4,-6),(3,-3.3),(4,-13.5),(-8,-13.5)],z+H-.05,.05,black,False)
 for i in range(58):box('Social pod rear straight oak blade',(-8+i*.21,-11.7,z+H-.46),(.038,3.6,.23),wood)
 C='Lighting'
 for x,y,r in [(-5.8,-11.5,.90),(-4.4,-9.6,.46),(-2.9,-10.7,.64),(-1.4,-8.3,.80)]:
  h=z+H-.75;finish(beam('Social pod varied drum housing',(x,y,h),(x,y,h+.17),r,white),True);finish(beam('Social pod varied drum diffuser',(x,y,h-.015),(x,y,h),r*.96,em),True)
  data=bpy.data.lights.new('Social pod drum downlight','AREA');data.energy=65;data.shape='DISK';data.size=r*1.8;data.color=(1,.91,.78);o=bpy.data.objects.new('Social pod drum downlight',data);COL[C].objects.link(o);o.location=(x,y,h-.028)
# Move social view back into the larger actual office pod, so bar and stair share frame.
cam=bpy.data.objects['REF03_Social_hub'];cam.location=(-6.4,-12.2,2*H+1.6);target=Vector((1.3,-2.0,2*H+1.6));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=23;cam.data.shift_y=.04
cam=bpy.data.objects['REF04_Writeup'];cam.location.y=11.1
cam=bpy.data.objects['REF05_Lower_stair'];cam.data.lens=37;cam.rotation_euler=(Vector((3.9,.7,2.0))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
print('Social pod depth and camera framing refined')
