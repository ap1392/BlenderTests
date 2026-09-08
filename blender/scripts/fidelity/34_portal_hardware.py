exec(compile(open('/Users/aditya2610/Desktop/Projects3/BlenderTests/blender/scripts/fidelity/common.py').read(),'common.py','exec'))
# Helper boxes store their positions in mesh vertices, so reflect the actual geometry.
for ob in bpy.data.objects:
 if ob.name.startswith(('Elevator central leaf joint','Elevator indicator dark face','Elevator blue indicator')):
  ob.location.y=0
  if not ob.get('hardware_mesh_face_v34'):
   for v in ob.data.vertices:v.co.y=-12.2-v.co.y
   ob['hardware_mesh_face_v34']=True;finish(ob)
# L4 published west throat: closed door pair and opaque surround. Number assignment unverified.
remove_where(lambda o:o.name.startswith('L4 west social portal'))
C='Rooms';p=Vector((-9.1,-8.8));q=Vector((-6.9,-10));t=(q-p).normalized();n=Vector((-t.y,t.x));mid=(p+q)/2;width=(q-p).length;z=FLOORS[3]
gray=bpy.data.materials['Office charcoal paint'];leaf=bpy.data.materials.get('Deep olive portal leaf')or mat('Deep olive portal leaf',(.12,.19,.105),.48)
def bx(name,u,depth,h,w,d,ht,ma):
 pos=mid+t*u+n*depth;ob=box('L4 west social portal '+name,(0,0,h+z),(w,d,ht),ma,False,.006);ob.rotation_euler.z=math.atan2(t.y,t.x);ob.location.x=pos.x;ob.location.y=pos.y;return ob
for u in [-width/2+.11,width/2-.11]:bx('gray jamb',u,0,H/2,.22,.28,H,gray)
bx('gray head',0,0,(H+2.55)/2,width,.28,H-2.55,gray)
for u in [-width/2+.245,width/2-.245]:bx('lime reveal',u,.015,1.275,.05,.30,2.55,lime)
bx('lime reveal head',0,.015,2.52,width-.44,.30,.07,lime)
clear=width-.54
for u in [-clear/4,clear/4]:
 bx('closed olive leaf',u,-.015,1.23,clear/2-.012,.055,2.46,leaf)
 bx('leaf lower kickplate',u,.016,.16,clear/2-.075,.008,.24,metal)
 pos=mid+t*(u+(.28 if u<0 else -.28))+n*.068
 beam('L4 west social portal vertical pull',(*pos,z+.92),(*pos,z+1.22),.014,metal)
bpy.context.scene['west_social_portal']='Published L4 double-door throat(-9.1,-8.8) to(-6.9,-10.0); NE-facing, closed. Green finish photo-informed; specific401–419 attribution not asserted.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/ISEC_Master.blend'))
